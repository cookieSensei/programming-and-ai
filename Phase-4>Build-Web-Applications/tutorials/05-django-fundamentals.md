# Tutorial 05 — Django Fundamentals

## Why this matters

A new Django project can look intimidating because it creates many files.

You do **not** need to understand everything before you build.

For Phase 4, learn the small set of concepts you will repeatedly use.

## 1. What is Django?

Django is a Python web framework.

A framework provides reusable structure and tools for common application tasks.

Django provides systems for:

- URL routing
- request handling
- templates
- forms
- database models
- migrations
- authentication
- administration
- security features

You decide what your application should do. Django provides infrastructure that helps you implement it.

## 2. Project vs app

A Django **project** is the overall website/application configuration.

A Django **app** is a component responsible for an area of functionality.

For example:

```text
Project
├── accounts
├── bookings
└── products
```

A small MWP may have only one app.

Do not worry if different projects organize apps differently.

## 3. `manage.py`

This is the command center for a Django project.

Start the development server:

```bash
python manage.py runserver
```

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

## 4. `settings.py`

This contains configuration.

You will encounter:

```python
INSTALLED_APPS
DATABASES
STATIC_URL
DEBUG
ALLOWED_HOSTS
SECRET_KEY
```

Do not memorize every setting.

Instead ask:

> What part of Django does this setting configure?

## 5. `urls.py`

URL configuration connects browser addresses to Python code.

```python
urlpatterns = [
    path("", home),
    path("about/", about),
]
```

This creates:

```text
/        → home()
/about/  → about()
```

## 6. `views.py`

A view is Python code that handles a request.

```python
def home(request):
    return render(request, "main/home.html")
```

A view may:

- retrieve records
- validate input
- create records
- update records
- delete records
- choose a template
- redirect users

Think:

> A view is the Python code that decides how to respond to a request.

## 7. `models.py`

Models describe application data.

```python
class Booking(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
```

Django uses this model to work with database records.

## 8. `templates/`

Templates contain HTML plus Django template syntax.

```django
<h1>{{ booking.name }}</h1>
```

They are where server-side data becomes a browser page.

## 9. `admin.py`

This configures Django Admin.

```python
from django.contrib import admin
from .models import Booking

admin.site.register(Booking)
```

Now the model can be managed through `/admin/`.

## 10. The complete request flow

For:

```text
/bookings/
```

a simplified request is:

```text
Browser
   ↓
URL
   ↓
urls.py
   ↓
view
   ↓
model/database
   ↓
template
   ↓
HTML
   ↓
Browser
```

Not every request uses every step.

For example, a simple static response may not need a database.

## 11. What not to learn yet

You can postpone:

- advanced class-based views
- middleware internals
- Django REST Framework
- advanced ORM optimization
- custom authentication architecture
- asynchronous internals

Learn advanced features when a real project needs them.

## 12. Exercise

Open a Phase 4 project and locate:

```text
manage.py
settings.py
urls.py
views.py
models.py
templates/
static/
admin.py
```

Write one sentence describing each.

## 13. Using ChatGPT

Ask:

> I know Python but am new to Django. Here is my project structure. Explain what each important file does and then trace a request to `/bookings/`. Do not rewrite anything.

## Remember

The architecture matters more than memorizing files:

```text
URL
 ↓
View
 ↓
Model / business logic
 ↓
Template
 ↓
Browser
```
