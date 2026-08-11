# 5. AI Career Companion

## Bringing Everything Together

We have spent the first part of Phase 5 building the infrastructure around an application:

```text
SQL
 ↓
PostgreSQL
 ↓
Supabase
 ↓
Authentication
 ↓
Authorization / RLS
 ↓
File Storage
```

Now we bring back the intelligence we learned in Phase 4.

We are going to build:

# AI Career Companion

This is not a production SaaS application. It is a **learning project** whose purpose is to demonstrate how the pieces we have learned fit together.

---

# 1. The Big Transition

In Phase 4, we could build something like:

```text
Resume
 ↓
OCR / Text Extraction
 ↓
NLP
 ↓
Similarity
 ↓
Match Score
```

The application worked, but it was mostly stateless.

Now we want:

```text
User
 ↓
Login
 ↓
Upload Resume
 ↓
Store Resume
 ↓
Parse Resume
 ↓
Store Analysis
 ↓
Add Job
 ↓
Match Resume → Job
 ↓
Store Match
 ↓
Return Later
 ↓
See Previous Results
```

The intelligence is only one part of the system.

---

# 2. What Makes This an Intelligent Application?

Our application combines several components we already know:

```text
Python
Streamlit
SQL
PostgreSQL
Supabase
Authentication
File Storage
Regex
NLP
Machine Learning
Similarity
OCR
```

Not every feature needs a neural network.

A useful intelligent system can simply:

```text
Read information
Extract information
Compare information
Rank information
Present useful results
```

That is enough for this project.

---

# 3. The Application We Are Building

The AI Career Companion will help a user understand how their resume relates to job descriptions.

A simple version can provide:

```text
Resume
 ↓
Extract skills
 ↓
Store profile
 ↓
Add job descriptions
 ↓
Compare resume with jobs
 ↓
Rank jobs
 ↓
Explain matching skills
```

Eventually:

```text
My Resume
   │
   ├── Skills
   ├── Experience
   └── Education
          │
          ▼
      Job Database
          │
          ├── Job A
          ├── Job B
          └── Job C
          │
          ▼
     Matching Engine
          │
          ▼
       Rankings
```

---

# 4. Start With the Data Model

Before writing AI code, decide what information the application needs.

A simple schema is:

```text
users
profiles
resumes
jobs
matches
```

Conceptually:

```text
users
  │
  ├── profiles
  │
  └── resumes
          │
          └── matches
                  │
                  └── jobs
```

---

# 5. Profiles

A profile contains information about the person:

```text
profile
-----------------------
user_id
first_name
last_name
job_title
```

The profile is not the resume. It is application-level information about the user.

---

# 6. Resumes

A resume record can contain:

```text
resume_id
user_id
filename
storage_path
extracted_text
created_at
```

The actual PDF lives in:

```text
Supabase Storage
```

The database stores its metadata.

```text
resumes table
       │
       └── storage_path
                │
                ▼
        Storage / PDF
```

---

# 7. Jobs

A job record might contain:

```text
job_id
title
company
description
created_at
```

For this introductory project, jobs can simply be entered manually. We do not need to build a job-board crawler yet.

---

# 8. Matches

A match connects a resume with a job:

```text
matches
-------------------------
id
resume_id
job_id
score
created_at
```

We can later add:

```text
matched_skills
missing_skills
explanation
```

---

# 9. Initial Schema

A simplified jobs table:

```sql
CREATE TABLE public.jobs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT,
    description TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

And matches:

```sql
CREATE TABLE public.matches (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    resume_id BIGINT
        REFERENCES public.resumes(id)
        ON DELETE CASCADE,

    job_id BIGINT
        REFERENCES public.jobs(id)
        ON DELETE CASCADE,

    score NUMERIC,

    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

Add RLS policies appropriate to the ownership model before exposing user-owned records.

---

# 10. The User Journey

```text
Create account
      ↓
Login
      ↓
Upload resume
      ↓
Store file
      ↓
Extract text
      ↓
Save resume data
      ↓
Add a job
      ↓
Calculate similarity
      ↓
Store match
      ↓
Return later
      ↓
See previous results
```

---

# 11. The Architecture

```text
                           USER
                             │
                             ▼
                       STREAMLIT UI
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
             AUTH          RESUME          JOBS
              │              │              │
              │              ▼              │
              │          STORAGE            │
              │              │              │
              │              ▼              │
              └────────── POSTGRESQL ───────┘
                             │
                             ▼
                    INTELLIGENCE LAYER
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
           Parsing       Similarity       Ranking
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                           MATCHES
```

---

# 12. Do Not Start With the AI

It is tempting to immediately write:

```python
calculate_similarity(...)
```

But first ask:

```text
Where does the resume come from?
Where is it stored?
Who owns it?
Where are jobs stored?
Where do results go?
```

A useful order is:

```text
Data
 ↓
Application flow
 ↓
Persistence
 ↓
Intelligence
 ↓
UI
```

---

# 13. Reuse Phase 4

We do not need to throw away our previous work.

Our Phase 4 resume parser already taught us how to:

```text
Read documents
Clean text
Use regex
Extract information
Use NLP
Calculate similarity
```

Now turn those pieces into functions:

```python
def extract_resume_text(file):
    ...


def extract_skills(text):
    ...


def calculate_match(resume_text, job_text):
    ...
```

The functions do the intelligence. Supabase and Streamlit provide the surrounding application.

---

# 14. A Useful Separation

Think about four layers:

```text
UI
 ↓
Streamlit

Application Logic
 ↓
Python

Intelligence
 ↓
NLP / ML / OCR / Similarity

Persistence
 ↓
PostgreSQL / Storage
```

This separation makes the project easier to understand and modify.

---

# 15. Resume Processing Pipeline

```text
resume.pdf
     │
     ▼
Storage
     │
     ▼
PDF / Image Processing
     │
     ▼
Text Extraction
     │
     ▼
Text Cleaning
     │
     ▼
Information Extraction
     │
     ▼
Structured Resume
```

For example:

```python
{
    "name": "Alice",
    "email": "alice@example.com",
    "skills": [
        "Python",
        "SQL",
        "Machine Learning"
    ]
}
```

---

# 16. Store the Raw Text Too

Do not only store structured fields.

Keep:

```text
extracted_text
```

as well.

Why? Because we may improve the parser later. If the original text is still stored, we can reprocess it without asking the user to upload the resume again.

---

# 17. Job Processing

A job description can be treated similarly:

```text
Job Description
      ↓
Text Cleaning
      ↓
Skill Extraction
      ↓
Structured Job
```

For example:

```python
{
    "title": "Python Developer",
    "skills": [
        "Python",
        "SQL",
        "Django",
        "PostgreSQL"
    ]
}
```

---

# 18. The First Matching Algorithm

Start with something we already understand:

# Cosine Similarity

```text
Resume text
      ↓
Vector
      │
      │ cosine similarity
      ▼
Job description
      ↓
Vector
```

A natural first implementation is TF-IDF + cosine similarity.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform([
    resume_text,
    job_text
])

score = cosine_similarity(
    vectors[0],
    vectors[1]
)[0][0]
```

---

# 19. Why Start With Something Simple?

We want students to understand the entire system.

Instead of:

```text
magic model
 ↓
score
```

we can see:

```text
Text
 ↓
TF-IDF
 ↓
Vectors
 ↓
Cosine Similarity
 ↓
Ranking
```

Later, embeddings can replace TF-IDF without changing the overall application architecture.

---

# 20. The Score Is Not a Hiring Probability

A score such as:

```text
82%
```

means the chosen text representations were similar according to the algorithm.

It does **not** mean:

```text
82% chance of getting hired
```

or:

```text
82% job eligibility
```

The UI should describe it as a similarity or match score.

---

# 21. Explain the Score

A useful application should show more than a number.

For example:

```text
Match Score: 82%

Strong matches:
✓ Python
✓ SQL
✓ Machine Learning

Potential gaps:
✗ Django
✗ PostgreSQL
```

---

# 22. Skill Matching

Start with simple set logic.

```python
resume_skills = set(resume_skills)
job_skills = set(job_skills)

matched = resume_skills & job_skills
missing = job_skills - resume_skills
```

For example:

```text
Resume:
Python
SQL
Machine Learning
Pandas

Job:
Python
SQL
Machine Learning
Django
PostgreSQL
```

Result:

```text
Matched:
Python
SQL
Machine Learning

Missing:
Django
PostgreSQL
```

---

# 23. Store Match Results

Once we calculate:

```text
score
matched_skills
missing_skills
```

store them.

For example:

```sql
ALTER TABLE public.matches
ADD COLUMN matched_skills JSONB,
ADD COLUMN missing_skills JSONB;
```

Now the application remembers not only the score, but also the explanation.

---

# 24. Job Ranking

Suppose the user has:

```text
Job A → 82%
Job B → 64%
Job C → 91%
Job D → 73%
```

We can rank them:

```text
Job C → 91%
Job A → 82%
Job D → 73%
Job B → 64%
```

The application now helps prioritize jobs instead of merely storing them.

---

# 25. Dashboard

A simple Streamlit dashboard could show:

```text
AI CAREER COMPANION

Welcome, Alice

--------------------------------

My Resume
resume.pdf

--------------------------------

Top Job Matches

Python Developer       91%
ML Engineer             87%
Data Analyst            76%

--------------------------------

Missing Skills

PostgreSQL
Docker
Django
```

That is enough to feel like a real application.

---

# 26. Streamlit Session State vs Database

Streamlit reruns the script from top to bottom when users interact with widgets. Session State can preserve values across reruns for the current user session. citeturn0search1turn0search0

For example:

```python
if "user" not in st.session_state:
    st.session_state.user = None
```

But:

> **Session State is not our database.**

Session State is tied to a browser session and can reset when the session ends or the page is reloaded. citeturn0search0turn0search1

Use:

```text
Session State
```

for temporary UI/session information.

Use:

```text
PostgreSQL
```

for persistent application data.

Use:

```text
Storage
```

for persistent files.

---

# 27. Resume Upload UI

A first version might look like:

```python
uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)
```

Streamlit's uploader keeps uploaded file data in memory; it is not a persistent file store. citeturn0search2turn0search5

Therefore:

```text
uploaded_file
      ↓
