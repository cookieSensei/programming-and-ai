# 0. From Application to Product

## From a Program That Runs to Software That Remembers

In the previous phases, we learned how to build programs and intelligent applications.

For example, a Phase 4 application might look like:

```text
User
 ↓
Streamlit
 ↓
Python
 ↓
AI / ML
 ↓
Result
```

The application accepts an input, processes it, and produces an output.

That is useful.

But there is an important question:

> **What happens when the application stops running?**

---

# 1. What Does the Application Remember?

Imagine our Resume Intelligence application.

A user uploads:

```text
resume.pdf
```

The application extracts:

```text
Name
Email
Skills
Experience
```

Then it calculates:

```text
Match Score: 82%
```

The result appears on the screen.

Now the user closes the browser.

Tomorrow they open the application again.

Where is the resume?

Where is the match score?

Where is the user's history?

If we only stored everything in Python variables:

```python
resume = {}
matches = []
```

the information disappears when the program stops.

This leads us to an important concept:

# Persistence

---

# 2. Temporary Data vs Persistent Data

Consider:

```python
name = "Alice"
```

This value exists in the running Python process.

Conceptually:

```text
Python Program
      ↓
    Memory
      ↓
      name
```

When the program ends:

```text
Python Program
      ↓
     STOP
      ↓
   Memory gone
```

Persistent data is different:

```text
Python Program
      ↓
    Database
      ↓
   Stored Data
```

The program can stop.

The data remains.

---

# 3. Why Do We Need Databases?

Suppose our application has many users.

We might have:

```text
Alice
 ├── resume.pdf
 ├── Resume skills
 └── 3 job matches

Bob
 ├── resume.pdf
 ├── Resume skills
 └── 5 job matches
```

Trying to manage this entirely with Python variables quickly becomes difficult.

We need a system designed to:

```text
Store data
Retrieve data
Update data
Delete data
Relate data
```

That system is a:

# Database

---

# 4. A Database Is Not AI

This distinction is important.

A database does not:

```text
learn
predict
classify
generate
```

Instead, it stores and retrieves information.

For example:

```text
AI model
   ↓
Predicts match score
   ↓
Database
   ↓
Stores match score
```

So:

```text
AI
```

and:

```text
Database
```

solve different problems.

---

# 5. Our Application Is Growing

In Phase 4:

```text
Resume
 ↓
Analysis
 ↓
Result
```

In Phase 5:

```text
User
 ↓
Application
 ↓
Resume
 ↓
Analysis
 ↓
Database
 ↓
Result
```

Now the application can remember.

---

# 6. State

A useful word for this is:

> **State**

State is information about what is currently happening or what has happened.

For our application, state might include:

```text
Current user
Uploaded resumes
Saved jobs
Previous analyses
Match scores
```

Without persistence:

```text
Application
    ↓
Temporary state
```

With persistence:

```text
Application
    ↓
Persistent state
    ↓
Database
```

---

# 7. Multiple Users

Now imagine:

```text
Alice
```

and:

```text
Bob
```

both use our application.

Alice uploads:

```text
alice_resume.pdf
```

Bob uploads:

```text
bob_resume.pdf
```

The application needs to know:

```text
Which data belongs to Alice?
Which data belongs to Bob?
```

This introduces another concept:

# Users

---

# 8. User Identity

We need some way to identify a user.

Conceptually:

```text
Alice → User ID 1
Bob   → User ID 2
```

Then data can be associated with the user.

For example:

```text
User 1
 ├── Resume 101
 └── Match 501

User 2
 ├── Resume 102
 └── Match 502
```

We will later use authentication and database relationships to implement this.

---

# 9. Files vs Data

A resume contains:

```text
resume.pdf
```

But our application also extracts information from it:

```text
name
email
skills
experience
```

These are different kinds of data.

We can think of them as:

```text
File
 ↓
Storage

Structured information
 ↓
Database
```

For example:

```text
resume.pdf
      │
      ├──────────────→ File Storage
      │
      └→ Extracted data → Database
```

We will later use Supabase to work with both.

---

# 10. What Is a Backend?

