# Tutorial 02 - Learn Enough SQL to Work With Your Data

## Phase 5 - Make Applications Real

### The big idea

Django's ORM allows you to work with data without writing SQL most of the time.

That is useful.

But a builder should also understand what is happening underneath.

The goal of this tutorial is **not** to turn you into a database administrator.

The goal is:

> **SQL should stop looking like mysterious database magic.**

The official Phase 5 project focuses on `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE`, and `ORDER BY`, with the outcome of being able to inspect and change application data. fileciteturn13file1L143-L170

---

# 1. What is SQL?

SQL stands for Structured Query Language.

It is a language used to communicate with relational databases.

You can think of SQL as a way of asking the database questions and giving it instructions.

```text
Python/Django
     ↓
ORM
     ↓
SQL
     ↓
Database
```

When you use:

```python
Product.objects.all()
```

Django handles the lower-level database communication for you.

SQL is what you should recognize when you look underneath.

---

# 2. SELECT means "show me data"

The simplest query:

```sql
SELECT * FROM products;
```

Read it approximately as:

> Select every column from the products table.

The `*` means all columns.

If the table contains:

```text
id | name      | price
---|-----------|------
1  | Laptop    | 50000
2  | Keyboard  | 2000
3  | Mouse     | 1000
```

the query returns all three records.

---

# 3. Select specific columns

You do not always need every column.

```sql
SELECT name, price
FROM products;
```

The result might be:

```text
name      | price
----------|------
Laptop    | 50000
Keyboard  | 2000
Mouse     | 1000
```

This teaches an important database habit:

> Ask for the information you actually need.

---

# 4. WHERE filters records

Suppose you want expensive products:

```sql
SELECT *
FROM products
WHERE price > 1000;
```

The database filters rows.

Conceptually:

```text
All products
     ↓
price > 1000
     ↓
Matching products
```

This is similar to filtering in Python.

---

# 5. Other comparisons

You may see:

```sql
WHERE price = 1000
```

```sql
WHERE price >= 1000
```

```sql
WHERE price < 1000
```

```sql
WHERE price <= 1000
```

```sql
WHERE name = 'Laptop'
```

The exact syntax matters, but the mental model is simple:

> `WHERE` decides which rows qualify.

---

# 6. AND and OR

You can combine conditions.

```sql
SELECT *
FROM products
WHERE price > 1000
AND name = 'Laptop';
```

Or:

```sql
SELECT *
FROM products
WHERE name = 'Laptop'
OR name = 'Keyboard';
```

Think of these as logical conditions.

---

# 7. ORDER BY

Suppose you want products sorted by price:

```sql
SELECT *
FROM products
ORDER BY price;
```

Ascending order is normally the default.

You can explicitly request:

```sql
ORDER BY price ASC;
```

For highest first:

```sql
ORDER BY price DESC;
```

The Phase 5 project specifically uses `ORDER BY` to introduce sorting. fileciteturn13file1L196-L204

---

# 8. INSERT creates a record

To add a row:

```sql
INSERT INTO products
(name, price)
VALUES
('Laptop', 50000);
```

Conceptually:

```text
SQL
 ↓
Database
 ↓
New row
```

Afterward:

```text
id | name   | price
---|--------|------
1  | Laptop | 50000
```

The database may generate the ID.

---

# 9. UPDATE changes data

Suppose the laptop price changes.

```sql
UPDATE products
SET price = 48000
WHERE id = 1;
```

The structure is:

```text
UPDATE table
SET column = value
WHERE record condition;
```

This is powerful.

It is also dangerous.

---

# 10. Why WHERE matters

Consider:

```sql
UPDATE products
SET price = 48000;
```

What does this mean?

It can mean:

> Set the price of every matching row - potentially every product - to 48000.

That is very different from:

```sql
UPDATE products
SET price = 48000
WHERE id = 1;
```

The second query targets one record.

This is why the Phase 5 project explicitly emphasizes the importance of the `WHERE` condition when using `UPDATE`. fileciteturn13file1L224-L235

---

# 11. DELETE removes data

Example:

```sql
DELETE FROM products
WHERE id = 3;
```

The record with ID 3 is removed.

Again:

```sql
DELETE FROM products;
```

can remove every row.

That is why destructive SQL should be treated carefully.

---

# 12. CRUD and SQL

You already learned CRUD in Phase 4.

SQL maps directly:

```text
CREATE → INSERT
READ   → SELECT
UPDATE → UPDATE
DELETE → DELETE
```

