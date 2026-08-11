# Project 4.2 — Deploying an Intelligent Application

## From `localhost` to a Real Application

Our application now works locally.

We can run:

```bash
streamlit run app.py
```

and open it in a browser.

But there is a difference between:

```text
"I can run my application."
```

and:

```text
"Someone else can use my application."
```

Deployment is the process of taking our application from a development environment and making it available in another environment where users can run it.

The goal of this module is not to memorize one hosting platform.

The goal is to understand what happens when software leaves our laptop.

---

# 1. Local Development

Until now, our workflow has been:

```text
Write code
   ↓
Run locally
   ↓
Open localhost
   ↓
Test
   ↓
Change code
```

For Streamlit:

```bash
streamlit run app.py
```

The application runs on our machine.

Conceptually:

```text
Your Computer

┌──────────────────────────────┐
│                              │
│  Python                      │
│  Dependencies                │
│  AI Model                    │
│  Streamlit                   │
│  app.py                      │
│                              │
└──────────────┬───────────────┘
               │
               ▼
           localhost
```

Nobody else can automatically use that application simply because it works on your computer.

---

# 2. What Deployment Changes

With deployment:

```text
Your Computer
     ↓
Git Repository
     ↓
Deployment Environment
     ↓
Running Application
     ↓
Users
```

The deployment environment needs to recreate enough of our project to run it.

That means it needs:

```text
Python
+
Dependencies
+
Source Code
+
Configuration
+
Models / Model Access
```

---

# 3. "Works on My Machine"

This is one of the most common software problems.

You might have:

```text
Python 3.12
```

installed locally.

Another machine might have:

```text
Python 3.10
```

Your laptop may already have:

```text
Tesseract
```

installed.

The deployment server may not.

You may have installed:

```text
some-package
```

months ago without recording it.

The deployment environment doesn't know about it.

Therefore:

> A project should explicitly describe what it needs.

---

# 4. `requirements.txt`

We have already seen:

```text
requirements.txt
```

For example:

```text
streamlit
scikit-learn
sentence-transformers
beautifulsoup4
```

The deployment environment can install:

```bash
pip install -r requirements.txt
```

Now the machine has the Python dependencies required by the application.

---

# 5. Why Requirements Matter

Imagine our application imports:

```python
import streamlit
import sklearn
import cv2
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
```

If the deployment environment doesn't have these packages:

```text
ModuleNotFoundError
```

The application cannot start.

A requirements file turns:

```text
"Install whatever I happen to have."
```

into:

```text
"Install these declared dependencies."
```

---

# 6. System Dependencies Are Different

Python packages are only one type of dependency.

Remember our OCR project.

It may require:

```text
Python package
+
external OCR engine
```

For example:

```text
pytesseract
```

is a Python interface.

It does not itself contain the complete OCR engine.

This distinction is important:

```text
Python dependency
```

versus:

```text
System dependency
```

---

# 7. Dependency Layers

Our application can therefore depend on:

```text
Application Code
       ↓
Python Packages
       ↓
System Libraries / Programs
       ↓
Operating System
       ↓
Hardware
```

For example:

```text
Streamlit
   ↓
Python
   ↓
sentence-transformers
   ↓
PyTorch
   ↓
Operating System
```

A deployment environment needs to satisfy the relevant layers.

---

# 8. Large AI Dependencies

Embedding models can introduce another issue.

Our code might contain:

```python
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
```

The first run may download model files.

So deployment involves more than:

```text
pip install
```

We also need to think about:

```text
model availability
download time
disk space
memory
startup time
network access
```

---

# 9. Model Download vs Model File

There are two broad approaches.

### Approach A

Let the application download the model when it starts.

```text
Application starts
      ↓
Download model
      ↓
Load model
      ↓
Ready
```

### Approach B

Provide/cache the model as part of the deployment process.

```text
Deployment
    ↓
Model already available
    ↓
Application starts
```

The correct approach depends on:

```text
platform
model size
deployment strategy
licensing
startup requirements
```

The important lesson is to recognize that **models are dependencies too**.

---

# 10. Cold Start

Suppose our application starts.

It needs:

```text
Python
 ↓
Packages
 ↓
Embedding model
 ↓
OCR components
 ↓
Application
```

The first startup may take significantly longer than later requests.

This is often called a:

