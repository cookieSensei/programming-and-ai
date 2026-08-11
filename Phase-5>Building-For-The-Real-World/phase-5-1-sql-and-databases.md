# 1. SQL & Databases

## Teaching Our Application to Remember

In the previous section, we discovered a problem.

Our applications can process information, but if we only keep that information in Python memory, it disappears when the program stops.

We need persistent storage.

That leads us to:

```text
Database
```

And to communicate with a relational database, we use:

```text
SQL
```

---

# 1. What Is SQL?

SQL stands for:

> **Structured Query Language**

It is a language used to work with relational databases.

With SQL, we can ask a database to:

```text
Create data
Read data
Update data
Delete data
```

These operations are often summarized as:

```text
CRUD
```

---

# 2. What Is a Relational Database?

A relational database stores information in tables.

Imagine a spreadsheet:

```text
users

id    name      email
1     Alice     alice@example.com
2     Bob       bob@example.com
3     Carol     carol@example.com
```

A database table looks conceptually similar.

But a database provides much more powerful ways to:

```text
Search
Filter
Connect tables
Update records
Control access
```

---

# 3. Table, Row, and Column

A table contains:

```text
Columns
```

and:

```text
Rows
```

For example:

```text
users
────────────────────────────────
id | name  | email
────────────────────────────────
1  | Alice | alice@example.com
2  | Bob   | bob@example.com
```

Here:

```text
id
name
email
```

are columns.

Each user record is a row.

---

# 4. Creating a Table

We can create a table using:

```sql
CREATE TABLE users (
    id INTEGER,
    name TEXT,
    email TEXT
);
```

Read this almost like English:

```text
Create a table called users.

The table has:
    an integer id
    a text name
    a text email
```

SQL becomes much easier once you learn to read it this way.

---

# 5. Data Types

Columns have types.

Common types include:

```text
INTEGER
TEXT
BOOLEAN
DATE
TIMESTAMP
NUMERIC
```

For example:

```sql
CREATE TABLE users (
    id INTEGER,
    name TEXT,
    active BOOLEAN
);
```

The type tells the database what kind of value belongs in the column.

---

# 6. Insert Data

Now we can add a row.

```sql
INSERT INTO users (
    id,
    name,
    email
)
VALUES (
    1,
    'Alice',
    'alice@example.com'
);
```

Another:

```sql
INSERT INTO users (
    id,
    name,
    email
)
VALUES (
    2,
    'Bob',
    'bob@example.com'
);
```

Now our table contains two users.

---

# 7. Read Data With SELECT

The most common SQL operation is:

```sql
SELECT
```

For example:

```sql
SELECT *
FROM users;
```

This means:

```text
Select everything
from the users table.
```

The result might be:

```text
1 | Alice | alice@example.com
2 | Bob   | bob@example.com
```

---

# 8. Select Specific Columns

We do not always need every column.

```sql
SELECT name, email
FROM users;
```

Result:

```text
Alice | alice@example.com
Bob   | bob@example.com
```

This is often better than:

```sql
SELECT *
```

when we only need specific information.

---

# 9. WHERE

Suppose we only want Alice.

```sql
SELECT *
FROM users
WHERE name = 'Alice';
```

Now the database returns only Alice's row.

This is called:

```text
Filtering
```

---

# 10. More Conditions

We can combine conditions.

```sql
SELECT *
FROM users
WHERE name = 'Alice'
AND active = TRUE;
```

We can also use:

```text
OR
```

For example:

```sql
SELECT *
FROM users
WHERE name = 'Alice'
OR name = 'Bob';
```

---

# 11. Comparison Operators

SQL supports comparisons such as:

```text
=
!=
>
<
>=
<=
```

For example:

```sql
SELECT *
FROM jobs
WHERE salary > 100000;
```

This asks for jobs where salary is greater than 100,000.

---

# 12. ORDER BY

Suppose we want users sorted alphabetically.

