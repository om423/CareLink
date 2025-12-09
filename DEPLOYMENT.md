# CareLink Deployment Guide

Complete step-by-step guide to deploy the CareLink Django application from GitHub.

## Quick Start (TL;DR)

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/CareLink.git && cd CareLink

# 2. Set up virtual environment
python3 -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with your Gemini API key
echo "GEMINI_API_KEY=your-api-key-here" > .env
echo "DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" >> .env

# 5. Set up database
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` after starting the server.

---

## Prerequisites

Before starting, ensure you have:
- **Python 3.11+** installed (check with `python3 --version`)
- **Git** installed (check with `git --version`)
- **pip** (Python package manager)
- **Google Gemini API Key** (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))

---

## Step 1: Clone the Repository from GitHub

```bash
# Navigate to your desired directory
cd ~/projects  # or wherever you want the project

# Clone the repository
git clone https://github.com/YOUR_USERNAME/CareLink.git

# Navigate into the project directory
cd CareLink
```

**Note:** Replace `YOUR_USERNAME` with the actual GitHub username/organization.

---

## Step 2: Create a Python Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Verify activation (you should see (venv) in your terminal prompt)
which python3  # Should point to venv/bin/python3
```

---

## Step 3: Install Dependencies

```bash
# Make sure you're in the project root and venv is activated
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**Expected packages to install:**
- Django (web framework)
- django-environ (environment variables)
- whitenoise (static file serving)
- google-genai / google-generativeai (Gemini AI SDK)
- pytest, pytest-django (for testing, optional)

---

## Step 4: Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
# Option 1: Copy the example file and edit it
cp .env.example .env

# Option 2: Create manually
touch .env

# Edit the file (use nano, vim, or your preferred editor)
nano .env
```

Add the following content to `.env` (or copy from `.env.example` and update):

```env
# Google Gemini API Key (REQUIRED for AI features)
GEMINI_API_KEY=your-gemini-api-key-here

# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Optional: SSL settings for production
DJANGO_SECURE_SSL_REDIRECT=False
```

**Important:**
- Replace `your-gemini-api-key-here` with your actual Gemini API key
- Replace `your-secret-key-here-change-in-production` with a secure random string (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)

**Alternative:** You can also set environment variables directly:
```bash
export GEMINI_API_KEY="your-api-key-here"
export DJANGO_SECRET_KEY="your-secret-key-here"
```

---

## Step 5: Verify Django Settings

Check that the settings module is correctly configured:

```bash
# Verify Django can find settings
python manage.py check
```

If you see "System check identified no issues", you're good to go!

---

## Step 6: Set Up the Database

```bash
# Create database migrations (if needed)
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate
```

This will create the SQLite database file (`db.sqlite3`) with all necessary tables.

---

## Step 7: Create a Superuser (Admin Account)

```bash
# Create an admin user to access Django admin panel
python manage.py createsuperuser

# Follow the prompts:
# Username: admin
# Email address: admin@example.com
# Password: [choose a secure password]
# Password (again): [confirm]
```

---

## Step 8: Collect Static Files (For Production)

```bash
# Collect all static files into STATIC_ROOT
python manage.py collectstatic --noinput
```

**Note:** For development, this step is optional as Django serves static files automatically.

---

## Step 9: Verify Gemini API Key

Test that your Gemini API key is configured:

```bash
# Quick test (optional)
python -c "
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carelink.settings.dev')
application = get_wsgi_application()
from django.conf import settings
print('GEMINI_API_KEY configured:', bool(settings.GEMINI_API_KEY))
"
```

---

## Step 10: Run the Development Server

```bash
# Start the Django development server
python manage.py runserver

# Or specify a port
python manage.py runserver 8000
```

The server will start at `http://127.0.0.1:8000/`

**Verify it's working:**
- Visit `http://127.0.0.1:8000/healthz/` - should return `{"status": "ok"}`
- Visit `http://127.0.0.1:8000/` - should show the landing page
- Visit `http://127.0.0.1:8000/admin/` - should show the admin login

---

## Step 11: (Optional) Seed Test Data

To populate the database with test users:

```bash
# Create test users and admin account
python carelink/seed_users.py

# Or seed with fake medical data
python manage.py seed_fake_profiles
```

**Test Users Created:**
- Username: `ritwij ghosh`, `varsha kantheti`, `om patel`, `guilherme luvielmo`, `raphael lafeldt`
- Password: `password123`
- Admin: `admin` / `admin123`

---

## Step 12: Access the Application

### Public Pages
- **Landing Page**: `http://127.0.0.1:8000/`
- **Login**: `http://127.0.0.1:8000/accounts/login/`
- **Register**: `http://127.0.0.1:8000/accounts/register/`

### Admin Panel
- **Admin Dashboard**: `http://127.0.0.1:8000/admin/`
- **Platform Performance Dashboard**: `http://127.0.0.1:8000/admin/dashboard/`

### After Login (Patient)
- **Dashboard**: `http://127.0.0.1:8000/`
- **Triage Chat**: `http://127.0.0.1:8000/triage/chat/`
- **Appointment Booking**: `http://127.0.0.1:8000/appointments/book/`

---

## Production Deployment

For production deployment, follow these additional steps:

### 1. Update Production Settings

Edit `.env` file:
```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-production-secret-key-here
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SECURE_SSL_REDIRECT=True
```

### 2. Use Production Database (PostgreSQL recommended)

Install PostgreSQL and update `carelink/settings/base.py`:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}
```

### 3. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 4. Use Production Server (Gunicorn)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn carelink.wsgi:application --bind 0.0.0.0:8000
```

### 5. Set Up Process Manager (systemd/supervisor)

Create a systemd service file or use a process manager to keep the server running.

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'environ'"
**Solution:**
```bash
pip install django-environ
```

### Issue: "GEMINI_API_KEY not working"
**Solution:**
- Verify the API key is correct in `.env` file
- Check there are no extra spaces or quotes
- Ensure `.env` is in the project root directory
- Restart the server after changing `.env`

### Issue: "Port already in use"
**Solution:**
```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python manage.py runserver 8001
```

### Issue: "Database migration errors"
**Solution:**
```bash
# Delete old migrations (if safe to do so)
# Or reset database
rm db.sqlite3
python manage.py migrate
```

### Issue: "Static files not loading"
**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Ensure DEBUG=True for development
# Or configure proper static file serving for production
```

---

## Quick Deployment Checklist

- [ ] Repository cloned from GitHub
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with `GEMINI_API_KEY`
- [ ] Database migrations applied (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Server running (`python manage.py runserver`)
- [ ] Health check passing (`/healthz/` returns OK)
- [ ] Admin dashboard accessible (`/admin/dashboard/`)

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes* | None | Google Gemini API key for AI features |
| `DJANGO_SECRET_KEY` | Yes | Auto-generated | Django secret key for encryption |
| `DJANGO_DEBUG` | No | True | Enable/disable debug mode |
| `DJANGO_ALLOWED_HOSTS` | Yes | 127.0.0.1,localhost | Comma-separated list of allowed hosts |
| `DJANGO_SECURE_SSL_REDIRECT` | No | False | Force HTTPS in production |

*Required for AI triage features to work. App will run without it but show errors when using AI features.

---

## Support

For deployment issues:
1. Check the Django logs in the terminal
2. Verify all environment variables are set
3. Ensure all dependencies are installed
4. Check database connection and migrations
5. Review the troubleshooting section above

---

**Last Updated:** 2025-01-XX