> **Cold start**

Caching can reduce repeated initialization.

---

# 11. Streamlit Caching

We previously used:

```python
@st.cache_resource
def load_model():

    return SentenceTransformer(
        MODEL_NAME
    )
```

This is useful in deployment too.

We want:

```text
First initialization
      ↓
Load model
      ↓
Cache model
```

rather than repeatedly loading it unnecessarily.

---

# 12. Application State

We should understand what can persist between interactions.

For example:

```text
Uploaded resume
Parsed resume
Embedding
```

may be expensive to recompute.

Streamlit provides mechanisms for caching resources and data.

The important design question is:

> What can safely be reused?

---

# 13. Deployment Configuration

Some values should be configurable without changing source code.

For example:

```text
MODEL_NAME
SEMANTIC_THRESHOLD
MAX_FILE_SIZE
```

We could put them in:

```text
config.py
```

But deployment environments often provide:

```text
environment variables
```

Conceptually:

```text
Environment
   ↓
Configuration
   ↓
Application
```

---

# 14. Environment Variables

Python can read environment variables:

```python
import os

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "all-MiniLM-L6-v2"
)
```

This means:

```text
If MODEL_NAME exists:
    use it

Otherwise:
    use the default
```

This is useful when deployment settings differ from local settings.

---

# 15. Secrets Are Different

Suppose a future version of the application uses:

```text
API_KEY
```

We should not write:

```python
API_KEY = "my-secret-key"
```

into source code.

And definitely don't commit:

```text
.env
```

containing secrets.

Instead:

```text
Deployment platform
      ↓
Secret configuration
      ↓
Environment variable
      ↓
Application
```

---

# 16. `.env` During Local Development

For local development, developers often use:

```text
.env
```

For example:

```text
API_KEY=...
```

Then:

```text
.env
```

belongs in:

```text
.gitignore
```

The principle is:

> Configuration can be stored separately from source code, and secrets should not be committed to the repository.

---

# 17. Git Becomes Important

Deployment works especially naturally when the project is tracked with Git.

Our workflow becomes:

```text
Developer
   ↓
Code
   ↓
Git commit
   ↓
Git repository
   ↓
Deployment system
```

The repository becomes the source from which the deployment environment builds the application.

---

# 18. The Deployment Pipeline

A simplified deployment process looks like:

```text
Git Repository
      ↓
Clone repository
      ↓
Create environment
      ↓
Install dependencies
      ↓
Configure environment
      ↓
Start application
      ↓
Application available
```

This is the basic idea behind many deployment systems.

---

# 19. Manual vs Automatic Deployment

### Manual

You:

```text
change code
 ↓
build
 ↓
upload
 ↓
restart application
```

### Automated

You:

```text
git push
   ↓
deployment system
   ↓
build
   ↓
test
   ↓
deploy
```

The second approach is the beginning of:

> **Continuous Integration / Continuous Deployment**

We don't need to build a sophisticated CI/CD system yet.

Students should understand the concept.

---

# 20. Deployment Platforms

A Streamlit application can be deployed using a platform that supports Python applications.

The exact platform is less important for this lesson than understanding the common requirements:

```text
Repository
Requirements
Entry point
Environment configuration
Runtime
Resources
```

For an educational project, choose a platform that makes these concepts visible without requiring a large infrastructure setup.

---

# 21. Entry Point

The deployment environment needs to know:

> What should I run?

For our project:

```bash
streamlit run app.py
```

is the entry point.

This is conceptually similar to:

```text
main()
```

in a traditional program.

The deployment environment needs to know how to start the application.

---

# 22. Port and Network

Locally:

```text
localhost
```

is enough.

On a deployed machine, the application must listen in a way that the hosting environment can expose to users.

The deployment platform often handles the networking layer.

The important concept is:

```text
Application
    ↓
Server process
    ↓
Network
    ↓
User browser
```

Students don't need to become network engineers to understand this flow.

---

# 23. Localhost vs Public Application

Locally:

```text
Browser
   ↓
localhost
   ↓
Your laptop
```

Deployed:

```text
Browser
   ↓
Internet
   ↓
Hosting environment
   ↓
Python process
   ↓
Streamlit
```

That is the conceptual transition.

---

# 24. File Uploads in a Deployed Application

Our application accepts:

```text
Resume file
```

