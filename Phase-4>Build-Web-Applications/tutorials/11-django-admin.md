# Tutorial 11 - Django Admin

## Why this matters

A founder may need to manage application data without you building a complete custom dashboard.

Django Admin provides a ready-made interface for registered models.

## 1. Register a model

Suppose:

```python
class Booking(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
```

In `admin.py`:

```python
from django.contrib import admin
from .models import Booking

admin.site.register(Booking)
```

The important line is:

```python
admin.site.register(Booking)
```

You are telling Django:

> Make this model available through the administration interface.

## 2. Create a superuser

Run:

```bash
python manage.py createsuperuser
```

Django asks for a username, email, and password.

When typing the password, the terminal does not show characters. That is normal.

## 3. Open Admin

Start:

```bash
python manage.py runserver
```

Visit:

```text
http://127.0.0.1:8000/admin/
```

Log in.

Your registered models should appear.

## 4. Where is the booking actually stored?

The admin is not the database.

The database stores the record.

The relationship is:

```text
Customer-facing application
          ↓
       Database
          ↑
       Admin
```

Both interfaces work with the same underlying data.

## 5. Why this is useful for an MWP

Imagine your application is a booking website.

Customers use:

```text
/services/
/book/
/contact/
```

The founder can use:

```text
/admin/
```

to manage:

```text
Bookings
Customers
Services
```

You can therefore create a useful internal workflow without first building a custom dashboard.

## 6. Admin is not the public application

Do not confuse:

```text
/admin/
```

with:

```text
/
/booking/
/products/
```

Admin is primarily for trusted administrators.

## 7. Customizing the list

You may later use:

```python
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "date",
    )
```

You may also encounter:

```python
list_filter
search_fields
ordering
```

These are conveniences for managing data.

Learn them when a project needs them.

## 8. Admin and permissions

Django supports users and permissions.

Not every user should necessarily be able to edit every record.

This becomes more important when authentication and authorization are introduced.

## 9. Exercise

In a booking project:

1. register `Booking`
2. create a superuser
3. start Django
4. open `/admin/`
5. create a booking through the public site
6. find it in Admin
7. edit it in Admin
8. refresh the public application

You should observe the same database record from two interfaces.

## 10. Using ChatGPT

Ask:

> I registered my Booking model in Django Admin. Explain why it appears there and how the model, admin, and database are connected.

Then:

> Show me how to make the booking list easier for an administrator to search, explaining each option before adding it.

## Remember

```text
             Database
             ↑      ↑
             │      │
       Application  Admin
```

One database can support multiple interfaces.
