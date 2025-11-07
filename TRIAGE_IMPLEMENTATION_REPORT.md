# CareLink Triage Implementation Report
## User Stories #2, #4, and #6 Technical Summary

**Date:** November 2025  
**Scope:** Analysis of AI triage functionality for patient symptom assessment and history tracking

---

## Executive Summary

All three user stories (#2, #4, #6) are **fully implemented** with a complete end-to-end flow from user input through AI processing to persistent storage and retrieval. The implementation uses Google Gemini AI for symptom analysis, stores results in a Django model, and provides comprehensive UI for both real-time chat and historical review.

---

## User Story #2: Plain Language Symptom Description → AI Preliminary Diagnosis

### ✅ Implementation Status: **FULLY IMPLEMENTED**

### Files and Functions

#### **Backend Views** (`triage/views.py`)
- **`chat(request)`** (lines 72-76): Renders the chat interface page
  - Route: `/triage/chat/`
  - Requires: `@login_required`
  - Passes patient context to template
  
- **`chat_api(request)`** (lines 79-156): AJAX endpoint for symptom submission
  - Route: `/triage/chat/api/`
  - Method: POST only
  - Accepts JSON body with:
    - `symptoms`: string (required)
    - `conversation_history`: array (optional, for multi-turn conversations)
    - `session_id`: string (optional, for session tracking)
  - Returns JSON response with AI triage result

- **`get_patient_context(user)`** (lines 55-69): Helper function
  - Extracts patient profile data (age, weight, medical_history, allergies)
  - Used to enhance AI prompts with patient-specific context
  - Handles missing profiles gracefully

#### **AI Service Client** (`carelink/common/services/gemini_client.py`)
- **`GeminiClient`** class (lines 65-286): Complete Gemini API wrapper
  - **`__init__()`** (lines 77-114): Initializes client with API key
    - Supports both new (`google.genai`) and legacy (`google.generativeai`) SDKs
    - Falls back through multiple model versions if primary fails
    - Models tried: `gemini-2.0-flash` → `gemini-2.5-flash` → `gemini-1.5-flash-8b` → `gemini-1.5-flash-latest` → `gemini-1.5-pro`
  
  - **`generate_triage(symptoms_text, patient_context)`** (lines 116-143): Main entry point
    - Builds prompt with patient context
    - Calls Gemini API with retry logic
    - Parses JSON response
    - Returns structured dict with keys: `severity`, `summary`, `advice`, `red_flags`, `differential`, `rationale`
  
  - **`_build_prompt(symptoms_text, patient_context)`** (lines 246-285): Prompt construction
    - Formats patient context (age, weight, allergies, medical_history) as JSON
    - Includes system instructions for conservative medical triage
    - Specifies required JSON output format
  
  - **`_request_with_retry(prompt)`** (lines 145-201): API call with fallbacks
    - Retries once on failure (with 0.6s delay)
    - Tries multiple model variants if primary fails
    - Handles both new and legacy SDK paths
  
  - **`_parse_or_repair(raw_text, original_prompt)`** (lines 203-243): JSON parsing
    - Strips code fences (```json ... ```)
    - Extracts JSON blocks from mixed text
    - Attempts repair by re-requesting if parsing fails
    - Falls back to safe defaults if all parsing fails

#### **Frontend Template** (`templates/triage/chat.html`)
- **Lines 1-387**: Complete chat interface
  - Real-time message display (lines 32-49: initial greeting)
  - Text input form (lines 52-63)
  - Sidebar with patient context display (lines 71-85)
  - Severity assessment widget (lines 87-99)
  - JavaScript chat handler (lines 137-386)
    - `addUserMessage(text)`: Displays user input
    - `addAIResponse(result)`: Renders AI assessment with severity badge
    - `updateSeverityDisplay(severity)`: Updates sidebar severity indicator
    - `getSeverityColor(severity)`: Maps severity to color (Critical→red, Severe→amber, Moderate→teal, Mild→green)
    - AJAX submission to `/triage/chat/api/`
    - Conversation history tracking for multi-turn chats
    - Session ID generation for grouping related interactions

### Data Flow

1. **User Input** → Patient types symptoms in textarea (`chat.html` line 55)
2. **JavaScript Handler** → Form submission intercepted, AJAX POST to `/triage/chat/api/` (lines 305-374)
3. **View Processing** → `chat_api()` receives JSON, extracts symptoms and conversation history (lines 86-96)
4. **Context Enrichment** → `get_patient_context()` retrieves patient profile data (line 100)
5. **AI Processing** → `GeminiClient.generate_triage()` builds prompt and calls Gemini API (lines 113)
6. **Response Parsing** → JSON response parsed into structured dict (lines 127-134)
7. **Persistence** → `TriageInteraction` model created/updated with result (lines 116-144)
8. **UI Update** → JavaScript receives JSON response, renders AI assessment in chat (lines 345-359)

### Models and Database Fields

**`TriageInteraction` model** (`triage/models.py`, lines 5-19):
- `user`: ForeignKey to User (required)
- `session_id`: CharField(255) - Groups multi-turn conversations
- `symptoms_text`: TextField - Full symptom description (may include conversation history)
- `severity`: CharField(20) - One of: "Mild", "Moderate", "Severe", "Critical"
- `result`: JSONField - Complete AI response with all fields
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)