Locally, we might not think much about this.

In deployment, ask:

```text
How large can the file be?

Where is it stored?

How long is it stored?

Is it deleted?

How many users can upload simultaneously?

```

These are software design questions.

---

# 25. Don't Assume Local Files Persist

A common mistake is:

```python
with open(
    "uploaded_resume.pdf",
    "wb"
) as file:
    ...
```

and then assuming that file will permanently exist.

Depending on the deployment environment, local storage may be:

```text
temporary
ephemeral
container-specific
```

Therefore:

> Don't build a persistent data-storage strategy around temporary application files.

---

# 26. Temporary Files

If OCR requires a physical file, a better design may be:

```text
Upload
 ↓
Temporary file
 ↓
OCR
 ↓
Extract text
 ↓
Delete temporary file
```

This reduces unnecessary retention of personal documents.

It is also cleaner from a privacy perspective.

---

# 27. Resource Limits

Your laptop might have:

```text
16 GB RAM
```

A small deployment environment may have much less.

Your local machine may have:

```text
powerful CPU
```

while the deployment environment has:

```text
limited CPU
```

Therefore:

> A model that runs locally does not automatically mean it is suitable for every deployment environment.

---

# 28. Large Models Change the Deployment Problem

Suppose we replace:

```text
all-MiniLM-L6-v2
```

with a much larger model.

We may encounter:

```text
More memory
More startup time
More storage
More computation
Higher cost
```

This introduces a real engineering trade-off:

```text
Model quality
       ↕
Resource requirements
```

There is rarely a completely free upgrade.

---

# 29. Measure Before Optimizing

We can measure:

```text
Startup time
OCR time
Embedding time
Matching time
Memory usage
```

For example:

```text
Startup:
4.2 seconds

OCR:
2.1 seconds

Embedding:
0.8 seconds

Matching:
0.1 seconds
```

Now we know where optimization might matter.

---

# 30. Deployment Is an Experiment

Try deploying the application.

Then observe:

```text
Does it start?
Does the model load?
Does OCR work?
Can users upload files?
Is processing fast enough?
Does the UI behave correctly?
```

Deployment itself becomes another iteration loop:

```text
Deploy
 ↓
Test
 ↓
Observe
 ↓
Fix
 ↓
Commit
 ↓
Redeploy
```

---

# 31. Production-Like Error Handling

A deployed application should not expose internal details unnecessarily.

Instead of showing:

```text
FileNotFoundError:
[long traceback]
```

the user might see:

```text
We couldn't process this document.

Please try another file.
```

Meanwhile, logs can contain:

```text
ERROR: OCR processing failed
```

This separation is important.

---

# 32. Logging in Deployment

Logs become especially useful after deployment.

Locally:

```python
print("processing")
```

might be enough.

But when a user reports:

> "The application failed."

you need to know:

```text
When?
What stage?
Which component?
What exception?
```

Structured logging becomes increasingly valuable as applications grow.

---

# 33. Don't Log Sensitive Documents

Remember:

```text
Resume
```

may contain personal information.

Avoid:

```python
logger.info(
    resume_text
)
```

Prefer:

```python
logger.info(
    "Resume processed successfully"
)
```

or:

```python
logger.info(
    "Resume contained %d characters",
    len(resume_text)
)
```

Logging should help diagnose the application without unnecessarily collecting user data.

---

# 34. Security Basics

Even a simple student project should consider:

```text
Input validation
File validation
Secret management
Dependency updates
Privacy
Error handling
```

For example, don't assume that:

```text
filename.endswith(".pdf")
```

proves the uploaded file is a safe PDF.

File handling should be treated as an external input boundary.

---

# 35. External Input Is Untrusted

This is an important software principle:

> Anything supplied by a user should be treated as untrusted input.

That includes:

```text
Files
Text
Filenames
URLs
Form fields
```

Our application should validate what it expects.

---

# 36. Limit Uploaded Files

A practical application may impose:

```text
Maximum file size
```

and accepted types:

```text
PDF
PNG
JPG
JPEG
```

This protects the application from unnecessarily expensive processing.

For example:

```text
500 MB image
```

should not casually enter an OCR pipeline designed for:

```text
2 MB resume
```

---

# 37. Protect Expensive Operations

Some operations are expensive:

```text
OCR
Embedding
Large file processing
```