This is an important connection.

You are not learning a completely new concept.

You are learning another interface for the same data operations.

---

# 13. SQL vs Django ORM

The same conceptual operation may appear differently.

Django:

```python
Product.objects.all()
```

SQL:

```sql
SELECT * FROM products;
```

Django:

```python
Product.objects.filter(price__gt=1000)
```

SQL:

```sql
SELECT *
FROM products
WHERE price > 1000;
```

Django is giving you a Python-friendly abstraction over database operations.

---

# 14. Why learn SQL if Django hides it?

Because when something goes wrong, SQL knowledge helps you ask better questions.

For example:

> Is the database actually storing the record?

> Does the table contain any rows?

> Is my filter excluding records?

> Did my update affect one row or many?

You can understand database behavior even when Django is doing the SQL for you.

---

# 15. SQL exercise: inspect your application

Use your Phase 4/5 database.

Start with:

```sql
SELECT *
FROM your_table;
```

Then answer:

```text
How many records exist?

Which record is newest?

Which records match a particular condition?

Which records belong to a particular user?

Which values are unusually high or low?
```

The official project recommends questions of exactly this type as an exercise. fileciteturn13file1L247-L258

---

# 16. Think in questions

SQL becomes easier when you translate a business question into database logic.

Business question:

> Which products cost more than ₹10,000?

Translate:

```text
products
+
price > 10000
```

Then:

```sql
SELECT *
FROM products
WHERE price > 10000;
```

Business question:

> Show the cheapest products first.

Translate:

```sql
SELECT *
FROM products
ORDER BY price ASC;
```

---

# 17. NULL and missing information

You will eventually encounter:

```text
NULL
```

This means a value is absent/unknown rather than simply being the string `"NULL"`.

For example:

```text
phone = NULL
```

does not necessarily mean:

```text
phone = "NULL"
```

This distinction becomes important when filtering and validating data.

You do not need advanced SQL null theory yet.

Just remember:

> Missing data and ordinary values are different things.

---

# 18. SQL safety habit

Before running:

```sql
UPDATE ...
```

or:

```sql
DELETE ...
```

first run the corresponding `SELECT`.

For example, before:

```sql
DELETE FROM products
WHERE price < 100;
```

inspect:

```sql
SELECT *
FROM products
WHERE price < 100;
```

If the `SELECT` returns the records you intend to remove, then you understand the target.

This is a useful builder habit.

---

# 19. SQL exercise: translate ORM to SQL

Take these Django queries:

```python
Product.objects.all()
```

```python
Product.objects.filter(price__gt=1000)
```

```python
Product.objects.order_by("-price")
```

Write the equivalent SQL.

Then reverse the exercise.

Given:

```sql
SELECT *
FROM products
WHERE price > 1000
ORDER BY price DESC;
```

describe the query in plain English.

---

# 20. Common beginner mistakes

### Forgetting quotes around text

SQL text values commonly use quotes:

```sql
WHERE name = 'Laptop'
```

not:

```sql
WHERE name = Laptop
```

### Forgetting WHERE

Especially dangerous with:

```sql
UPDATE
DELETE
```

### Wrong table name

Django may generate table names that are not exactly what you expect.

Inspect the actual schema when unsure.

### Confusing database and model names

A Python model:

```python
class Product(models.Model):
```

is not necessarily identical in spelling to the physical database table.

Let Django's migration/schema tools tell you the actual structure.

---

# 21. Completion exercise

Create a small SQL notebook containing:

```sql
-- Read
SELECT ...

-- Filter
SELECT ...
WHERE ...

-- Sort
SELECT ...
ORDER BY ...

-- Insert
INSERT ...

-- Update
UPDATE ...
WHERE ...

-- Delete
DELETE ...
WHERE ...
```

For each query, write one sentence explaining what it does.

---

# 22. Using ChatGPT

Prompt:

> I know Django ORM but am new to SQL. Here is a Django queryset. Explain the SQL concept behind it and show an equivalent simple SQL query. Explain every clause.

For debugging:

> Here is the SQL query I intended to run and the result I got. Explain what the query actually asks the database to do. Do not change it until you explain it.

---

# Remember

```text
SELECT → read
INSERT → add
UPDATE → change
DELETE → remove

WHERE   → filter
ORDER BY → sort
```

The objective is not database mastery.

The objective is that when you see:

```sql
SELECT *
FROM bookings
WHERE user_id = 7;
```

you immediately understand:

> "Find the bookings belonging to user 7."
