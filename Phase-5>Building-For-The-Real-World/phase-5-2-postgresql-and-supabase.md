# 2. PostgreSQL + Supabase

## From SQL on a Screen to a Real Application Database

We now know the basics of SQL.

We can:

```text
CREATE
INSERT
SELECT
UPDATE
DELETE
JOIN
```

But so far, we have mostly thought about a database as an abstract concept.

Now we are going to use a real PostgreSQL database.

We will use:

# Supabase

Supabase gives every project a full PostgreSQL database. We can work with that database through the Supabase Dashboard, SQL Editor, or programmatically from Python. citeturn0search7

The goal of this tutorial is not to learn every feature of Supabase.

The goal is:

> **Connect a real database to a Python application.**

---

# 1. What Is Supabase?

Supabase is a platform built around PostgreSQL.

For this project, the important pieces are:

```text
Supabase
│
├── PostgreSQL Database
├── Authentication
├── Storage
└── APIs / Client Libraries
```

We will introduce these pieces gradually.

For now, focus on:

```text
Python
   ↓
Supabase
   ↓
PostgreSQL
```

---

# 2. Why PostgreSQL?

PostgreSQL is a relational database system.

That means the SQL concepts we just learned still apply.

For example:

```sql
SELECT *
FROM users;
```

is still SQL.

Supabase is not replacing PostgreSQL with a different database language.

It gives us a hosted PostgreSQL database and tools around it. citeturn0search7

---

# 3. Create a Supabase Project

Create a Supabase project from the Supabase Dashboard.

The project gives us a PostgreSQL database that we can manage through the dashboard.

Once the project exists, we can use the:

```text
Table Editor
```

to inspect tables visually and:

```text
SQL Editor
```

to write SQL directly. citeturn0search7

---

# 4. Create Our First Table

Let's create a simple table for our future application.

Open the SQL Editor and run:

```sql
CREATE TABLE notes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

We have now created a real PostgreSQL table.

---

# 5. Look at the Table

Open the Table Editor.

You should now see:

```text
notes
──────────────────────────────
id
title
content
created_at
```

The important realization is:

> **This is the same relational database we just learned to manipulate with SQL.**

The difference is that the database is now hosted by Supabase.

---

# 6. Insert Some Data

Use SQL:

```sql
INSERT INTO notes (
    title,
    content
)
VALUES (
    'First Note',
    'Learning Supabase'
);
```

Add another:

```sql
INSERT INTO notes (
    title,
    content
)
VALUES (
    'Second Note',
    'Connecting Python to PostgreSQL'
);
```

Now:

```sql
SELECT *
FROM notes;
```

should return the records.

---

# 7. The Database Is Persistent

Stop thinking about the table as Python memory.

The data is stored in PostgreSQL.

Conceptually:

```text
Python Program
      ↓
Supabase
      ↓
PostgreSQL
      ↓
notes
```

If the Python program stops, the rows remain in the database.

That is persistence.

---

# 8. Install the Python Client

Supabase provides an official Python client.

Install it with:

```bash
pip install supabase
```

The current Supabase Python documentation lists `supabase` as the package installed from PyPI. citeturn0search2

We will use this library to interact with the database from Python.

---

# 9. Why Use a Client Library?

We could connect to PostgreSQL directly.

But Supabase provides a Python client that makes common operations convenient.

Our application can think in terms of:

```python
supabase.table("notes")
```

instead of manually implementing every HTTP request.

The client is our Python entry point into Supabase functionality. citeturn0search1

---

# 10. Project Structure

Create a small project:

```text
supabase-demo/
│
├── app.py
├── .env
└── requirements.txt
```

Later, this will grow into our AI Career Companion.

For now, keep it tiny.

---

# 11. Environment Variables

Our application needs the Supabase project URL and a key.

Do not write secrets directly into:

```python
app.py
```

Instead, use environment variables.

For example:

```text
SUPABASE_URL=your-project-url
SUPABASE_PUBLISHABLE_KEY=your-key
```

The Supabase documentation shows initializing the Python client from environment variables. citeturn0search1turn0search3

---

# 12. Why Not Hardcode the Key?

Avoid:

```python
SUPABASE_KEY = "some-secret-value"
```

inside source code that might be committed to Git.

Instead:

```text
Environment
     ↓
Application
     ↓
Supabase client
```

This also makes it easier to use different credentials in different environments.

---

# 13. Load the Environment

Install:

```bash
pip install python-dotenv
```

Then:

```python
import os
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get(
    "SUPABASE_URL"
)