```sql
SELECT *
FROM users
ORDER BY name;
```

Descending order:

```sql
SELECT *
FROM users
ORDER BY name DESC;
```

Ascending order is:

```text
ASC
```

and is the default in many cases.

---

# 13. LIMIT

Suppose a table contains thousands of rows.

We only want the first ten.

```sql
SELECT *
FROM users
LIMIT 10;
```

This is useful when exploring data or building interfaces.

---

# 14. UPDATE

Now suppose Alice changes her email.

```sql
UPDATE users
SET email = 'newalice@example.com'
WHERE id = 1;
```

The important part is:

```sql
WHERE id = 1
```

Without a condition, you could accidentally update every row.

So always understand which rows an UPDATE affects.

---

# 15. DELETE

We can delete a row:

```sql
DELETE FROM users
WHERE id = 2;
```

Again, the:

```sql
WHERE
```

condition matters.

Without it:

```sql
DELETE FROM users;
```

could delete every row in the table.

---

# 16. CRUD Summary

We now have the basic four operations:

```text
CREATE
   ↓
INSERT

READ
   ↓
SELECT

UPDATE
   ↓
UPDATE

DELETE
   ↓
DELETE
```

These operations appear in almost every data-driven application.

---

# 17. Primary Keys

Now we need to make our tables more reliable.

Consider:

```text
id    name
1     Alice
2     Bob
```

The `id` uniquely identifies each user.

We can declare it as a primary key:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
);
```

A primary key identifies a row.

---

# 18. Why Primary Keys Matter

Imagine two users both named:

```text
Alice
```

Names are not necessarily unique.

But IDs can be:

```text
1 → Alice
2 → Alice
```

Now we can distinguish them.

This is why databases commonly use IDs as primary keys.

---

# 19. Auto-Generated IDs

In PostgreSQL, a common approach is to let the database generate IDs.

For example:

```sql
CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    email TEXT
);
```

Now we can insert:

```sql
INSERT INTO users (name, email)
VALUES (
    'Alice',
    'alice@example.com'
);
```

The database generates the ID.

---

# 20. Relationships

Our AI Career Companion needs more than one table.

We might have:

```text
users
resumes
jobs
matches
```

A resume belongs to a user.

So:

```text
User
 │
 └── Resume
```

A job can have many matches.

So:

```text
Job
 │
 ├── Match
 ├── Match
 └── Match
```

This is where relational databases become powerful.

---

# 21. Foreign Keys

Suppose:

```text
users
```

has:

```text
id
```

and:

```text
resumes
```

has:

```text
user_id
```

We can make `user_id` reference the user:

```sql
CREATE TABLE resumes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    filename TEXT
);
```

Now:

```text
resumes.user_id
```

connects a resume to:

```text
users.id
```

This is a:

# Foreign Key

---

# 22. Visualizing the Relationship

Think:

```text
users
────────────────
id | name
────────────────
1  | Alice
2  | Bob


resumes
────────────────────
id | user_id | file
────────────────────
1  | 1       | a.pdf
2  | 1       | b.pdf
3  | 2       | c.pdf
```

Alice has:

```text
a.pdf
b.pdf
```

Bob has:

```text
c.pdf
```

The database knows this relationship through:

```text
user_id
```

---

# 23. JOIN

Now suppose we want:

```text
Resume filename
+
User name
```

The information lives in two tables.

We can combine them with:

```sql
SELECT
    users.name,
    resumes.filename
FROM users
JOIN resumes
    ON users.id = resumes.user_id;
```

This is one of the most important SQL concepts.

We are joining related tables.

---

# 24. Why Not Put Everything in One Table?

We could create:

```text
user_name
user_email
resume_filename
job_title
match_score
```

all in one giant table.

But then information gets repeated.

For example:

```text
Alice
Alice
Alice
Alice
```

for every resume or job match.

Relational databases allow us to organize related information into separate tables.

---

# 25. Our Initial Schema

For the AI Career Companion, we can begin with:

```text
users
│
├── resumes
│
├── jobs
│
└── matches
```

A simplified design:

```text
users
----------------
id
name
email