We should avoid repeating them unnecessarily.

For example:

```text
User clicks Analyze
        ↓
OCR
        ↓
Embedding
```

If the same input is submitted again:

```text
Can we reuse previous work?
```

This is where caching and application state become useful.

---

# 38. Deployment and Caching

Our model:

```python
@st.cache_resource
```

can be cached.

Data transformations can potentially be cached too.

But be careful:

> Cache only data that is safe and appropriate to reuse.

For example, caching a public job description is very different from globally caching a user's private resume data.

---

# 39. Privacy-Aware Caching

Ask:

```text
Who can access the cached object?

How long does it remain?

Can another user receive it?

Does the framework isolate sessions?
```

The technical feature:

```text
cache
```

is not automatically safe for every kind of data.

This is an important distinction between:

```text
performance engineering
```

and:

```text
privacy engineering
```

---

# 40. Environment-Specific Configuration

Our application may have:

```text
Development
Testing
Production
```

Each environment may need different settings.

For example:

```text
Development:
DEBUG-like logging

Testing:
Small test model / dataset

Production:
Normal logging
Production model
```

We don't need a complicated configuration system yet.

Students should understand the principle:

> The same application code may run with different configuration.

---

# 41. Development Workflow

Our local development workflow becomes:

```text
Edit
 ↓
Run locally
 ↓
pytest
 ↓
Evaluate
 ↓
Git commit
```

Then:

```text
Push
 ↓
Deploy
 ↓
Smoke test
 ↓
Observe
```

---

# 42. What Is a Smoke Test?

A smoke test is a quick test asking:

> Does the deployed application basically work?

For our project:

```text
Open application
 ↓
Upload sample resume
 ↓
Paste sample job
 ↓
Click Analyze
 ↓
Check result
```

If this works, the deployment is at least alive.

It does not prove everything works.

It is simply a fast sanity check.

---

# 43. Deployment Checklist

Before sharing the application:

```text
□ requirements.txt exists
□ application starts
□ model loads
□ OCR works
□ file upload works
□ empty inputs handled
□ errors handled
□ no secrets in Git
□ .gitignore configured
□ tests pass
□ evaluation completed
□ file limits considered
□ privacy considered
□ README updated
```

---

# 44. README Deployment Instructions

Update:

```text
README.md
```

with:

```markdown
# Resume Job Matcher

## Run locally

pip install -r requirements.txt

streamlit run app.py

## Run tests

pytest

## Architecture

Resume
→ OCR
→ Parser
→ Embeddings
→ Matching
→ Score
→ Streamlit
```

Then add:

```markdown
## Deployment

Describe the deployment platform,
required configuration, and startup command.
```

A user should not have to guess how to run the project.

---

# 45. The Deployment Artifact

What are we actually deploying?

Not just:

```text
app.py
```

We are deploying:

```text
Source Code
+
Dependencies
+
Configuration
+
Models / Model Access
+
Runtime Instructions
```

This is a useful mental model.

---

# 46. Containerization — Optional Next Step

A common way to package applications is:

```text
Docker
```

Conceptually:

```text
Application
+
Dependencies
+
Runtime
        ↓
Container
```

This can make environments more reproducible.

But students do not need to master Docker to understand deployment.

Treat it as the next layer of software engineering.

---

# 47. What Docker Solves

Without containerization:

```text
Machine A
Python 3.x
Package versions...
System libraries...
```

versus:

```text
Machine B
Python 3.y
Different packages...
Different system libraries...
```

With a container:

```text
Application
+
Defined runtime
+
Defined dependencies
```

can be packaged together.

The underlying infrastructure still matters, but the environment becomes more controlled.

---

# 48. Why We Are Not Starting With Docker

The educational progression matters.

Students should first understand:

```text
What does the application need?
```

before learning:

```text
How do I package the application into a container?
```

Otherwise Docker becomes:

```text
Copy Dockerfile
Run command
Hope it works
```

Instead, we want students to understand what the Dockerfile is actually describing.

---

# 49. Deployment Architecture

Our application has now evolved into:

```text
                    INTERNET
                       │
                       ▼
                  Web Browser
                       │
                       ▼
                Hosting Platform
                       │
            ┌──────────┴──────────┐
            │                     │
            ▼                     ▼
        Streamlit             Runtime
            │                     │
            └──────────┬──────────┘
                       ▼
                  Application
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
       OCR          Embeddings     Matching
         │             │             │
         └─────────────┼─────────────┘
                       ▼
                  Match Report
```

