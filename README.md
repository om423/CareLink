# CareLink — AI-Enhanced Telehealth Triage Platform

**Status:** Core features implemented with AI-powered triage, user onboarding, history tracking, and personalized dashboard.

## Overview

CareLink is a comprehensive telehealth triage platform that uses Google's Gemini AI to provide instant symptom assessments. The platform features a conversational AI chat interface, personalized patient profiles, and comprehensive health tracking.

## Quickstart

### 1. Environment Setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables
Set `GEMINI_API_KEY` in your environment for live AI functionality:
```bash
export GEMINI_API_KEY="your-api-key-here"
```
Or create a `.env` file in the project root:
```
GEMINI_API_KEY=your-api-key-here
```
*Without an API key, the app works but AI triage will show an error message.*

### 3. Database Setup
```bash
python manage.py migrate
```

### 4. (Optional) Seed Test Data
```bash
# Create 5 test users + admin
python carelink/seed_users.py

# OR seed with fake medical data
python manage.py seed_fake_profiles
```

**Test Users:**
- Username: `ritwij ghosh`, `varsha kantheti`, `om patel`, `guilherme luvielmo`, `raphael lafeldt`
- Password: `password123`
- Admin: `admin` / `admin123`

### 5. Run Server
```bash
python manage.py runserver
```
Visit `http://localhost:8000`

## Features

### 🤖 AI-Powered Triage Chat
- **Conversational Interface**: Real-time chat with AI health assistant
- **Context-Aware**: Considers patient's age, weight, allergies, and medical history
- **Multi-Turn Conversations**: AI remembers all messages in a session for comprehensive assessment
- **Instant Response**: User messages appear immediately with loading indicator
- **Severity Assessment**: Color-coded severity levels (Mild, Moderate, Severe, Critical)
- **Keyboard Shortcuts**:
  - Enter to send message
  - Shift+Enter for new line

**AI Output Includes:**
- Summary of symptoms
- Red flags to watch for
- Possible causes (differential diagnosis)
- Personalized advice
- Detailed rationale

### 👤 User Onboarding
- **First-Time User Flow**: Automatic redirect to onboarding on first login
- **Medical Profile Setup**: Collects age, weight, allergies, and medical history
- **Progressive UI**: Step-by-step process with clear instructions
- **Privacy Assurance**: Built-in messaging about data security

### 📊 Personalized Dashboard
**For Logged-In Users:**
- Welcome message with user's name
- Quick stats (total assessments, last assessment time, latest severity)
- Recent assessment cards (last 3 sessions)
- Profile summary sidebar
- Quick action buttons (Start Triage, View History, Find Care, Book Appointment)
- Profile completeness alerts
- Health tips and emergency contact

**For Logged-Out Users:**
- Marketing landing page with feature highlights

### 📜 Triage History
- **Session-Based Tracking**: Each chat appears as one entry (not per message)
- **Comprehensive View**: Shows full conversation context and final assessment
- **Detailed Reports**:
  - Complete symptom description
  - Severity assessment
  - AI recommendations
  - Red flags
  - Differential diagnosis
- **Print Support**: Print-friendly report format
- **Chronological Sorting**: Most recent sessions first

### 👥 User Profiles
- **Patient Information**: Age, weight, allergies, medical history
- **Profile Editing**: Update medical information anytime
- **Role Support**: Patient and Doctor/Admin roles
- **Data Persistence**: Securely stored for future triage sessions

## Project Structure

```
CareLink/
├── carelink/              # Django project root
│   ├── settings/          # Split settings (base, dev, prod)
│   ├── common/            # Shared services
│   │   └── services/
│   │       ├── gemini_client.py    # Gemini AI integration
│   │       ├── openai_client.py    # (Future) OpenAI integration
│   │       └── maps_client.py      # (Future) Maps integration
│   └── static/            # Project-level static files
├── templates/             # Global templates
│   ├── base.html          # Base template
│   ├── home/
│   │   ├── dashboard.html # Logged-in user dashboard
│   │   └── landing.html   # Marketing page
│   └── triage/
│       ├── chat.html      # AI chat interface
│       ├── history.html   # Triage history list
│       └── detail.html    # Individual assessment view
├── home/                  # Home app
├── accounts/              # Authentication
├── profiles/              # User profiles
│   ├── models.py          # PatientProfile model
│   ├── views.py           # Onboarding & profile editing
│   └── templates/
│       └── onboarding.html
├── triage/                # AI triage system
│   ├── models.py          # TriageInteraction model
│   ├── views.py           # Chat, history, detail views
│   └── urls.py
├── doctors/               # Doctor listings (future)
├── appointments/          # Appointment booking (future)
└── tests/                 # Test suite
    ├── test_triage_chat.py
    └── test_routes_smoke.py
```

