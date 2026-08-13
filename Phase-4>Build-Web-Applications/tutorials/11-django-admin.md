# Tutorial 11 — Django Admin

## Why This Matters

Django Admin gives beginners a powerful way to inspect and manage application data.

## Register a Model

```python
from django.contrib import admin
from .models import Booking

admin.site.register(Booking)
```

## Create an Admin User

```bash
python manage.py createsuperuser
```

Then visit `/admin/` after starting the development server.

## What Is Happening?

```text
Booking model
     ↓
admin.site.register()
     ↓
Django Admin
     ↓
Manage records
```

The database stores the booking. Admin is an interface for managing it.

## Try It

Create a booking through your application. Open `/admin/` and find the same booking.

## Using ChatGPT

Ask: **“Why does registering my Django model in admin.py make it appear in /admin/? Explain the connection between model, database, and admin.”**