key = os.environ.get(
    "SUPABASE_PUBLISHABLE_KEY"
)
```

We can now initialize the client.

---

# 14. Create the Supabase Client

```python
from supabase import create_client

supabase = create_client(
    url,
    key
)
```

The official Python documentation uses `create_client()` with the project URL and key. citeturn0search1

Our application now has a connection to the Supabase client.

---

# 15. First SELECT From Python

We created:

```text
notes
```

Now let's read it.

```python
response = (
    supabase
    .table("notes")
    .select("*")
    .execute()
)

print(response.data)
```

Conceptually:

```text
Python
  ↓
Supabase client
  ↓
notes table
  ↓
PostgreSQL
  ↓
Rows
```

---

# 16. Compare SQL and Python

We previously wrote:

```sql
SELECT *
FROM notes;
```

The Python client expresses the same basic operation as:

```python
response = (
    supabase
    .table("notes")
    .select("*")
    .execute()
)
```

This is important.

We are not abandoning SQL.

We are using a Python interface to interact with our database.

---

# 17. Insert From Python

Now let's create a record from Python.

```python
response = (
    supabase
    .table("notes")
    .insert({
        "title": "Python Note",
        "content": "Inserted from Python"
    })
    .execute()
)
```

The official Supabase Python API supports passing a dictionary to `insert()` for a single row. citeturn0search0

Now run:

```python
print(response.data)
```

and inspect the table in Supabase.

---

# 18. Insert Multiple Rows

We can also insert multiple records:

```python
response = (
    supabase
    .table("notes")
    .insert([
        {
            "title": "Note A",
            "content": "First"
        },
        {
            "title": "Note B",
            "content": "Second"
        }
    ])
    .execute()
)
```

The client supports a list for bulk inserts. citeturn0search0

---

# 19. Filtering

Suppose we only want a particular record.

The Python client lets us add filters.

For example:

```python
response = (
    supabase
    .table("notes")
    .select("*")
    .eq("id", 1)
    .execute()
)
```

The idea is similar to:

```sql
SELECT *
FROM notes
WHERE id = 1;
```

The SQL mental model remains useful.

---

# 20. Update

We can update a record:

```python
response = (
    supabase
    .table("notes")
    .update({
        "title": "Updated Title"
    })
    .eq("id", 1)
    .execute()
)
```

The important part is:

```python
.eq("id", 1)
```

We want to target a specific record.

Supabase's Python documentation recommends combining `update()` with filters to target the rows being updated. citeturn0search13

---

# 21. Delete

We can delete a record using a filter:

```python
response = (
    supabase
    .table("notes")
    .delete()
    .eq("id", 1)
    .execute()
)
```

Again, the filter matters.

Think back to:

```sql
DELETE FROM notes
WHERE id = 1;
```

---

# 22. CRUD From Python

We now have:

```text
CREATE
 ↓
insert()

READ
 ↓
select()

UPDATE
 ↓
update()

DELETE
 ↓
delete()
```

This maps nicely to the SQL concepts we already learned.

---

# 23. Build a Tiny Python Application

Let's make a simple command-line application.

```python
import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_PUBLISHABLE_KEY"]
)

response = (
    supabase
    .table("notes")
    .select("*")
    .execute()
)

for note in response.data:
    print(note["title"])
```

Run:

```bash
python app.py
```

You should see the titles stored in your database.

---

# 24. What Just Happened?

A Python program:

```text
started
   ↓
loaded environment variables
   ↓
created Supabase client
   ↓
queried PostgreSQL
   ↓
received rows
   ↓
printed them
```

That is a real application talking to a real database.

---

# 25. Add Streamlit

We already know Streamlit from earlier phases.

Let's combine:

```text
Streamlit
+
Supabase
```

Start with:

```python
import streamlit as st

st.title("My Notes")
```

Then query:

```python
response = (
    supabase
    .table("notes")
    .select("*")
    .execute()
)
```

Display the notes:

```python
for note in response.data:
    st.write(note["title"])
```

Now the database is behind a user interface.

---

# 26. Add a Form

```python
title = st.text_input(
    "Title"
)

content = st.text_area(
    "Content"
)

if st.button("Save"):
    supabase.table("notes").insert({
        "title": title,
        "content": content
    }).execute()

    st.success("Saved!")
```

Now:

```text
User
 ↓
Streamlit
 ↓
Python
 ↓
Supabase
 ↓
PostgreSQL
```

The user can create persistent records.

---

# 27. Refresh the Application

After inserting a record, we may want the interface to show the new data.

One simple approach is to rerun the Streamlit script after the operation.

The important idea is:

```text
Insert
 ↓
Database changes
 ↓
Application reruns
 ↓
SELECT
 ↓