## Key Technologies

- **Backend**: Django 5.1, Python 3.13
- **Database**: SQLite (dev), PostgreSQL (prod-ready)
- **AI**: Google Gemini 2.0 Flash (with fallback models)
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Testing**: Pytest, pytest-django, factory_boy
- **Code Quality**: Black, isort, Flake8, djLint
- **Security**: CSRF protection, HIPAA-compliant practices

## API Endpoints

### Health Checks
- `GET /healthz/` - Health check
- `GET /readyz/` - Readiness check

### Authentication
- `POST /accounts/login/` - User login
- `POST /accounts/register/` - User registration
- `POST /accounts/logout/` - User logout

### Triage
- `GET /triage/chat/` - AI chat interface
- `POST /triage/chat/api/` - Submit symptoms (AJAX)
- `GET /triage/history/` - View triage history
- `GET /triage/history/<id>/` - View specific assessment

### Profiles
- `GET /profiles/onboarding/` - First-time user onboarding
- `GET /profiles/edit/` - Edit profile

## Development

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_triage_chat.py

# Run with coverage
coverage run -m pytest
coverage report
```

### Code Formatting
```bash
# Format Python code
black .
isort .

# Lint Python code
flake8

# Format Django templates
djlint templates --reformat

# Run all pre-commit hooks
pre-commit run --all-files
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View migration status
python manage.py showmigrations
```

## Configuration

### Settings Files
- `carelink/settings/base.py` - Common settings
- `carelink/settings/dev.py` - Development settings (default)
- `carelink/settings/prod.py` - Production settings

### Environment Variables
- `GEMINI_API_KEY` - Google Gemini API key (required for AI features)
- `DJANGO_SECRET_KEY` - Django secret key
- `DJANGO_DEBUG` - Debug mode (default: True)
- `DJANGO_ALLOWED_HOSTS` - Allowed hosts (comma-separated)

## Key Features Implementation Details

### Session-Based Triage History
- Each chat session generates a unique `session_id`
- Multiple messages in one chat update the same database record
- History shows one entry per chat session (not per message)
- Final assessment reflects all symptoms discussed

### Conversation Context
- Frontend tracks full conversation history
- All previous messages sent with each new request
- AI considers entire conversation for comprehensive assessment
- Symptoms concatenated with "Additional information:" separator

### Patient Context Integration
- AI receives patient's age, weight, allergies, and medical history
- Influences severity assessment and recommendations
- Privacy-conscious: only sends relevant medical data
- Gracefully handles missing profile information

## Testing

### Test Coverage
- Triage chat functionality with monkeypatched Gemini client
- Route smoke tests for all major endpoints
- JSON parsing and repair flows
- Error handling and retry logic
- Patient context integration

### Running Tests Without API Key
Tests use monkeypatching to avoid network calls:
```python
def test_triage_chat_post_monkeypatched(client, monkeypatch):
    # Tests run without GEMINI_API_KEY
    pass
```

## Production Considerations

### Security
- CSRF protection enabled
- SQL injection prevention via ORM
- XSS prevention with template escaping
- User authentication required for sensitive endpoints
- Session-based user isolation

### Performance
- Database query optimization with aggregation
- Efficient session grouping (no N+1 queries)
- Static file serving via WhiteNoise
- Response caching for static assets

### Scalability
- Stateless architecture (session ID on client)
- PostgreSQL-ready for production
- CDN-ready static file structure
- Horizontal scaling possible

## Future Enhancements

- [ ] Doctor search and profiles
- [ ] Appointment booking system
- [ ] Telemedicine video calls
- [ ] Prescription management
- [ ] Health metrics tracking
- [ ] Integration with wearable devices
- [ ] Multi-language support
- [ ] Mobile app (React Native)

## Contributing

1. Follow the code style (Black, isort, Flake8)
2. Write tests for new features
3. Update documentation
4. Run pre-commit hooks before committing

## License

[Your License Here]

## Support

For issues or questions, contact the development team or file an issue in the repository.

---

**Built with ❤️ for better healthcare access**
