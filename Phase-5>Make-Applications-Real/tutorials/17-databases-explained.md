# Tutorial 17 — Databases Explained

## Why This Matters

A database gives an application persistent memory.

## Mental Model

Without a database, information held only in memory can disappear when the process stops.

```text
Application
   ↓
Database
   ↓
Stored information
```

## Tables

A relational database uses tables:

```text
products

id | name     | price
---|----------|------
1  | Laptop   | 50000
2  | Keyboard | 2000
```

## Rows, Columns and IDs

A row is one record. A column describes one property. An `id` commonly identifies a record uniquely.

## Relationships

Applications connect information:

```text
Customer
   ↓
Booking
   ↓
Service
```

## Django Models

A Django model is a Python representation of application data. Django uses it to work with the underlying database.

## Try It

For your MWP, list what information it must remember, what tables could represent that information, and what identifies each record.
