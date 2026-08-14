# Tutorial 10 - Django Models and Migrations

## Why this matters

Applications need to remember information.

A booking application remembers bookings. An inventory application remembers products. A CRM remembers customers.

Django models describe this data in Python.

## 1. A model

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
```

This describes a product record.

Conceptually:

```text
Product
 ├── name
 └── price
```

## 2. Common fields

You will commonly encounter:

```python
models.CharField()
models.TextField()
models.IntegerField()
models.DecimalField()
models.BooleanField()
models.DateField()
models.DateTimeField()
models.EmailField()
```

For example:

```python
class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    confirmed = models.BooleanField(default=False)
```

## 3. The database connection

A relational database stores records in tables.

Your model:

```python
class Product(models.Model):
    name = ...
    price = ...
```

corresponds conceptually to:

```text
product table

id | name     | price
---|----------|------
1  | Laptop   | 50000
2  | Mouse    | 1000
```

Django's ORM lets you work with these records using Python.

## 4. What is a migration?

Changing `models.py` does not automatically change the database.

Suppose you add:

```python
description = models.TextField()
```

Your Python model now expects a new field.

The database also needs a structural change.

Migrations are Django's mechanism for recording and applying those changes.

## 5. Creating migrations

Run:

```bash
python manage.py makemigrations
```

Django examines your models and creates a migration file.

You might see:

```text
Migrations for 'main':
  main/migrations/0002_add_description.py
```

## 6. Applying migrations

Then:

```bash
python manage.py migrate
```

Think:

```text
makemigrations
 ↓
Create instructions

migrate
 ↓
Apply instructions
```

## 7. Why you might see "no such table"

Suppose your code executes:

```python
Product.objects.all()
```

and Django reports:

```text
django.db.utils.OperationalError:
no such table: main_product
```

The likely situation is:

```text
Python model exists
        ↓
Database table does not
```

Check:

```bash
python manage.py showmigrations
```

Then:

```bash
python manage.py migrate
```

If you changed a model:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 8. Creating records

```python
Product.objects.create(
    name="Mouse",
    price=1000,
)
```

## 9. Reading records

All:

```python
Product.objects.all()
```

One:

```python
Product.objects.get(id=1)
```

Filtered:

```python
Product.objects.filter(price__gt=1000)
```

This is Django's ORM.

## 10. Updating

```python
product = Product.objects.get(id=1)
product.price = 1200
product.save()
```

The `save()` writes the change to the database.

## 11. Deleting

```python
product.delete()
```

Deletion should be treated carefully because data can be lost.

## 12. Migrations and Git

Migration files normally belong in Git:

```text
main/migrations/
    0001_initial.py
    0002_add_description.py
```

They describe database changes.

The local database itself should generally not be treated as source code.

## 13. Exercise

Create:

```python
class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
```

Then:

```bash
python manage.py makemigrations
python manage.py migrate
```

Register it in Admin.

Create a record.

Display it through a view and template.

Trace:

```text
Model
 ↓
Migration
 ↓
Database
 ↓
Admin
 ↓
View
 ↓
Template
```

## 14. Using ChatGPT

If migrations fail, provide the exact error, `models.py`, migration output, and `showmigrations` output.

Ask:

> Explain why my Django model and database schema are out of sync and give me the smallest safe fix.

Do not delete migrations or databases just because an AI suggests it without explaining why.

## Remember

```text
models.py
 ↓
makemigrations
 ↓
migration files
 ↓
migrate
 ↓
database schema
```

Models describe data. Migrations keep database structure synchronized with those models.
