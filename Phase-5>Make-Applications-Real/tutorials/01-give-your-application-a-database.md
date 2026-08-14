# Tutorial 01 — Give Your Application a Database

## Phase 5 — Make Applications Real

### The big idea

In Phase 4, you learned how a Django application can accept input, process it, and work with models.

Phase 5 asks a more practical question:

> **Where does the application remember information after the request is over?**

The answer is a database.

A database gives an application persistent memory.

```text
User
  ↓
Web application
  ↓
Database
  ↓
Stored information
```

If a user creates a booking today, you expect that booking to still exist tomorrow. If a founder adds a product, the product should still be there when the application restarts.

That is what persistence means.

The official Phase 5 project defines the outcome as understanding how application data is stored persistently and connects Django models to real database structures. fileciteturn13file0L11-L31

---

# 1. Memory vs persistence

Imagine a Python program:

```python
name = "Alice"
print(name)
```

While the program is running, Python knows:

```text
name → Alice
```

But if the program exits, that variable disappears.

A database solves a different problem.

```text
Application
     ↓
Database
     ↓
Permanent record
```

The application can stop.

The computer can restart.

The user can return later.

The information can still exist.

---

# 2. What is a database?

A database is a system for storing and retrieving structured information.

For a product application, you might need:

```text
Product
    name
    price
    description
    quantity
```

For a booking application:

```text
Booking
    customer
    service
    date
    time
    status
```

For an expense application:

```text
Expense
    description
    amount
    category
    date
    owner
```

The database stores these records.

---

# 3. Tables

A relational database organizes information into tables.

Think of a table as a structured collection of records.

Example:

```text
products

id | name      | price
---|-----------|------
1  | Laptop    | 50000
2  | Keyboard  | 2000
3  | Mouse     | 1000
```

Each row is a record.

Each column represents a piece of information about that record.

---

# 4. Rows

A row represents one record.

```text
1 | Laptop | 50000
```

means:

```text
Product
id     = 1
name   = Laptop
price  = 50000
```

Another row:

```text
2 | Keyboard | 2000
```

represents a different product.

---

# 5. Columns

A column describes one property.

```text
id
name
price
```

The `name` column contains product names.

The `price` column contains prices.

The `id` column identifies records.

This gives us:

```text
Table
 ├── columns → structure
 └── rows    → records
```

---

# 6. Primary keys

Most database tables need a way to distinguish one record from another.

Consider:

```text
name
------
Laptop
Laptop
Laptop
```

Names may not be unique.

Instead, a database can assign:

```text
id
--
1
2
3
```

Now each record has an identity.

A primary key is a field used to uniquely identify a record.

Django commonly provides an automatically managed primary key when you create a model.

---

# 7. Why IDs matter

Suppose you have:

```text
Product 1 → Laptop
Product 2 → Keyboard
Product 3 → Mouse
```

A URL might be:

```text
/products/2/
```

Django can use `2` to find the corresponding record.

Conceptually:

```text
/products/2/
       ↓
id = 2
       ↓
Keyboard
```

This is why database identity connects directly to web application URLs.

---

# 8. Records are application objects

A record is one stored instance of something.

For example:

```text
Booking #17
Customer: Sarah
Date: 2026-08-20
Service: Consultation
```

The application can retrieve it later.

The database does not inherently know that this is a "booking website." It stores structured information. Your application gives that information meaning.

---

# 9. Relationships

Real applications rarely have only one kind of data.

A booking application may have:

```text
Customer
Service
Booking
```

A booking connects these pieces:

```text
Customer
   ↓
Booking
   ↓
Service
```

For example:

```text
Sarah
  ↓
Booking #27
  ↓
Business Consultation
```

The relationship is important because you do not want to copy all customer information into every booking unnecessarily.

---

# 10. One-to-many thinking

A common relationship is:

```text
One customer
     ↓
Many bookings
```

For example:

```text
Sarah
 ├── Booking 1
 ├── Booking 8
 └── Booking 14
```

This is conceptually a one-to-many relationship.

You do not need advanced database theory yet.

Ask:

> Which thing belongs to which other thing?

That question will help you design relationships.

---

# 11. Django models are the application-level description

In Django, you might write:

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
```

This is Python code.

But it describes data that ultimately needs to live in a database.

Conceptually:

```text
Django Model
     ↓