**Database Migrations:**
- `0001_initial.py`: Creates `TriageRequest` model (deprecated, later deleted)
- `0002_triageinteraction.py`: Creates `TriageInteraction` model
- `0003_alter_triageinteraction_options_and_more.py`: Adds `session_id` and `updated_at`, deletes `TriageRequest`

### Routes

- **GET `/triage/chat/`**: Render chat page (`triage:chat`)
- **POST `/triage/chat/api/`**: Submit symptoms, get AI response (`triage:chat_api`)

### Dependencies

- **Required**: `GEMINI_API_KEY` environment variable (configured in `carelink/settings/base.py` line 21)
- **Python Packages**: `google-genai` or `google-generativeai` (checked in `gemini_client.py` lines 7-17)
- **User State**: Must be logged in (`@login_required` decorator)
- **Patient Profile**: Optional but recommended (enhances AI accuracy)

### Tests

**`tests/test_triage_chat.py`**:
- `test_triage_chat_get_requires_login()`: Verifies authentication requirement
- `test_triage_chat_post_monkeypatched()`: Tests full flow with mocked Gemini API
- `test_build_prompt_unknown_defaults()`: Validates prompt construction with missing context
- `test_json_repair_flow()`: Tests JSON parsing and repair logic
- `test_transient_error_backoff()`: Tests retry mechanism
- `test_context_card_rendered()`: Verifies patient context display in UI

---

## User Story #4: Estimated Severity Levels for ER/Clinic Decision

### ✅ Implementation Status: **FULLY IMPLEMENTED**

### Files and Functions

#### **Severity Assessment**

**AI Severity Classification** (`carelink/common/services/gemini_client.py`):
- **System Instructions** (lines 28-37): Explicitly instructs AI to return severity as one of:
  - `"Mild"`
  - `"Moderate"`
  - `"Severe"`
  - `"Critical"`
- **Response Structure** (lines 127-134): Severity is extracted from AI JSON response
- **Fallback Handling** (lines 128, 137): Defaults to `"Moderate"` if parsing fails

