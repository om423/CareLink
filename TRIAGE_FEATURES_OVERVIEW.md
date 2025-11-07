# CareLink Triage Features Overview

**Technical Summary for User Stories #2, #4, #6**

---

## 1. Feature Overview

The triage subsystem enables patients to describe symptoms in plain language and receive AI-powered preliminary assessments. The flow works as follows:

1. **Patient Input**: User types symptoms in a chat interface (`/triage/chat/`)
2. **Context Enrichment**: System retrieves patient profile data (age, weight, allergies, medical history)
3. **AI Processing**: Symptoms + patient context are sent to Google Gemini API via `GeminiClient`
4. **Response Parsing**: AI returns structured JSON with severity, summary, advice, red flags, differential diagnosis, and rationale
5. **Persistence**: Full assessment saved to `TriageInteraction` model
6. **Severity Display**: Color-coded severity badge (Mild/Moderate/Severe/Critical) displayed in UI
7. **History Tracking**: All interactions stored and accessible via `/triage/history/` with detail views

The system supports multi-turn conversations via `session_id` tracking, allowing follow-up questions within a single triage session.

---

## 2. Feature Mapping Table

| User Story | Summary | Key Files | Routes | Database Models | UI Templates |
|------------|---------|-----------|--------|-----------------|--------------|
| **#2: Symptom → AI Diagnosis** | Patients describe symptoms, receive AI assessment | `triage/views.py` (chat_api), `gemini_client.py` | `POST /triage/chat/api/` | `TriageInteraction` | `templates/triage/chat.html` |
| **#4: Severity Levels** | AI assigns severity (Mild/Moderate/Severe/Critical) with color coding | `gemini_client.py` (_build_prompt), `chat.html` (getSeverityColor) | All triage routes | `TriageInteraction.severity` | `chat.html`, `history.html`, `detail.html` |
| **#6: Triage History** | Patients review past assessments | `triage/views.py` (history, detail) | `GET /triage/history/`, `GET /triage/history/<id>/` | `TriageInteraction` | `templates/triage/history.html`, `templates/triage/detail.html` |

---

## 3. Architecture Notes

### GeminiClient Integration

**Location**: `carelink/common/services/gemini_client.py`

**Key Methods**:
- `generate_triage(symptoms_text, patient_context)` → Returns dict with `severity`, `summary`, `advice`, `red_flags`, `differential`, `rationale`
- `_build_prompt(symptoms_text, patient_context)` → Constructs prompt with patient context JSON block
- `_request_with_retry(prompt)` → Calls Gemini API with model fallbacks (`gemini-2.0-flash` → `gemini-2.5-flash` → `gemini-1.5-flash-8b` → `gemini-1.5-flash-latest` → `gemini-1.5-pro`)
- `_parse_or_repair(raw_text, original_prompt)` → Handles JSON parsing, strips code fences, attempts repair on malformed responses

**Django View Integration** (`triage/views.py:chat_api`):
```python
api_key = getattr(settings, "GEMINI_API_KEY", None)
client = GeminiClient(api_key=api_key)
patient_ctx = get_patient_context(request.user)
result = client.generate_triage(combined_symptoms, patient_context=patient_ctx)
```

### Patient Context Injection

**Helper Function**: `get_patient_context(user)` in `triage/views.py:55-69`

**Process**:
1. Retrieves `PatientProfile` for user (if exists)
2. Extracts: `age`, `weight`, `medical_history` (truncated to 300 chars), `allergies` (truncated to 200 chars)
3. Passes to `GeminiClient._build_prompt()` as dict

**Prompt Format** (`gemini_client.py:261-268`):
```python
patient_context_block = (
    "{\n"
    f'  "age": "{age}",\n'
    f'  "weight": "{weight}",\n'
    f'  "allergies": "{allergies}",\n'
    f'  "medical_history": "{med_hist}"\n'
    "}"
)
```

