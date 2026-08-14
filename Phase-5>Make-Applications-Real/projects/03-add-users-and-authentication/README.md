# Project 3 - Add Users and Authentication

This is a small multi-user Django application.

## Run

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `/register/` to create an account.

Then use:

```text
/login/
/
 /logout/
```

## What to explore

- `accounts/forms.py` - registration form
- `accounts/views.py` - registration and protected application flow
- `accounts/urls.py` - routes
- `app/models.py` - user-owned records
- `app/views.py` - filtering records for the logged-in user

The important security lesson is that the server filters data by the authenticated user. Do not rely on hiding links in the browser.