**Severity Display Logic** (`templates/triage/chat.html`):
- **`getSeverityColor(severity)`** (lines 209-216): Maps severity to CSS color variables
  - Critical → `var(--cl-red)` (#e74c3c)
  - Severe → `var(--cl-amber)` (#f39c12)
  - Moderate → `var(--cl-teal)` (#2d9cdb)
  - Mild → `var(--cl-green)` (#27ae60)

- **Severity Badge in Chat** (lines 257): Displays severity badge next to AI response
- **Sidebar Severity Widget** (lines 87-99, 278-282): Dedicated severity assessment card
  - Shows "Severity will be assessed after you submit" initially
  - Updates dynamically after AI response with colored badge

**Severity in History** (`templates/triage/history.html`):
- **Lines 49-58**: Severity badge displayed prominently in history list
  - Color-coded based on severity level
  - Uses same color mapping as chat interface

**Severity in Detail View** (`templates/triage/detail.html`):
- **Lines 34-51**: Large severity badge in dedicated card
  - Centered display with prominent styling
  - Color-coded for quick visual assessment

### Data Flow

1. **AI Assessment** → Gemini returns severity in JSON response (`gemini_client.py` line 128)
2. **Storage** → Severity saved to `TriageInteraction.severity` field (`views.py` line 124, 131)
3. **UI Rendering** → JavaScript receives severity, applies color mapping (`chat.html` line 274)
4. **Display** → Severity badge rendered in chat, sidebar, history, and detail views

### Visual Indicators

**Color Coding System:**
- **Critical (Red)**: Emergency situations, immediate medical attention required
- **Severe (Amber)**: Urgent care needed, consider ER or urgent care clinic
- **Moderate (Teal)**: Standard clinic visit recommended
- **Mild (Green)**: Self-care or routine follow-up may be sufficient

**UI Components:**
- Chat message badges (inline with AI response)
- Sidebar assessment widget (persistent during chat session)
- History list badges (quick overview)
- Detail page prominent display (full assessment view)

### Routes

- All triage routes display severity:
  - `/triage/chat/` - Real-time severity assessment
  - `/triage/history/` - Severity badges in list view
  - `/triage/history/<id>/` - Prominent severity display in detail view

### Dependencies

- Same as User Story #2 (AI integration, patient context)
- Severity is derived from AI response, not calculated separately

---

## User Story #6: Review AI-Generated Triage History

### ✅ Implementation Status: **FULLY IMPLEMENTED**

### Files and Functions

#### **Backend Views** (`triage/views.py`)

- **`history(request)`** (lines 21-43): List view of all triage interactions
  - Route: `/triage/history/`
  - Requires: `@login_required`
  - Queries: Gets unique sessions (latest interaction per `session_id`)
  - For interactions without `session_id`, each is treated as separate session
  - Orders by `-updated_at` (most recent first)
  - Passes `interactions` queryset to template

- **`detail(request, interaction_id)`** (lines 47-52): Detailed view of single interaction
  - Route: `/triage/history/<int:interaction_id>/`
  - Requires: `@login_required`
  - Security: Uses `get_object_or_404` with user filter (prevents cross-user access)
  - Passes single `interaction` object to template

#### **Frontend Templates**

**History List** (`templates/triage/history.html`, lines 1-124):
- **Header** (lines 7-24): Page title with "New Triage" button
- **Interaction Cards** (lines 28-90): Grid layout showing:
  - Date/time (lines 35-46): Formatted as day, month/year, time
  - Severity badge (lines 49-58): Color-coded severity indicator
  - Symptoms preview (lines 60-69): Truncated to 30 words with ellipsis
  - Summary preview (lines 79-86): If available, truncated to 20 words
  - "View Details" button (lines 72-76): Links to detail page
- **Empty State** (lines 100-114): Message when no history exists
- **Pagination Info** (lines 94-98): Shows count of interactions

**Detail View** (`templates/triage/detail.html`, lines 1-222):
- **Header** (lines 7-28): Interaction date/time, "New Assessment" button
- **Severity Card** (lines 34-51): Large, prominent severity display
- **Symptoms Card** (lines 53-64): Full symptom text (preserves line breaks)
- **AI Assessment Card** (lines 66-149): Complete breakdown:
  - Summary (lines 77-84)
  - Red Flags (lines 86-99): List of concerning symptoms
  - Differential Diagnosis (lines 101-114): Possible causes (with disclaimer)
  - Advice (lines 116-125): Next steps for patient
  - Rationale (lines 127-136): AI reasoning
  - Disclaimer (lines 138-144): Not a medical diagnosis
- **Sidebar** (lines 152-217):
  - Quick Actions: New Assessment, Find Nearby Care, Book Appointment, Print Report
  - Assessment Details: Date, time, assessment ID
  - Emergency Notice: Call 911 button

### Data Flow

1. **Storage** → Each triage interaction saved to `TriageInteraction` model (`views.py` lines 116-144)
2. **Query** → `history()` view queries user's interactions, groups by session (`views.py` lines 28-41)
3. **List Rendering** → Template displays summary cards with key info (`history.html` lines 28-90)
4. **Detail Access** → User clicks "View Details", `detail()` view fetches specific interaction (`views.py` line 51)
5. **Full Display** → Detail template renders complete assessment data (`detail.html` lines 31-149)

### Models and Database Fields

**Same as User Story #2** - Uses `TriageInteraction` model:
- `id`: Primary key (used in detail URL)
- `user`: ForeignKey (filters to current user only)
- `session_id`: Groups multi-turn conversations
- `symptoms_text`: Full symptom description
- `severity`: Severity level
- `result`: JSONField with complete AI response
- `created_at`: When interaction was first created
- `updated_at`: When interaction was last updated (used for ordering)

### Routes

- **GET `/triage/history/`**: List all triage interactions (`triage:history`)
- **GET `/triage/history/<id>/`**: View specific interaction details (`triage:detail`)

### Navigation Integration

**Navbar Links** (`templates/base.html`):
- Line 50: "Triage" link in navbar (for patients)
- Links to `/triage/chat/` for new assessments

**Cross-Page Links:**
- Chat page → History button (line 19 in `chat.html`)
- History page → New Triage button (line 19 in `history.html`)
- History page → View Details buttons (line 73 in `history.html`)
- Detail page → Back to History (line 11 in `detail.html`)
- Detail page → New Assessment (line 22 in `detail.html`)

### Admin Integration

**Django Admin** (`triage/admin.py`):
- `TriageInteractionAdmin` registered (lines 5-9)
- List display: user, severity, created_at
- Filters: severity, created_at
- Search: username, symptoms_text
- Allows admins to view and manage all triage interactions

### Dependencies

- **Authentication**: Must be logged in (`@login_required`)
- **User Isolation**: Each user only sees their own interactions (enforced in views)
- **Data Persistence**: Relies on `TriageInteraction` model storage

---

## Overlapping Code and Reuse

### Shared Components

1. **`TriageInteraction` Model**: Used by all three stories
   - Stores symptoms, severity, and full AI result
   - Single source of truth for triage data

2. **`GeminiClient` Service**: Used by Story #2 and indirectly by #4 and #6
   - Generates severity assessment
   - Returns structured JSON with all assessment fields

3. **Severity Color Mapping**: Consistent across all templates
   - `getSeverityColor()` function in `chat.html` (lines 209-216)
   - Same color logic in `history.html` (lines 51-55)
   - Same color logic in `detail.html` (lines 43-47)

4. **Patient Context**: Used in Story #2, displayed in chat UI
   - `get_patient_context()` helper function
   - Enhances AI accuracy for all assessments

5. **Session Tracking**: Groups multi-turn conversations
   - `session_id` field allows conversation continuity
   - History view groups by session (latest interaction per session)

### Data Flow Reuse

- **Story #2** creates `TriageInteraction` records
- **Story #4** reads severity from same records
- **Story #6** reads all fields from same records for display

---

## Configuration and Environment

### Required Settings

**`carelink/settings/base.py`**:
- Line 21: `GEMINI_API_KEY = env("GEMINI_API_KEY", default=None)`
- Must be set in environment or `.env` file for AI functionality

### Python Dependencies

**`requirements.txt`** (implied):
- `google-genai` or `google-generativeai` package
- Django 5.1.1+
- Standard Django packages

### Environment Variables

- `GEMINI_API_KEY`: Google Gemini API key (required for AI features)
- If not set, `GeminiClient` raises `RuntimeError` when called

---

## Security Considerations

1. **Authentication**: All triage views require `@login_required`
2. **User Isolation**: `detail()` view filters by `user=request.user` (prevents cross-user access)
3. **CSRF Protection**: All forms use `{% csrf_token %}`
4. **XSS Prevention**: JavaScript uses `escapeHtml()` function for user input (line 298 in `chat.html`)
5. **Input Validation**: Backend validates JSON and required fields (`views.py` lines 86-96)

---

## Known Limitations and Assumptions

### Limitations

1. **API Dependency**: Requires `GEMINI_API_KEY` to function
   - Without API key, triage fails with error message
   - Tests mock the API to avoid dependency

2. **Session Management**: Session IDs generated client-side
   - No server-side session validation
   - Potential for session ID collisions (low probability)

3. **Conversation History**: Stored in browser memory
   - Lost on page refresh
   - Not persisted between sessions

4. **Error Handling**: Database persistence failures are non-fatal
   - UI continues to work even if saving fails (line 142-144 in `views.py`)
   - User may lose assessment if database write fails

### Assumptions

1. **Patient Profile**: Optional but recommended
   - System works without profile, but AI accuracy improves with context
   - Age, weight, allergies, medical_history enhance assessment

2. **User Roles**: Triage accessible to all authenticated users
   - Navbar shows "Triage" link for patients (line 50 in `base.html`)
   - No role-based restrictions on triage views (only `@login_required`)

3. **AI Model Availability**: Assumes Gemini API is accessible
   - Multiple fallback models attempted if primary fails
   - Retry logic handles transient failures

---

## Testing Coverage

### Unit Tests (`tests/test_triage_chat.py`)

1. **Authentication**: Verifies login requirement
2. **Full Flow**: Tests complete symptom → AI → response cycle
3. **Prompt Construction**: Validates patient context inclusion
4. **JSON Parsing**: Tests repair logic for malformed responses
5. **Error Handling**: Tests retry mechanism for transient failures
6. **UI Rendering**: Verifies context card display

### Manual Testing Scenarios

1. **New User**: Create account → Access triage → Submit symptoms → View history
2. **Multi-Turn Chat**: Submit symptoms → Follow-up question → View session in history
3. **Severity Display**: Submit various symptoms → Verify severity colors match levels
4. **History Navigation**: View history → Click detail → Verify all fields displayed
5. **Error Cases**: Submit without API key → Verify graceful error handling

---

## Summary Tables

### Implementation Checklist

| User Story | Status | Key Files | Routes | Models |
|------------|--------|-----------|--------|--------|
| #2: Symptom Description → AI Diagnosis | ✅ Complete | `views.py`, `gemini_client.py`, `chat.html` | `/triage/chat/`, `/triage/chat/api/` | `TriageInteraction` |
| #4: Severity Levels | ✅ Complete | `chat.html`, `history.html`, `detail.html` | All triage routes | `TriageInteraction.severity` |
| #6: Triage History | ✅ Complete | `views.py`, `history.html`, `detail.html` | `/triage/history/`, `/triage/history/<id>/` | `TriageInteraction` |

### File Reference Quick Guide

| File | Purpose | Key Lines |
|------|---------|-----------|
| `triage/models.py` | Database model | 5-19 |
| `triage/views.py` | Backend logic | 21-156 |
| `triage/urls.py` | URL routing | 6-12 |
| `triage/admin.py` | Admin interface | 5-9 |
| `carelink/common/services/gemini_client.py` | AI integration | 65-286 |
| `templates/triage/chat.html` | Chat UI | 1-387 |
| `templates/triage/history.html` | History list | 1-124 |
| `templates/triage/detail.html` | Detail view | 1-222 |
| `tests/test_triage_chat.py` | Test suite | 1-159 |

---

## Conclusion

All three user stories (#2, #4, #6) are **fully implemented and functional**. The implementation provides:

- ✅ Complete AI-powered symptom assessment using Google Gemini
- ✅ Real-time chat interface with multi-turn conversation support
- ✅ Severity classification with visual indicators (color-coded badges)
- ✅ Comprehensive triage history with list and detail views
- ✅ Patient context integration for enhanced accuracy
- ✅ Robust error handling and fallback mechanisms
- ✅ Security measures (authentication, user isolation, CSRF protection)
- ✅ Admin interface for monitoring triage interactions
- ✅ Test coverage for critical paths

The codebase is production-ready for these features, with clear separation of concerns, reusable components, and comprehensive error handling.