**System Instructions** (`gemini_client.py:28-37`):
- Instructs AI to use patient context for risk assessment
- Notes allergies for medication interactions
- Factors comorbidities from medical history into severity

### Severity Derivation & Display

**Severity Source**: Extracted from AI JSON response (`gemini_client.py:128`)
- Values: `"Mild"`, `"Moderate"`, `"Severe"`, `"Critical"`
- Default fallback: `"Moderate"` if parsing fails

**Color Mapping** (`templates/triage/chat.html:209-216`):
- Critical → `var(--cl-red)` (#e74c3c)
- Severe → `var(--cl-amber)` (#f39c12)
- Moderate → `var(--cl-teal)` (#2d9cdb)
- Mild → `var(--cl-green)` (#27ae60)

**Display Locations**:
- **Chat Page**: Sidebar widget + inline badge with AI response
- **History List**: Color-coded badge per interaction card
- **Detail Page**: Large prominent badge in dedicated card

### Triage History Storage & Retrieval

**Model**: `TriageInteraction` (`triage/models.py:5-19`)
```python
class TriageInteraction(models.Model):
    user = ForeignKey(User)
    session_id = CharField(255)  # Groups multi-turn conversations
    symptoms_text = TextField()
    severity = CharField(20)
    result = JSONField()  # Full AI response
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Storage Logic** (`triage/views.py:116-144`):
- If `session_id` provided: Updates existing interaction or creates new
- If no `session_id`: Creates new interaction
- Saves combined symptoms (includes conversation history), severity, full JSON result
- Non-fatal: Persistence failures don't block UI

**Retrieval Logic** (`triage/views.py:21-43`):
- Filters by `user=request.user` (user isolation)
- Groups by `session_id`, takes latest interaction per session
- Orders by `-updated_at` (most recent first)
- For interactions without `session_id`, each treated as separate session

**Detail View Security** (`triage/views.py:51`):
```python
interaction = get_object_or_404(TriageInteraction, id=interaction_id, user=request.user)
```
Prevents cross-user access via user filter in query.

---

## 4. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ Patient (Browser)                                               │
│  └─> Types symptoms in chat.html textarea                      │
│      └─> JavaScript AJAX POST to /triage/chat/api/           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ Django View: chat_api() (triage/views.py:80-155)               │
│  ├─> Parse JSON body (symptoms, conversation_history, session_id)│
│  ├─> get_patient_context(user) → Extract PatientProfile data  │
│  └─> Combine conversation history + current symptoms           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ GeminiClient.generate_triage()                                  │
│  ├─> _build_prompt(symptoms, patient_context)                  │
│  │   └─> Format patient context as JSON block                 │
│  │   └─> Include system instructions for conservative triage   │
│  ├─> _request_with_retry(prompt)                               │
│  │   └─> Call Gemini API (with model fallbacks)                │
│  └─> _parse_or_repair(raw_response)                            │
│      └─> Extract JSON, handle code fences, repair if needed   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ AI Response (JSON)                                              │
│  {                                                               │
│    "severity": "Moderate",                                      │
│    "summary": "...",                                            │
│    "advice": "...",                                             │
│    "red_flags": [...],                                           │
│    "differential": [...],                                       │
│    "rationale": "..."                                           │
│  }                                                               │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ Persistence: TriageInteraction.objects.get_or_create()          │
│  ├─> Save symptoms_text (combined)                            │
│  ├─> Save severity                                             │
│  ├─> Save result (full JSON)                                   │
│  └─> Update if session_id exists, else create new             │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ JSON Response to Browser                                        │
│  └─> JavaScript renders AI response in chat UI                 │
│      ├─> Display severity badge (color-coded)                  │
│      ├─> Show summary, advice, red flags, differential         │
│      └─> Update sidebar severity widget                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ History Flow                                                     │
│  GET /triage/history/                                           │
│    └─> Query TriageInteraction (grouped by session_id)         │
│        └─> Render history.html with interaction cards          │
│                                                                  │
│  GET /triage/history/<id>/                                      │
│    └─> Get specific TriageInteraction (user-filtered)           │
│        └─> Render detail.html with full assessment             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Testing & QA Summary

### Test Coverage (`tests/test_triage_chat.py`)

| Test Case | Purpose | Status |
|-----------|---------|--------|
| `test_triage_chat_get_requires_login` | Verify authentication requirement | ✅ Pass |
| `test_triage_chat_post_monkeypatched` | Full flow with mocked Gemini API | ✅ Pass |
| `test_build_prompt_unknown_defaults` | Prompt construction with missing context | ✅ Pass |
| `test_json_repair_flow` | JSON parsing and repair logic | ✅ Pass |
| `test_transient_error_backoff` | Retry mechanism for API failures | ✅ Pass |
| `test_context_card_rendered` | Patient context display in UI | ✅ Pass |

### Test Approach

- **Mocking**: Uses `monkeypatch` to mock `GeminiClient` methods, avoiding real API calls
- **Isolation**: Each test creates isolated user accounts
- **Validation**: Checks prompt construction, JSON parsing, error handling, UI rendering

### Missing/Suggested Test Areas

1. **Integration Tests**:
   - End-to-end flow with real Gemini API (requires `GEMINI_API_KEY`)
   - Multi-turn conversation persistence
   - Session ID grouping logic

2. **Edge Cases**:
   - Very long symptom descriptions (>10,000 chars)
   - Missing patient profile (all fields None)
   - Invalid severity values from AI
   - Concurrent requests for same session_id

3. **Security Tests**:
   - Cross-user access prevention (detail view)
   - CSRF token validation
   - XSS prevention in symptom text rendering

4. **Performance Tests**:
   - API timeout handling
   - Database query optimization (history view with many interactions)
   - Large JSON result storage

---

## 6. Environment Requirements

### Environment Variables

**Required**:
- `GEMINI_API_KEY` - Google Gemini API key
  - Location: `carelink/settings/base.py:21`
  - Format: String (e.g., `"AIzaSy..."`
  - If missing: `GeminiClient` raises `RuntimeError` when called

**Optional**:
- `.env` file support via `django-environ`
- Default: `None` (will fail at runtime if API called)

### Python Dependencies

**Required Packages**:
- `google-genai` OR `google-generativeai` (either works, `GeminiClient` tries both)
- `Django >= 5.1.1`
- Standard Django packages (`django.contrib.auth`, etc.)

**Installation**:
```bash
pip install google-genai  # or google-generativeai
```

### Authentication Requirements

**All Triage Routes Require Login**:
- `@login_required` decorator on all views (`chat`, `chat_api`, `history`, `detail`)
- Unauthenticated users redirected to login page
- User isolation enforced via `user=request.user` filter in queries

### Patient Profile (Optional but Recommended)

- **Model**: `profiles.models.PatientProfile`
- **Fields Used**: `age`, `weight`, `medical_history`, `allergies`
- **Enhancement**: Improves AI accuracy but not required
- **Fallback**: If profile missing, context defaults to "Unknown" or "None reported"

---

## Quick Reference

**Key Routes**:
- `GET /triage/chat/` - Chat interface
- `POST /triage/chat/api/` - Submit symptoms (AJAX)
- `GET /triage/history/` - List all interactions
- `GET /triage/history/<id>/` - View specific interaction

**Key Models**:
- `TriageInteraction` - Stores symptoms, severity, AI result

**Key Services**:
- `GeminiClient` - Google Gemini API wrapper

**Key Templates**:
- `templates/triage/chat.html` - Chat UI
- `templates/triage/history.html` - History list
- `templates/triage/detail.html` - Detail view

---

**Last Updated**: November 2025  
**Django Version**: 5.1.1  
**Status**: Production-ready for User Stories #2, #4, #6

