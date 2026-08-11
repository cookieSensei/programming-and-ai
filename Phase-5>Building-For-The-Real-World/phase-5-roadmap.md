# Phase 5 — Building for the Real World

Phase 4 taught us how to combine programming and AI to build intelligent applications.

Now we take the next step.

A useful application should not only produce an answer.

It should be able to:

```text
Remember data
Have users
Store files
Handle multiple requests
Keep information after the program closes
Work with other people
Use unfamiliar technologies
```

This is where our applications begin to feel like real software.

The goal of Phase 5 is **not** to introduce every technology used by professional software engineers.

The goal is to develop the ability to take what we already know and turn it into software that can live beyond a single Python process.

---

# The Phase 5 Journey

```text
Phase 4
Building Intelligent Systems
        ↓
"Can I build an intelligent application?"
        ↓
Phase 5
Building for the Real World
        ↓
"Can I keep data, work with users,
learn new tools, and build with others?"
```

---

# 0. From Application to Product

Before introducing databases, we first discover why we need them.

In Phase 4, an application might work like:

```text
User
 ↓
Streamlit
 ↓
Python
 ↓
AI
 ↓
Result
```

But what happens when the program stops?

The data disappears.

Now ask:

```text
What if a user comes back tomorrow?

What if there are 100 users?

What if we need to remember previous results?

What if users need to upload files?

What if two people use the application at the same time?
```

These questions lead naturally to the next concepts.

```text
Application
   ↓
State
   ↓
Persistence
   ↓
Database
   ↓
Users
   ↓
Backend
```

---

# 1. SQL & Databases

We introduce SQL because our application has data that needs to be stored.

Instead of:

```python
users = []
```

we begin thinking about:

```text
users
resumes
jobs
applications
matches
```

as database tables.

Students learn the basic language of relational databases:

```text
CREATE TABLE
INSERT
SELECT
WHERE
ORDER BY
UPDATE
DELETE
```

Then:

```text
Primary Keys
Foreign Keys
Relationships
JOIN
```

The goal is not to become a database administrator.

The goal is to understand:

> **How applications store and retrieve structured data.**

---

# 2. PostgreSQL Through Supabase

Instead of spending the course configuring a database server, we use Supabase.

Supabase gives us access to a real PostgreSQL database.

Students can see their tables, write SQL, and connect their Python applications to the database.

The conceptual progression is:

```text
Python variable
      ↓
Python data structure
      ↓
File / CSV
      ↓
SQL table
      ↓
PostgreSQL database
```

The database is no longer something abstract.

It becomes part of the application.

---

# 3. Connecting Python to the Database

Now our application becomes:

```text
Streamlit
    ↓
Python
    ↓
Supabase
    ↓
PostgreSQL
```

Students learn basic CRUD operations:

```text
Create
Read
Update
Delete
```

For example:

```text
User uploads resume
        ↓
Python processes it
        ↓
Store resume information
        ↓
Read it later
```

This is the first time an application we've built can genuinely remember something.

---

# 4. Authentication & Users

Once data exists, another question appears:

> **Whose data is it?**

Now introduce authentication.

The application becomes:

```text
Sign Up
   ↓
Login
   ↓
User
   ↓
User ID
   ↓
User's Data
```

For example:

```text
Alice
 ├── Resume A
 ├── Resume B
 └── Job Match 1

Bob
 ├── Resume C
 └── Job Match 2
```

The database now needs to understand relationships between users and their data.

---

# 5. Row-Level Access

We introduce the basic idea of:

> A user should only be able to access the data they are allowed to access.

For example:

```text
Alice → Alice's resumes
Bob   → Bob's resumes
```

This introduces database access policies at a conceptual level.

Students do not need to become security experts.

They need to understand why access control exists and how the database can participate in enforcing it.

---

# 6. Files and Storage

A database row is not necessarily the right place to store a PDF.

Now we discover another distinction:

```text
Structured data
        ↓
Database
```

versus:

```text
Files
        ↓
Object storage
```

Our application can therefore have:

```text
Supabase
│
├── PostgreSQL
│     ├── users
│     ├── resumes
│     ├── jobs
│     └── matches
│
└── Storage
      ├── resume-a.pdf
      ├── resume-b.pdf
      └── ...
```

The database can store information **about** a file while storage keeps the actual file.

---

# 7. Project — AI Career Companion

We now combine Phase 4's Resume Intelligence application with everything learned in Phase 5.