resumes
----------------
id
user_id
filename
text


jobs
----------------
id
title
description


matches
----------------
id
resume_id
job_id
score
```

This is enough to begin.

We can improve it later.

---

# 26. Querying Related Data

Suppose we want to see all resumes belonging to Alice.

```sql
SELECT
    users.name,
    resumes.filename
FROM users
JOIN resumes
    ON users.id = resumes.user_id
WHERE users.name = 'Alice';
```

The database performs the relationship lookup for us.

---

# 27. SQL Is Declarative

One useful concept is that SQL is largely **declarative**.

In Python, we might think:

```python
for user in users:
    if user["name"] == "Alice":
        print(user)
```

In SQL, we describe what we want:

```sql
SELECT *
FROM users
WHERE name = 'Alice';
```

We don't manually tell the database how to scan every row.

We describe the result we want.

---

# 28. SQL and Python Work Together

SQL does not replace Python.

They have different responsibilities.

For example:

```text
Python
 ↓
Application logic
 ↓
SQL
 ↓
Database
```

Python might decide:

```text
"The user wants their previous resumes."
```

Then SQL retrieves them.

---

# 29. A Small Python Example

Eventually we will connect Python to our database.

Conceptually:

```python
result = database.query(
    """
    SELECT *
    FROM resumes
    WHERE user_id = %s
    """
)
```

The exact Python API will depend on the database client.

For now, focus on understanding the SQL itself.

---

# 30. Practice Database

Before connecting Supabase, practice with a small database.

Create:

```text
students
```

with:

```text
id
name
email
course
```

Insert several students.

Then answer:

```text
1. How many students are there?

2. Find students enrolled in Python.

3. Sort students by name.

4. Find one student by ID.

5. Update an email.

6. Delete a student.

7. Add a second table for courses.

8. Connect students to courses.
```

Write the SQL yourself.

---

# 31. Mini Project

Create a simple:

# Student Database

Tables:

```text
students
courses
```

Relationships:

```text
student
   ↓
course
```

Then practice:

```text
INSERT
SELECT
WHERE
ORDER BY
UPDATE
DELETE
JOIN
```

The goal is not the application UI.

The goal is becoming comfortable asking a database questions.

---

# 32. Common Mistakes

### Forgetting WHERE

Dangerous:

```sql
UPDATE users
SET name = 'Alice';
```

This may update every row.

Better:

```sql
UPDATE users
SET name = 'Alice'
WHERE id = 1;
```

---

### Deleting Without a Condition

Dangerous:

```sql
DELETE FROM users;
```

This deletes all rows.

Always understand what your query affects.

---

### Confusing IDs

Remember:

```text
Primary key
```

identifies a row.

```text
Foreign key
```

connects a row to another table.

---

# 33. The Mental Model

You should now be able to visualize:

```text
DATABASE
│
├── TABLE
│     │
│     ├── ROW
│     └── COLUMN
│
├── PRIMARY KEY
│
└── FOREIGN KEY
        │
        ▼
      TABLE
```

And:

```text
Python
  ↓
SQL
  ↓
Database
  ↓
Rows
```

---

# 34. What We Have Learned

We started with:

```python
users = []
```

and discovered why that isn't enough for a real application.

We learned:

```text
Database
Table
Row
Column
Primary Key
Foreign Key
CRUD
SELECT
WHERE
ORDER BY
JOIN
```

These concepts will become the foundation for the rest of Phase 5.

---

# 35. Next Step

Now we have learned how relational databases work.

The next question is:

> **How do we get a real PostgreSQL database without spending the course configuring database infrastructure?**

We will use:

# Supabase

And connect our Python application to it.