So far, Streamlit has allowed us to put the interface and Python logic together conveniently.

As applications grow, we start thinking in terms of responsibilities:

```text
User Interface
      ↓
Application Logic
      ↓
Data / Services
```

The part responsible for handling data and application operations is often called the:

# Backend

For this course, we do not need to build a complicated backend architecture.

We simply need to understand the separation of responsibilities.

---

# 11. Frontend vs Backend

A simplified picture is:

```text
             USER
               │
               ▼
          FRONTEND / UI
               │
               ▼
        APPLICATION LOGIC
               │
        ┌──────┴──────┐
        ▼             ▼
       AI          DATABASE
```

The UI shows information.

The application logic decides what to do.

The database remembers information.

The AI components perform tasks such as:

```text
classification
extraction
similarity
prediction
```

---

# 12. Our New Application Flow

A user might now do this:

```text
Open application
      ↓
Create account
      ↓
Login
      ↓
Upload resume
      ↓
Resume is stored
      ↓
Resume is analyzed
      ↓
Analysis is stored
      ↓
User views result
      ↓
User returns tomorrow
      ↓
Previous result is still available
```

This is fundamentally different from a simple script.

---

# 13. CRUD

Once we have persistent data, four operations appear repeatedly.

They are commonly called:

```text
Create
Read
Update
Delete
```

Together:

# CRUD

For a resume application:

```text
Create
→ Add a resume

Read
→ View a resume

Update
→ Change resume information

Delete
→ Remove a resume
```

These four operations will become central when we learn SQL.

---

# 14. Why SQL Comes Next

Now we have a problem:

> We need to tell the database what data to store and what data to retrieve.

This is where SQL comes in.

SQL allows us to write instructions such as:

```sql
SELECT *
FROM resumes;
```

or:

```sql
SELECT *
FROM resumes
WHERE user_id = 1;
```

We will learn SQL in the next section.

---

# 15. The Important Mental Model

Do not think:

```text
SQL = another programming language I have to memorize.
```

Think:

```text
Application
      ↓
Needs data
      ↓
Database
      ↓
SQL
      ↓
Ask database for data
```

SQL is a language for working with relational databases.

---

# 16. Phase 4 vs Phase 5

This is the transition between the two phases.

### Phase 4

```text
Can I build an intelligent application?
```

### Phase 5

```text
Can I build an application
that remembers, has users,
and can be used repeatedly?
```

That is why we are introducing databases now.

---

# 17. The Project We Are Building Toward

Our central Phase 5 project is:

# AI Career Companion

It will eventually look roughly like:

```text
                  AI CAREER COMPANION

                         USER
                          │
                          ▼
                       LOGIN
                          │
                          ▼
                      DASHBOARD
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          RESUMES        JOBS       ANALYSIS
             │            │            │
             └────────────┼────────────┘
                          ▼
                   MATCHING ENGINE
                          │
                          ▼
                       DATABASE
                          │
                          ▼
                        RESULTS
```

We will build this one piece at a time.

---

# 18. What We Are Not Doing Yet

We are not going to immediately build:

```text
Authentication
Database
Storage
AI
Dashboard
```

all at once.

That would hide the learning.

Instead:

```text
Understand the problem
        ↓
Learn SQL
        ↓
Create a database
        ↓
Connect Python
        ↓
Add users
        ↓
Add storage
        ↓
Combine with AI
```

Each step introduces one new idea.

---

# 19. Exercise

Before continuing, think about a simple application you have already built.

For example:

```text
Calculator
```

Ask:

```text
What data does it need?

What data should it remember?

What happens when the program closes?
```

Now consider:

```text
Resume Intelligence
```

Ask:

```text
What should be remembered?

Who owns the data?

What should happen when the user returns?
```

Write down your answers.

---

# 20. Takeaway

We have made an important conceptual transition.

Previously:

```text
Program
 ↓
Input
 ↓
Output
```

Now:

```text
User
 ↓
Application
 ↓
AI / Logic
 ↓
Database
 ↓
Persistent Data
```

The application is no longer just something that runs.

It can **remember**.

That is the reason we need databases.

And that is why the next thing we learn is:

# SQL