The application becomes:

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
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          RESUMES          JOBS         ANALYSIS
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                     MATCHING ENGINE
                            │
                            ▼
                         DATABASE
                            │
                            ▼
                          RESULTS
```

The system can:

```text
Create an account
Upload a resume
Store the resume
Parse the resume
Add job descriptions
Match resumes to jobs
Store results
View previous analyses
```

Now our Phase 4 application has persistence and users.

---

# 8. Build Incrementally

Do not build the complete application in one step.

Use versions.

### Version 1

```text
Streamlit
+
Supabase
+
One table
```

### Version 2

```text
Create
Read
Update
Delete
```

### Version 3

```text
User accounts
```

### Version 4

```text
Resume upload
+
Storage
```

### Version 5

```text
Resume parsing
```

### Version 6

```text
Job descriptions
+
Matching
```

### Version 7

```text
Persistent match history
```

### Version 8

```text
Dashboard
```

Each version should introduce one meaningful idea.

---

# 9. AI-Assisted Development

Phase 5 is also where we change how we learn technologies.

We will encounter libraries and services we have never used before.

Instead of waiting for a tutorial for every API, learn how to investigate.

Use:

```text
Documentation
    ↓
Small experiment
    ↓
Error
    ↓
Question
    ↓
AI assistant
    ↓
Test the suggestion
    ↓
Understand
    ↓
Integrate
```

The AI assistant is a learning and development tool.

It is not a replacement for understanding the code.

---

# 10. Asking Better Questions

Instead of asking:

```text
"Build Supabase authentication for me."
```

ask:

```text
"I have a Streamlit application.
I have a Supabase project.
How does authentication work?
Show me the smallest example that lets
a user sign in and retrieve their user ID."
```

Then test the example.

The goal is to learn how to reduce a large problem into a small experiment.

---

# 11. Read Documentation

When using a new technology, look for:

```text
Getting Started
Installation
Authentication
Basic Usage
Examples
API Reference
```

Students should become comfortable navigating documentation without needing a tutorial for every operation.

This is one of the core capabilities of Phase 5.

---

# 12. Debugging With AI

When something fails:

```text
Error
 ↓
Read the error
 ↓
Identify the relevant code
 ↓
Form a hypothesis
 ↓
Ask AI / search documentation
 ↓
Try the smallest fix
 ↓
Verify
```

Do not simply paste the entire project into an AI assistant and accept a giant rewrite.

The objective is:

> **Understand why the problem happened.**

---

# 13. Git Becomes a Team Tool

Git was introduced earlier.

Now we use it as a collaboration system.

Instead of only:

```text
edit
 ↓
commit
 ↓
edit
 ↓
commit
```

we can work with:

```text
main
 │
 ├── feature/auth
 ├── feature/resume-upload
 ├── feature/dashboard
 └── feature/matching
```

A feature can follow:

```text
Branch
 ↓
Build
 ↓
Commit
 ↓
Push
 ↓
Pull Request
 ↓
Review
 ↓
Merge
```

---

# 14. Issues

Before writing code, describe the problem.

For example:

```text
Issue #12

Add resume upload

Goal:
Allow authenticated users to upload a PDF resume.

Requirements:
- User must be logged in
- Accept PDF
- Store file
- Store metadata
- Show upload success
```

Now development becomes connected to a clear task.

---

# 15. Pull Requests

A pull request is a place to discuss a proposed change before merging it.

A student should be able to explain:

```text
What did I change?

Why did I change it?

How did I test it?