Database Table
```

The model describes the structure Django expects.

---

# 12. The ORM

Django provides an ORM: Object-Relational Mapper.

This lets you interact with database records using Python-style code.

For example:

```python
Product.objects.all()
```

means:

> Give me the products.

You do not have to write raw SQL for every normal operation.

The ORM translates your request into database operations.

---

# 13. Creating a record

You can create a product:

```python
Product.objects.create(
    name="Laptop",
    price=50000,
)
```

Conceptually:

```text
Python
 ↓
Django ORM
 ↓
Database
 ↓
New row
```

---

# 14. Reading records

To retrieve all products:

```python
products = Product.objects.all()
```

Then perhaps:

```python
for product in products:
    print(product.name)
```

The database is being used as persistent storage behind the scenes.

---

# 15. Updating a record

Suppose:

```python
product = Product.objects.get(id=1)
```

Then:

```python
product.price = 48000
product.save()
```

The database changes from:

```text
Laptop | 50000
```

to:

```text
Laptop | 48000
```

---

# 16. Deleting a record

You can delete:

```python
product.delete()
```

But deletion is destructive.

Before adding delete functionality to a real product, ask:

> Should this information actually disappear, or should it be marked inactive?

For many applications, "archive" or "inactive" may be safer than permanent deletion.

---

# 17. Your Phase 4 application

Do not invent a completely unrelated example.

Return to your Phase 4 project.

Ask:

> **What information does my application need to remember?**

Write it down.

For example:

```text
Application: Appointment Booker

Needs to remember:

Customer
Service
Appointment date
Appointment time
Booking status
```

Then turn that into data structures.

```text
Customer
Service
Booking
```

---

# 18. Database design exercise

Create this table:

```text
My application:

What does the user create?
____________________________

What does the application need to remember?
____________________________

What information belongs together?
____________________________

What should have its own table?
____________________________
```

Then draw:

```text
Application
     ↓
Data
     ↓
Tables
     ↓
Relationships
```

---

# 19. Inspect the actual database

This is an important Phase 5 habit.

Do not only look at:

```text
models.py
```

Look at the actual database.

You should be able to answer:

> Does my Django model actually correspond to stored database data?

For a simple SQLite development project, you may have:

```text
db.sqlite3
```

You can inspect it with a database viewer or SQLite tooling.

The purpose is not to become a database administrator.

The purpose is to remove the mystery.

---

# 20. Models, migrations, and database

The relationship is:

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

If you change:

```python
class Product(models.Model):
    name = ...
```

to:

```python
class Product(models.Model):
    name = ...
    description = ...
```

the database schema needs to change too.

That is what migrations handle.

---

# 21. Common beginner confusion

### "I created a model, so why is the database empty?"

Because a model describes structure.

It does not automatically mean records have been created.

You may need:

```python
Product.objects.create(...)
```

or Django Admin or another input flow.

### "I have a table, so why can't my view find data?"

Possible reasons include:

- wrong query
- empty table
- wrong database
- migrations not applied
- wrong model
- filtering too aggressively

Debug the data path.

---

# 22. The complete mental model

At the end of this tutorial, think:

```text
User
 ↓
Django application
 ↓
Model / ORM
 ↓
Database
 ↓
Table
 ↓
Row
```

And in the opposite direction:

```text
Database
 ↓
ORM
 ↓
Django view
 ↓
Template
 ↓
User
```

---

# 23. Completion exercise

For your own application, write:

```text
Application:
________________________

Table 1:
________________________

Columns:
________________________

Table 2:
________________________

Columns:
________________________

Relationships:
________________________
```

Then explain your design aloud.

If you can explain what your application remembers and why, you have completed the core objective.

---

# 24. Using ChatGPT

Use AI as an architecture assistant.

Prompt:

> Here is my Phase 4 Django application and its models. I am entering Phase 5. Explain what information the application currently stores, what database tables Django will create, and what relationships exist. Do not redesign the application.

Then ask:

> Identify the minimum database structure needed for the core user journey. Explain why each field exists.

Do not ask AI to create a giant database schema before you understand the problem.

---

# Remember

The most important sentence is:

> **A database stores the information my application needs to remember.**

And:

> **A Django model describes the data my application works with.**

The official Phase 5 sequence deliberately moves from this database mental model into SQL, where you learn to work with the stored data directly. fileciteturn13file0L121-L133
