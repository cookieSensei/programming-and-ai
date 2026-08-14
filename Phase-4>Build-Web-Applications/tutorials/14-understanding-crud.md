# Tutorial 14 — Understanding CRUD

## Why this tutorial exists

Many business applications are fundamentally about managing information.

CRUD gives you a simple vocabulary:

```text
Create
Read
Update
Delete
```

## 1. Create

Create means adding a new record.

Example:

```text
Customer submits booking
        ↓
New Booking record
```

## 2. Read

Read means retrieving information.

Examples:

```text
Show products
Show one booking
Show my bookings
Search customers
```

Django:

```python
Product.objects.all()
```

is a read operation.

## 3. Update

Update changes an existing record.

```text
Booking
status = pending

      ↓

status = confirmed
```

Django:

```python
booking.status = "confirmed"
booking.save()
```

## 4. Delete

Delete removes information:

```python
booking.delete()
```

Treat deletion carefully because it can be irreversible.

## 5. CRUD and Django

A typical mapping is:

```text
CREATE
 ↓
Form
 ↓
View
 ↓
Model
 ↓
Database

READ
 ↓
View
 ↓
Queryset
 ↓
Template

UPDATE
 ↓
Form
 ↓
View
 ↓
Model
 ↓
Database

DELETE
 ↓
View
 ↓
Model
 ↓
Database
```

## 6. CRUD is not the business idea

A restaurant booking app and an inventory app can have completely different business purposes.

Yet both may need:

```text
Create
Read
Update
Delete
```

The technical pattern is reusable.

## 7. CRUD and MWP thinking

Suppose your idea is:

> A marketplace for local tutors.

A first version might only need:

```text
Create tutor profile
Read tutor profiles
Update tutor profile
Delete tutor profile
```

Then perhaps:

```text
Customer sends inquiry
```

You may deliberately leave out:

```text
payments
AI recommendations
analytics
mobile app
notifications
```

## 8. Not every application needs all four

A contact form might need:

```text
Create message
Read message in Admin
```

Users may never update or delete their messages.

CRUD is a thinking tool, not a mandatory checklist.

## 9. CRUD and URLs

A project might use routes such as:

```text
/products/
       ↓
list

/products/create/
       ↓
create

/products/5/
       ↓
detail

/products/5/edit/
       ↓
update

/products/5/delete/
       ↓
delete
```

The exact design can vary.

## 10. CRUD and security

Once authentication exists, you must ask:

> Who is allowed to perform this operation?

For example:

```text
User A
 ↓
Delete User B's booking
```

should not automatically be allowed.

Server-side permissions become important.

## 11. Exercise

Take one Phase 4 project.

Write:

```text
Main record:
__________

Create:
__________

Read:
__________

Update:
__________

Delete:
__________
```

Then decide which operations are actually necessary.

## 12. Using ChatGPT

Ask:

> Map the CRUD operations in this Django application to its URLs, views, forms, models, templates, and database operations.

## Remember

```text
Create → add
Read   → retrieve
Update → change
Delete → remove
```

When you encounter a new business idea, ask:

> What information does the application manage, and what does the user need to do with it?