What should the reviewer look at?
```

This is a small but important professional habit.

---

# 16. Code Review

The goal of code review is not:

```text
Find mistakes in someone's code.
```

It is:

```text
Understand the change
+
Improve the code
+
Share knowledge
```

Students should learn to give useful feedback.

For example:

```text
"Could this database operation be moved
into a separate function so the Streamlit
page remains easier to read?"
```

is more useful than:

```text
"This code is bad."
```

---

# 17. Team Project

The final project of Phase 5 can be collaborative.

A small team might divide work:

```text
Team
│
├── Database
├── Authentication
├── UI
├── AI / Resume pipeline
└── Integration
```

But everyone should understand the overall architecture.

The objective is not to create isolated pieces.

It is to learn how separate contributions become one application.

---

# 18. Final Real-World Project

After the guided AI Career Companion project, students build something of their own.

The requirement is intentionally simple:

> **Build a useful application for a real problem.**

It should contain:

```text
Python
+
Persistent data
+
A real database
+
A user-facing interface
+
At least one intelligent component
```

The intelligent component could come from earlier phases.

For example:

```text
ML classifier
NLP pipeline
Computer vision
OCR
Similarity search
Recommendation
Rule + ML hybrid
```

Students do not need to invent a new AI algorithm.

They need to build a useful system.

---

# 19. Examples

Possible projects:

```text
Study Planner
```

```text
Document Organizer
```

```text
Personal Knowledge Base
```

```text
Job Application Tracker
```

```text
Expense Analyzer
```

```text
Student Feedback Analyzer
```

```text
Image Classification Dashboard
```

```text
Research Paper Organizer
```

The project should be chosen according to the student's interests.

---

# 20. The Final Architecture

By the end of Phase 5, students should understand an architecture like:

```text
                         USER
                           │
                           ▼
                         UI
                           │
                           ▼
                    APPLICATION LOGIC
                      │           │
                      │           │
                      ▼           ▼
                  AI / ML      DATABASE
                      │           │
                      │           ▼
                      │         SQL
                      │           │
                      └─────┬─────┘
                            ▼
                         STORAGE
```

Not every application needs every component.

The important skill is knowing **when a component is useful**.

---

# 21. What Phase 5 Is Really Teaching

The technologies are:

```text
SQL
PostgreSQL
Supabase
Authentication
Storage
Git
GitHub
AI assistants
```

But the deeper capabilities are:

```text
Persistence
Collaboration
Independent learning
Debugging
Reading documentation
Working with unfamiliar tools
Building software for users
```

Those capabilities should survive even when the technologies change.

---

# 22. The Complete Curriculum Journey

We can now see the whole program:

```text
PHASE 0
Learning to Learn
        ↓
"I can learn this."

PHASE 1
Thinking Like a Programmer
        ↓
"I can write programs."

PHASE 2
Building Software
        ↓
"I can build software."

PHASE 3
Teaching Computers to Learn
        ↓
"I can teach a computer to learn."

PHASE 4
Building Intelligent Systems
        ↓
"I can build intelligent systems."

PHASE 5
Building for the Real World
        ↓
"I can continue learning and building
beyond this program."
```

The final statement is deliberately broader than:

```text
"I know SQL."
```

or:

```text
"I know Supabase."
```

Those technologies will change.

The capability is what matters.

---

# 23. Final Phase 5 Roadmap

```text
PHASE 5 — BUILDING FOR THE REAL WORLD
│
├── 0. From Application to Product
│   ├── State
│   ├── Persistence
│   ├── Users
│   └── Why databases exist
│
├── 1. SQL & Databases
│   ├── Tables
│   ├── CRUD
│   ├── Filtering
│   ├── Sorting
│   ├── Primary keys
│   ├── Foreign keys
│   └── JOIN
│
├── 2. PostgreSQL + Supabase
│   ├── Create a project
│   ├── Tables
│   ├── SQL Editor
│   ├── Python connection
│   └── CRUD from Python
│
├── 3. Authentication
│   ├── Sign up
│   ├── Login
│   ├── Sessions
│   ├── User IDs
│   └── Basic row-level access
│
├── 4. Files & Storage
│   ├── Uploads
│   ├── Object storage
│   ├── Database metadata
│   └── User-owned files
│
├── 5. Project — AI Career Companion
│   ├── Users
│   ├── Resumes
│   ├── Jobs
│   ├── Resume parsing
│   ├── Matching
│   ├── Persistent results
│   └── Dashboard
│
├── 6. AI-Assisted Development
│   ├── Documentation
│   ├── AI-assisted learning
│   ├── Debugging
│   ├── Code review
│   └── Learning unfamiliar libraries
│
├── 7. Team Development
│   ├── Issues
│   ├── Branches
│   ├── Pull requests
│   ├── Code review
│   └── Integration
│
└── 8. FINAL REAL-WORLD PROJECT
    ├── Choose a problem
    ├── Design the application
    ├── Use persistent data
    ├── Include an intelligent component
    ├── Work collaboratively
    └── Build something useful
```

---

# 24. The Final Principle

Phase 5 should not end with:

> "Here are ten more technologies you know."

It should end with:

> **"I don't know how to build this yet — but I know how to figure it out."**

That is the capability this phase is designed to develop.

And that matches the existing CookieSensei curriculum philosophy: the curriculum explicitly says that technologies change while the ability to learn does not, and Phase 5's stated outcome is that learners can continue learning and building beyond the program. citeturn0view0
