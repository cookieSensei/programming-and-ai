# Tutorial 05 — Django Fundamentals

## Why This Matters

Django has many files; beginners only need a small core mental model.

## Project and App

A project is the overall Django configuration. An app is a component that handles a particular area of functionality.

```text
Project
├── accounts
├── bookings
└── products
```

## Important Files

```text
manage.py    → Django commands
settings.py  → configuration
urls.py      → URL routing
views.py     → request logic
models.py    → persistent data
templates/   → HTML
admin.py     → Django Admin configuration
```

## Core Flow

```text
URL
 ↓
View
 ↓
Model / logic
 ↓
Template
 ↓
Browser
```

## Do Not Learn Everything

You can postpone advanced class-based views, middleware internals, signals, APIs, and custom authentication. Learn them only when a project needs them.

## Try It

Open a Phase 4 project and locate its URLs, views, templates, models, and admin configuration.

## Using ChatGPT

Ask: **“Explain how a request to /bookings/ travels through my Django project. Don't rewrite the code.”**
