# Tutorial 14 — Understanding CRUD

## Why This Matters

Many business applications are variations of managing information.

## CRUD

```text
Create
Read
Update
Delete
```

## Example

For products:

```text
Create → add product
Read   → list products
Update → edit product
Delete → remove product
```

## Django Mapping

```text
Create → Form → Model → Database
Read   → Queryset → Template
Update → Form → Model → Database
Delete → Model → Database
```

## Entrepreneurial Connection

Bookings, inventory, contacts, expenses, tasks, orders, and listings often share the same CRUD pattern even though their business purposes differ.

## Try It

Take a project and identify what the user can create, read, update, and delete.

## Using ChatGPT

Ask: **“Map the CRUD operations in my application to the Django views, forms, models, and templates.”**
