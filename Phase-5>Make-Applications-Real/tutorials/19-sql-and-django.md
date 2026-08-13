# Tutorial 19 — SQL and Django

## Why This Matters

Students should understand that Django's ORM sits between Python code and the database.

## The Layers

```text
Django code
   ↓
Django ORM
   ↓
SQL
   ↓
Database
```

## Examples

```python
Product.objects.all()
```

Conceptually represents a read query.

```python
Product.objects.filter(price__gt=1000)
```

Conceptually represents filtering by price.

## Creating Data

```python
Product.objects.create(
    name="Mouse",
    price=1000,
)
```

Conceptually corresponds to an `INSERT` operation.

## Why Learn SQL?

The ORM lets you work in Python. SQL knowledge helps you understand what the database is doing and diagnose data problems.

## Try It

Take a Django queryset from your project and describe what database operation it represents.
