# Project 6 — Build Your Minimum Working Product

This is the final reference implementation for Phase 5.

It is a small service-booking application that demonstrates the minimum pieces a student may need to put an idea in front of real users:

```text
User
 ↓
Service
 ↓
Booking
 ↓
Confirmation
```

## Features

- User registration and login
- Service list
- Service detail
- Booking form
- User-specific bookings
- SQLite for local development
- Environment-based configuration
- Static files
- Gunicorn-ready deployment configuration

## Local setup

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_services
python manage.py runserver
```

Open `/register/` to create an account.

## Teaching note

This is a reference MWP, not a complete production product.

Students should change the problem, user journey, content, and data model for their own idea.