New data appears
```

This is a good place to introduce the idea that the UI is a view over persistent state.

---

# 28. Our First Real Architecture

We now have:

```text
                  USER
                    │
                    ▼
                STREAMLIT
                    │
                    ▼
                  PYTHON
                    │
                    ▼
              SUPABASE CLIENT
                    │
                    ▼
                POSTGRESQL
                    │
                    ▼
                  TABLES
```

This is a simple but real software architecture.

---

# 29. Create an Application Table

Let's move from generic notes toward our actual project.

Create:

```sql
CREATE TABLE resumes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id TEXT,
    filename TEXT NOT NULL,
    extracted_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

For the moment, `user_id` is just a placeholder.

We will properly connect it to authentication later.

---

# 30. Insert a Resume Record

Suppose our Python application has extracted:

```text
filename:
resume.pdf
```

and:

```text
extracted_text:
Python developer with experience in...
```

We can store the metadata:

```python
supabase.table("resumes").insert({
    "filename": "resume.pdf",
    "extracted_text": extracted_text
}).execute()
```

Now the resume information survives after the application closes.

---

# 31. Database vs File Storage

Notice something.

We stored:

```text
filename
extracted_text
```

But we did not necessarily store the actual:

```text
resume.pdf
```

inside the database.

That leads to our next concept:

```text
Database
+
File Storage
```

Supabase provides Storage for files, while PostgreSQL stores structured records. Supabase's Python client also exposes Storage operations. citeturn0search16

We will cover Storage in a later section.

---

# 32. Security Begins Here

We have intentionally kept this first database connection simple.

But now ask:

> What stops one user from reading another user's records?

This is an important real-world problem.

Supabase's database security model includes Row Level Security (RLS), which can restrict access to rows. Supabase recommends understanding RLS before exposing tables directly to an application. citeturn0search7turn0search2

We will introduce this after authentication.

---

# 33. A Note About Keys

Supabase has different types of keys and roles.

For a normal application client, use the appropriate publishable/client credential and database policies.

Never put an administrative secret key into browser-visible code.

Supabase explicitly warns that secret/admin keys must remain on trusted server-side environments and should never be exposed in the browser. citeturn0search4

For our introductory Streamlit application, keep credentials in environment variables and understand what access the credential provides.

---

# 34. A Useful Experiment

Try this:

### Step 1

Run your Python program.

### Step 2

Insert a note.

### Step 3

Stop Python.

### Step 4

Run Python again.

### Step 5

Read the notes.

You should still see the note.

That is the difference between:

```text
Python memory
```

and:

```text
Persistent database storage
```

---

# 35. Another Experiment

Create three notes:

```text
Python
SQL
Supabase
```

Then retrieve only:

```text
SQL
```

using a filter.

Next:

```text
Update SQL → PostgreSQL
```

Then delete:

```text
Python
```

Finally retrieve all remaining rows.

You have now performed:

```text
INSERT
SELECT
UPDATE
DELETE
```

from Python against a real PostgreSQL database.

---

# 36. Mini Project - Persistent Notes

Build:

# Persistent Notes

The application should allow a user to:

```text
Create a note
View notes
Update a note
Delete a note
```

Use:

```text
Streamlit
+
Supabase
+
PostgreSQL
```

The UI does not need to be beautiful.

The important part is that the data survives application restarts.

---

# 37. Suggested Project Structure

```text
persistent-notes/
│
├── app.py
├── .env
├── requirements.txt
└── README.md
```

`requirements.txt` might contain:

```text
streamlit
supabase
python-dotenv
```

Do not commit `.env`.

---

# 38. What Students Should Understand

At the end of this section, you should understand:

```text
What PostgreSQL is
What Supabase provides
How SQL relates to Supabase
How Python connects to Supabase
How to SELECT data
How to INSERT data
How to UPDATE data
How to DELETE data
Why environment variables matter
Why database security matters
```

You do not need to memorize the entire Supabase API.

You need to know how to find the documentation for the operation you need.

---

# 39. The Most Important New Skill

Earlier, we could build everything locally.

Now we are learning to work with a service we did not build ourselves.

That means we need a new workflow:

```text
Need something
    ↓
Read documentation
    ↓
Find relevant API
    ↓
Try tiny example
    ↓
Inspect result
    ↓
Integrate into application
```

This workflow will become increasingly important in the rest of Phase 5.

---

# 40. Next Step

We can now connect:

```text
Python
   ↓
Supabase
   ↓
PostgreSQL
```

But our application still does not know who the user is.

The next problem is:

> **How do we create accounts and associate database records with users?**

That leads us to:

# Authentication
