# CareLink - AI-Enhanced Telehealth Triage Platform

A Django-based telehealth platform that provides users with intelligent medical triage and streamlined access to healthcare professionals. CareLink combines OpenAI's language capabilities with Google Maps' geolocation features to enable patients to describe symptoms naturally, receive AI-generated assessments, and locate nearby medical providers.

## Project Structure

```
carelink/
├── carelink/           # Main Django project directory
│   ├── templates/      # Base templates
│   └── static/         # Static files (CSS, JS, images)
├── home/              # Landing page
├── accounts/          # User authentication
├── profiles/          # Patient and doctor profiles
├── triage/            # AI-powered triage system
├── doctors/            # Doctor management and dashboard
├── appointments/      # Appointment scheduling
└── db.sqlite3         # SQLite database
```

## Features (Planned)

### Patient Features
- Personal profile with medical history
- AI-powered symptom assessment
- Nearby clinic/doctor location on map
- Severity level estimation
- Online appointment booking
- Triage history tracking

### Doctor/Admin Features
- Triage report review
- Professional notes and feedback
- Availability management
- Clinic information management
- Platform performance monitoring

## Technology Stack

- **Backend**: Django 5.0
- **Database**: SQLite
- **Frontend**: Bootstrap 5.3.3 with custom medical-themed CSS
- **Icons**: FontAwesome
- **APIs**: OpenAI API, Google Maps API

## Getting Started

### Prerequisites

- Python 3.x
- Django 5.0

### Installation

1. Navigate to the project directory:
   ```bash
   cd "CareLink - 2340 Optional Project"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000/` in your browser

## Environment Variables

For production, set the following environment variables:

```bash
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

## Development Commands

### Database Operations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Development Tools
```bash
# Start development server
python manage.py runserver

# Access Django shell for debugging
python manage.py shell
```

## Current Status

This project is in initial setup phase. The basic Django structure is in place with all apps scaffolded. Implementation of models, views, and business logic is pending.

## Design Theme

The application uses a medical-themed color palette:
- Medical Blue (#0d6efd) - Primary actions
- Trust Teal (#2d9cdb) - Information and trust
- Healing Green (#27ae60) - Success and positive actions
- Warning Amber (#ff9800) - Important notices
- Urgent Red (#e74c3c) - Critical alerts

## Contributing

This is a CS 2340 optional project. Please follow Django best practices when contributing.