Supabase Storage
```

is what gives the resume persistence.

---

# 28. Keep Intelligence Outside the UI

For example:

```python
def process_resume(file_bytes):
    text = extract_text(file_bytes)
    text = clean_text(text)
    skills = extract_skills(text)

    return {
        "text": text,
        "skills": skills
    }
```

Then Streamlit can simply call:

```python
result = process_resume(
    uploaded_file.getvalue()
)
```

The UI remains readable.

---

# 29. Matching Function

Similarly:

```python
def match_resume_to_job(
    resume_text,
    job_text
):
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([
        resume_text,
        job_text
    ])

    score = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]

    return score
```

The UI does not need to know how cosine similarity works.

---

# 30. A Simple Project Structure

As the application grows, split responsibilities into modules:

```text
ai-career-companion/
│
├── app.py
│
├── pages/
│   ├── 1_Resume.py
│   ├── 2_Jobs.py
│   ├── 3_Matches.py
│   └── 4_Profile.py
│
├── services/
│   ├── database.py
│   ├── storage.py
│   ├── resume_parser.py
│   └── matcher.py
│
├── .env
├── requirements.txt
└── README.md
```

Do not create all of these files on day one. Start simple and refactor when the code becomes difficult to manage.

---

# 31. Database Helper

Eventually:

```python
def get_resumes(supabase, user_id):
    return (
        supabase
        .table("resumes")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
```

Then the UI can call:

```python
resumes = get_resumes(
    supabase,
    user.id
)
```

---

# 32. Storage Helper

Similarly:

```python
def upload_resume(
    supabase,
    user_id,
    file_name,
    file_bytes
):
    path = f"{user_id}/{file_name}"

    return (
        supabase
        .storage
        .from_("resumes")
        .upload(
            path,
            file_bytes
        )
    )
```

The UI does not need to know the exact Storage API call.

---

# 33. Add a Job

The user can enter:

```text
Job Title
Company
Description
```

For example:

```text
Python Developer

We are looking for a Python developer
with experience in SQL, Django,
PostgreSQL and machine learning.
```

Then persist the job in PostgreSQL.

---

# 34. Run Matching

When the user clicks:

```text
Analyze Match
```

run:

```text
Retrieve resume
      ↓
Retrieve job
      ↓
Extract text
      ↓
TF-IDF
      ↓
Cosine Similarity
      ↓
Skill comparison
      ↓
Result
```

Then store:

```text
score
matched_skills
missing_skills
```

---

# 35. Match History

Store:

```text
resume_id
job_id
score
matched_skills
missing_skills
created_at
```

Then show:

```text
Match History

Python Developer       91%
ML Engineer             87%
Data Analyst            76%
```

The user can return later and still see the results.

---

# 36. Add EDA

Because the database now contains many jobs and matches, we can reuse our EDA skills.

For example:

```text
Most common skills
Average match score
Jobs by company
Skills missing most often
```

A simple dashboard might show:

```text
Most Requested Skills

Python        74
SQL           68
AWS           52
Docker        47
PostgreSQL    39
```

This turns stored application data into useful career insights.

---

# 37. Optional ML Extension

Once the basic system works, we could experiment with a simple classifier:

```text
Job Description
 ↓
Features
 ↓
Classifier
 ↓
Job Category
```

Possible categories:

```text
Data Science
Machine Learning
Backend
Frontend
DevOps
Data Analytics
```

This is optional. Do not add it until the core application works.

---

# 38. Optional Embeddings

The first matching engine is:

```text
TF-IDF
+
Cosine Similarity
```

Later, students can replace it with:

```text
Embeddings
+
Cosine Similarity
```

The architecture can remain:

```text
resume
 ↓
representation
 ↓
similarity
 ↓
ranking
```

Only the representation changes.

---

# 39. What We Should Not Add Yet

Avoid turning the project into:

```text
LLM chatbot
Agents
Vector databases
Microservices
Kubernetes
Complex CI/CD
```

unless they serve a clear learning objective.

This is still an introductory program.

The goal is to understand:

```text
How a real application is assembled.
```

---

# 40. Minimum Viable Career Companion

The first complete version only needs:

```text
✓ Sign up
✓ Login
✓ Logout
✓ Upload resume
✓ Store resume
✓ Extract resume text
✓ Save resume data
✓ Add jobs
✓ Calculate similarity
✓ Show match score
✓ Show matched skills
✓ Show missing skills
✓ Save match history
```

That is already a substantial project.

---

# 41. Suggested Build Order

Do not build everything at once.

### Version 1

```text
Login
 ↓
Dashboard
```

### Version 2

```text
Upload resume
 ↓
Storage
```

### Version 3

```text
Resume
 ↓
Text extraction
 ↓
Database
```

### Version 4

```text
Add jobs
```

### Version 5

```text
TF-IDF
 ↓
Cosine Similarity
```

### Version 6

```text
Skill matching
```

### Version 7

```text
Match history
```

### Version 8

```text
Dashboard
```

### Version 9

```text
EDA / career insights
```

Each version should still work before the next feature is added.

---

# 42. The Finished Introductory Architecture

```text
                              USER
                                │
                                ▼
                         STREAMLIT APP
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
        AUTH                 RESUME                  JOBS
          │                     │                     │
          │                     ▼                     │
          │                  STORAGE                  │
          │                     │                     │
          │                     ▼                     │
          └─────────────── POSTGRESQL ────────────────┘
                                │
                                ▼
                       RESUME INTELLIGENCE
                                │
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
              OCR /         NLP / Regex     Similarity
              Parsing          Skills        TF-IDF
                 │              │            Cosine
                 └──────────────┼──────────────┘
                                ▼
                             MATCHES
                                │
                                ▼
                           DASHBOARD
                                │
                                ▼
                          CAREER INSIGHTS
```

---

# 43. What Students Have Actually Learned

This one project now uses almost the entire curriculum.

### Python

```text
Functions
Modules
File handling
Exceptions
Data structures
```

### EDA

```text
Data exploration
Statistics
Skill distributions
Career insights
```

### ML

```text
TF-IDF
Similarity
Ranking
Optional classification
```

### DL

```text
Optional document intelligence
```

### CV

```text
OpenCV
Image preprocessing
OCR
```

### NLP

```text
Regex
Tokenization
Text cleaning
Information extraction
```

### Software

```text
Streamlit
SQL
PostgreSQL
Supabase
Authentication
Storage
RLS
```

---

# 44. The Most Important Lesson

The biggest lesson is not how to use one particular library.

> **A real application is a collection of smaller systems working together.**

For example:

```text
Authentication
```

solves identity.

```text
PostgreSQL
```

solves structured persistence.

```text
Storage
```

solves files.

```text
Python
```

solves application logic.

```text
ML / NLP / CV
```

solve intelligence problems.

```text
Streamlit
```

solves the interface.

The application emerges from connecting them.

---

# 45. This Is Not Production Software

The purpose of this phase is not to build a production HR platform.

We are building a learning project that is:

```text
Small enough to understand
Large enough to integrate concepts
Simple enough to debug
Interesting enough to build
```

That is the sweet spot.

---

# 46. Final Challenge

Once the basic Career Companion works, change something yourself.

For example:

```text
Add job categories
```

or:

```text
Add a skill-gap chart
```

or:

```text
Allow multiple resumes
```

or:

```text
Compare two resumes
```

or:

```text
Add job search history
```

Before searching for a tutorial, ask:

```text
What data do I need?
Where should it live?
What function should perform the logic?
What should the UI display?
What SQL changes are required?
```

Then search the documentation for the specific problem.

---

# 47. Independent Engineering Workflow

Use the workflow:

```text
IDEA
 ↓
Break into smaller problem
 ↓
Identify data
 ↓
Design schema
 ↓
Write small function
 ↓
Test it
 ↓
Connect to application
 ↓
Commit to Git
 ↓
Iterate
```

This connects directly back to the developer workflow introduced earlier in the curriculum.

---

# 48. Final Takeaway

We started Phase 5 with:

```text
How does an application remember?
```

We learned:

```text
SQL
 ↓
PostgreSQL
```

Then:

```text
How do users identify themselves?
```

We learned:

```text
Authentication
 ↓
Authorization
 ↓
RLS
```

Then:

```text
Where do files live?
```

We learned:

```text
Supabase Storage
```

And now:

```text
How do all of these pieces work together?
```

We build:

# AI Career Companion

```text
User
 ↓
Auth
 ↓
Resume
 ↓
Storage
 ↓
Parsing
 ↓
NLP
 ↓
Matching
 ↓
Database
 ↓
Ranking
 ↓
Dashboard
```

This is the point of Phase 5.

Not to learn one more library.

But to learn how to **assemble the things you already know into software that people can actually use.**
