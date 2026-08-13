# Project 1 — Give Your Application a Database

This project makes database persistence explicit.

## Run

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open the local URL shown by Django.

## What to inspect

- `inventory/models.py` — Django model
- `inventory/admin.py` — admin registration
- `inventory/management/commands/seed_products.py` — sample data
- `db.sqlite3` — local database created by Django

The application demonstrates the relationship:

```text
Django Model
     ↓
Database Table
     ↓
Stored Rows
```

The next project will use SQL to inspect this database directly.
