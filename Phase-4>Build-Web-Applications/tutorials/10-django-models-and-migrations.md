# Tutorial 10 — Django Models and Migrations

## Why This Matters

Models describe persistent application data; migrations apply structural changes to the database.

## Model

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

## Mental Model

```text
Python Model
     ↓
Migration
     ↓
Database Table
```

## Commands

Create migration files:

```bash
python manage.py makemigrations
```

Apply them:

```bash
python manage.py migrate
```

## Why Two Commands?

`makemigrations` records the change you want. `migrate` applies that change to the database.

## Common Error

If you see:

```text
no such table: main_product
```

check migrations:

```bash
python manage.py showmigrations
python manage.py migrate
```

If you changed a model, use `makemigrations` first.

## Using ChatGPT

Provide the exact migration error, `models.py`, and migration output. Ask ChatGPT to explain the root cause before giving a fix.