This is no longer just a Python file.

It is a deployed system.

---

# 50. Deployment Changes Our Definition of "Done"

Earlier:

```text
Code runs
```

might have meant:

```text
Done
```

Now:

```text
Done
```

means:

```text
Code works
+
Tests pass
+
Evaluation is acceptable
+
Dependencies declared
+
Configuration understood
+
Errors handled
+
Application deploys
+
Smoke test passes
```

This is a major shift in engineering maturity.

---

# 51. Deployment Exercise

Take the resume-job matcher and deploy it.

Your goal is to produce:

```text
Public Application
```

that allows someone to:

```text
1. Upload a resume
2. Enter a job description
3. Analyze the match
4. See matched skills
5. See semantic matches
6. See missing skills
7. See the final score
```

Then ask another person to use it without explaining the code.

Observe where they get confused.

That feedback is part of the next iteration.

---

# 52. Deployment Evaluation

After deployment, test:

```text
Fresh browser
Different machine
Different file
Empty job description
Large document
Image resume
PDF resume
```

Record:

```text
Works
Fails
Slow
Confusing
```

Then improve the application.

---

# 53. Final Git Checkpoint

Once deployment works:

```bash
git status
```

Run:

```bash
pytest
```

Then:

```bash
git add .
```

Commit:

```bash
git commit -m "Prepare intelligent application for deployment"
```

Now Git represents a deployable milestone.

---

# 54. The Complete Phase 4 Workflow

We have now reached:

```text
Experiment
   ↓
Build
   ↓
Refactor
   ↓
Test
   ↓
Evaluate
   ↓
Deploy
   ↓
Observe
   ↓
Improve
```

Compare this with where we started:

```text
Jupyter Cell

1 + 2
```

That tiny experiment eventually became:

```text
Intelligent Software
```

with:

```text
Python
OCR
Regex
NLP
ML
DL
Embeddings
Computer Vision
Streamlit
Testing
Git
Deployment
```

---

# 55. Final Mental Model

The final lesson is not:

> "How to deploy Streamlit."

The lesson is:

> **Software has a lifecycle.**

```text
Idea
 ↓
Experiment
 ↓
Prototype
 ↓
Application
 ↓
Test
 ↓
Evaluate
 ↓
Deploy
 ↓
Monitor
 ↓
Iterate
```

AI applications follow the same lifecycle.

The AI model is only one part of that system.

---

# 56. Phase 4 Capstone

At the end of Phase 4, students should have a repository that looks approximately like:

```text
resume-job-matcher/
│
├── app.py
│
├── document_reader.py
├── resume_parser.py
├── job_parser.py
├── semantic_matcher.py
├── job_matcher.py
├── scoring.py
├── config.py
│
├── tests/
│   ├── test_resume_parser.py
│   ├── test_job_parser.py
│   ├── test_matcher.py
│   └── test_scoring.py
│
├── data/
│   └── evaluation/
│
├── requirements.txt
├── .gitignore
├── README.md
└── deployment configuration
```

And the deployed system:

```text
Resume
   ↓
Document Reader
   ↓
Resume Parser
   ↓
Semantic Representation
   ↓
Job Parser
   ↓
Matching
   ↓
Scoring
   ↓
Explanation
   ↓
Streamlit
   ↓
User
```

---

# 57. The End of the Project

We began by asking:

> How do computers read a resume?

Then:

> How do they extract information?

Then:

> How can they compare text?

Then:

> How can they understand semantic relationships?

Then:

> How can we compare a resume with a job?

And finally:

> How do we turn all of that into reliable software that another person can actually use?

That last question is the essence of Phase 4.

---

# 58. Final Takeaway

An intelligent application is not:

```text
AI Model
```

It is:

```text
                Intelligent Application

Data
 +
Preprocessing
 +
Representation
 +
Model
 +
Rules
 +
Evaluation
 +
Error Handling
 +
Testing
 +
Interface
 +
Deployment
 +
Iteration
```

The model may be the most exciting part.

But the surrounding engineering is what turns it into software.

And that is the final lesson:

> **Don't just build models. Build systems.**
