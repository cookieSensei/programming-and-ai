# Project 4 — Turning the AI Project Into Software

## From a Working Prototype to an Intelligent Application

We have built a working resume-to-job matching system.

So far, our development process has looked roughly like:

```text
Experiment
   ↓
Notebook
   ↓
Python Script
   ↓
Prototype
   ↓
Streamlit Application
```

The application can now:

```text
Read documents
Extract text
Parse resumes
Extract skills
Create embeddings
Compare resumes and jobs
Generate match scores
Display results
```

That is already a substantial project.

But there is a difference between:

> **A program that works**

and:

> **A piece of software that other people can reliably use.**

This project is about closing that gap.

We are not introducing another major AI technique.

Instead, we are going to improve the system around the AI.

---

# 1. The Prototype Problem

Imagine our application currently consists of:

```text
app.py
```

with hundreds of lines of code:

```python
load model
read file
run OCR
parse resume
extract skills
parse job
calculate embeddings
calculate similarity
calculate score
display everything
```

It might work.

But what happens when:

```text
OCR fails?
```

What happens when:

```text
the user uploads the wrong file?
```

What happens when:

```text
the embedding model cannot be downloaded?
```

What happens when:

```text
the job description is empty?
```

What happens when:

```text
the model takes 10 seconds to load?
```

What happens when:

```text
we want to replace the embedding model?
```

What happens when:

```text
we want to test the parser without opening Streamlit?
```

These are software engineering problems.

---

# 2. The New Goal

Our goal is to transform:

```text
AI Prototype
```

into:

```text
Reliable Intelligent Application
```

The architecture will become:

```text
                    Streamlit UI
                         │
                         ▼
                  Application Layer
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
        Document      Resume       Job
        Reader        Parser      Parser
             │           │           │
             └───────────┼───────────┘
                         ▼
                  Matching Engine
                         │
                         ▼
                    AI Models
                         │
                         ▼
                   Match Report
```

Each component has one primary responsibility.

---

# 3. Why Architecture Matters

Suppose OCR code is mixed directly into:

```python
st.button(...)
```

and:

```python
st.file_uploader(...)
```

Then the OCR system becomes tied to the UI.

That makes testing difficult.

Instead:

```text
UI
 ↓
document_reader.py
 ↓
text
```

The UI doesn't need to know how OCR works.

This is called **separation of concerns**.

---

# 4. Separate the Application Into Modules

Our project should evolve toward:

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
│
├── config.py
│
├── tests/
│   ├── test_resume_parser.py
│   ├── test_job_parser.py
│   ├── test_matcher.py
│   └── test_scoring.py
│
├── data/
│   └── test_cases/
│
├── requirements.txt
├── README.md
└── .gitignore
```

Now each file has a clear purpose.

---

# 5. What Should `app.py` Do?

Ideally:

```text
app.py
```

should primarily coordinate the application.

For example:

```python
resume_file = st.file_uploader(...)

job_text = st.text_area(...)

if st.button("Analyze"):

    text = process_document(
        resume_file
    )

    resume = parse_resume(
        text
    )

    result = match_resume_to_job(
        text,
        resume,
        job_text
    )

    display_result(
        result
    )
```

The details should live elsewhere.

---

# 6. The Application Layer

We can think of `app.py` as an orchestrator.

It says:

```text
Get input
 ↓
Call component
 ↓
Call component
 ↓
Call component
 ↓
Display result
```

It should not contain every implementation detail.

This makes the application easier to understand.

---

# 7. Configuration

Our application currently contains things such as:

```python
MODEL_NAME = "all-MiniLM-L6-v2"
```

and perhaps:

```python
THRESHOLD = 0.60
```

and:

```python
SKILL_WEIGHT = 0.60
```

Instead of scattering these values throughout the project, create:

```text
config.py
```

For example:

```python
MODEL_NAME = "all-MiniLM-L6-v2"

SEMANTIC_THRESHOLD = 0.60

SKILL_WEIGHT = 0.60
SEMANTIC_WEIGHT = 0.25
DOCUMENT_WEIGHT = 0.15
```

Now our configuration is centralized.

---

# 8. Why Configuration Matters

Suppose we want to experiment with:

```text
0.60
```

versus:

```text
0.70
```

If the threshold appears in five files, changing it becomes error-prone.

If it appears in:

```python
config.py
```

we change one place.

This is another form of separation of concerns.

---

# 9. Environment Variables

Some settings should not be stored directly in source code.

For example:

```text
API keys
database passwords
deployment configuration
```

For this project, we may not need secret credentials.

But students should learn the distinction:

```text
Application configuration
```

versus:

```text
Secrets
```

Never commit secrets to Git.

---

# 10. `.gitignore`

Create:

```text
.gitignore
```

A basic version might contain:

```text
__pycache__/
*.pyc
.venv/
venv/
.env
.DS_Store
```

If the application creates temporary files, add those too.

The purpose is:

> Keep generated, local, or sensitive files out of the repository.

---

# 11. Requirements

Our application depends on libraries.

For example:

```text
streamlit
scikit-learn
sentence-transformers
beautifulsoup4
```

and the OCR dependencies from Project 1.

Create or update:

```text
requirements.txt
```

Then another developer can install them with:

```bash
pip install -r requirements.txt
```

This is a small but important step toward reproducibility.

---

# 12. Virtual Environments

A project should ideally use its own environment.

For example:

```bash
python -m venv .venv
```

Activate it according to your operating system.

Then:

```bash
pip install -r requirements.txt
```

Now the project dependencies are isolated from the rest of the computer.

---

# 13. Model Loading

Embedding models can be expensive to load.

We don't want:

```text
Every button click
      ↓
Load model
      ↓
Run analysis
```

Instead:

```text
Application starts
      ↓
Load model once
      ↓
Reuse model
```

With Streamlit:

```python
@st.cache_resource
def load_model():

    return SentenceTransformer(
        MODEL_NAME
    )
```

Then:

```python
model = load_model()
```

---

# 14. Why Caching Matters

Without caching:

```text
User clicks Analyze
        ↓
Load model
        ↓
Analyze
```

Again:

```text
User changes input
        ↓
Load model again
        ↓
Analyze
```

With caching:

```text
First run
 ↓
Load model
 ↓
Cache model

Later runs
 ↓
Reuse model
```

This can dramatically improve the user experience.

---

# 15. Error Handling

Real applications fail.

For example:

```python
text = process_document(
    uploaded_file
)
```

might fail.

We shouldn't let the entire application crash with an obscure traceback.

We can handle expected failures:

```python
try:

    text = process_document(
        uploaded_file
    )

except Exception as error:

    st.error(
        "Could not process the document."
    )
```

During development, we should also log the actual error.

---

# 16. Don't Hide Every Error

This is a common beginner mistake:

```python
try:
    ...
except:
    pass
```

Now the application silently ignores problems.

The user sees:

```text
Nothing happened.
```

and we have no idea why.

Instead:

```python
except Exception as error:

    logger.exception(
        "Document processing failed"
    )

    st.error(
        "Could not process the document."
    )
```

The user gets a useful message.

The developer gets the technical details.

---

# 17. Logging

Python provides:

```python
import logging
```

We can configure:

```python
logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(
    __name__
)
```

Then:

```python
logger.info(
    "Processing resume"
)
```

or:

```python
logger.info(
    "Extracted %d characters",
    len(text)
)
```

And errors:

```python
logger.exception(
    "Resume processing failed"
)
```

---

# 18. Why Logging Is Better Than Print

We used:

```python
print()
```

throughout our early experiments.

That's fine for learning.

But applications benefit from:

```python
logging
```

because we can control:

```text
INFO
WARNING
ERROR
DEBUG
```

and configure where logs go.

This becomes particularly useful once an application is deployed.

---

# 19. Validate Inputs

Suppose the user clicks:

```text
Analyze
```

without uploading a resume.

We should detect that first.

```python
if resume_file is None:

    st.warning(
        "Please upload a resume."
    )

    st.stop()
```

Similarly:

```python
if not job_text.strip():

    st.warning(
        "Please enter a job description."
    )

    st.stop()
```

Good applications validate input before doing expensive work.

---

# 20. Validate the Extracted Text

A file may technically upload successfully but produce no useful text.

For example:

```python
text = process_document(...)
```

could return:

```text
""
```

Then:

```python
parse_resume("")
```

doesn't make much sense.

So:

```python
if not text.strip():

    st.error(
        "No readable text was found."
    )

    st.stop()
```

This is another example of defensive programming.

---

# 21. Data Validation

Our parser returns a dictionary:

```python
{
    "name": ...,
    "email": ...,
    "skills": ...
}
```

As projects grow, dictionaries can become difficult to reason about.

For example, one function might expect:

```python
"skills"
```

while another accidentally produces:

```python
"skill"
```

We can eventually introduce structured models.

For example, with Python's:

```python
dataclasses
```

or a validation library such as:

```text
Pydantic
```

For this project, students should first understand the problem before introducing another dependency.

---

# 22. A Simple Dataclass

Python provides:

```python
from dataclasses import dataclass
```

We could define:

```python
@dataclass
class Resume:

    name: str | None

    email: str | None

    phone: str | None

    skills: list[str]
```

Now our application has a clear representation of a resume.

Instead of:

```python
resume["skills"]
```

we can eventually use:

```python
resume.skills
```

This becomes increasingly useful as the project grows.

---

# 23. Structured Match Results

We can do the same for the match result.

For example:

```python
@dataclass
class MatchResult:

    final_score: float

    matched_skills: list[str]

    missing_skills: list[str]

    semantic_matches: list[dict]
```

Now the application has an explicit data contract.

This makes the code easier to reason about.

---

# 24. Testing

We have already created evaluation examples.

Now we should turn some of them into automated tests.

Install:

```text
pytest
```

Then create:

```text
tests/
```

---

# 25. Test the Email Parser

Create:

```text
tests/test_resume_parser.py
```

For example:

```python
from resume_parser import extract_email


def test_extract_email():

    text = """
    John Smith
    john@example.com
    """

    assert extract_email(text) == (
        "john@example.com"
    )
```

Run:

```bash
pytest
```

If the test passes:

```text
PASSED
```

If we accidentally break the parser:

```text
FAILED
```

Now our software can detect regressions automatically.

---

# 26. Test Missing Email

```python
def test_missing_email():

    text = """
    John Smith
    Python Developer
    """

    assert extract_email(text) is None
```

This is important.

We don't only test:

```text
happy path
```

We also test:

```text
failure cases
```

---

# 27. Test Skill Extraction

```python
def test_extract_skills():

    text = """
    Python developer
    with SQL experience.
    """

    skills = extract_skills(
        text
    )

    assert "Python" in skills
    assert "SQL" in skills
```

Now our skill extraction has an automated contract.

---

# 28. Test the Matcher

Create:

```text
tests/test_matcher.py
```

We can test deterministic portions first.

For example:

```python
def test_exact_skill_match():

    resume = {
        "python",
        "sql"
    }

    job = {
        "python",
        "sql",
        "aws"
    }

    matched, missing = (
        match_exact_skills(
            resume,
            job
        )
    )

    assert matched == {
        "python",
        "sql"
    }

    assert missing == {
        "aws"
    }
```

This is easier to test than embedding-based behavior.

---

# 29. Don't Over-Test Model Internals

We should not write a test like:

```python
assert embedding_score == 0.7348291
```

Why?

Because changing the model version or text preprocessing may legitimately change the score.

Instead, test the behavior we care about.

For example:

```text
A clearly related pair
should rank higher than
an obviously unrelated pair.
```

This is a more robust test.

---

# 30. Model Evaluation vs Software Testing

These are related but different.

### Software test

Asks:

> Does this function behave according to its contract?

### Model evaluation

Asks:

> Does this model/system perform well on representative data?

For example:

```text
pytest
```

tests code behavior.

Whereas:

```text
precision / recall / F1
```

evaluate extraction or matching quality.

We need both.

---

# 31. Add a Test Dataset

Our project should contain a small evaluation set:

```text
data/
└── test_cases/
    ├── strong_match/
    ├── partial_match/
    └── weak_match/
```

Keep this separate from:

```text
tests/
```

because:

```text
tests/
```

contains executable software tests.

While:

```text
data/
```

contains examples used to evaluate application behavior.

---

# 32. Reproducibility

Suppose someone clones the repository.

They should be able to understand:

```text
What Python version?
What dependencies?
What model?
What configuration?
How do I run it?
How do I test it?
```

This information belongs in:

```text
README.md
```

---

# 33. Write the README

At minimum:

```markdown
# Resume Job Matcher

## Installation

pip install -r requirements.txt

## Run

streamlit run app.py

## Test

pytest

## Architecture

Resume
→ OCR
→ Parser
→ Embeddings
→ Matching
→ Streamlit
```

Also explain:

```text
Limitations
Evaluation
Model
Configuration
```

A README is part of the software.

---

# 34. The Difference Between a Notebook and an Application

Think back to Phase 0.

We started with:

```text
Jupyter Notebook

1 + 2
```

Then:

```text
app.py

print(1 + 2)
```

Then:

```text
Git
 ↓
Checkpoint
```

Now our application has evolved into:

```text
Multiple modules
        +
Tests
        +
Configuration
        +
Models
        +
UI
        +
Evaluation
        +
Documentation
```

This is the full journey we wanted students to see.

---

# 35. Add a Health Check

A simple application can display:

```text
System Status

✓ OCR available
✓ Embedding model loaded
✓ Resume parser available
✓ Matching engine available
```

This is useful for debugging.

For example:

```python
with st.expander(
    "System Information"
):

    st.write(
        "Embedding model:",
        MODEL_NAME
    )
```

---

# 36. Add Processing Information

The application can show:

```text
Document characters: 4,218
Resume skills found: 8
Job requirements found: 6
Semantic matches: 4
```

This helps users understand what happened.

It also helps developers diagnose unexpected output.

---

# 37. Timing the Pipeline

We can measure processing time.

Python provides:

```python
import time
```

For example:

```python
start = time.perf_counter()

text = process_document(
    resume_file
)

elapsed = (
    time.perf_counter()
    - start
)

logger.info(
    "OCR completed in %.2f seconds",
    elapsed
)
```

We can do the same for:

```text
OCR
Parsing
Embedding
Matching
```

Now we know where the application spends time.

---

# 38. Performance Is Part of the Application

Imagine:

```text
OCR      → 4 seconds
Embedding → 1 second
Matching → 0.1 seconds
```

The obvious optimization target is:

```text
OCR
```

not:

```text
Matching
```

This is why measuring is better than guessing.

---

# 39. Avoid Unnecessary Work

Suppose the user changes only the job description.

We shouldn't necessarily redo:

```text
OCR
```

on the resume.

The architecture should allow:

```text
Resume
 ↓
OCR once
 ↓
Cache text
```

Then:

```text
Job changes
 ↓
Reuse resume text
 ↓
Recalculate matching
```

This is a practical reason to keep components separate.

---

# 40. Think in Data Flow

A good way to design the application is to ask:

```text
What data enters?
What data changes?
What data can be cached?
What data is expensive to calculate?
What data is deterministic?
```

For our system:

```text
Uploaded Resume
      ↓
OCR Text
      ↓
Parsed Resume
      ↓
Resume Embedding
```

The job changes independently:

```text
Job Description
      ↓
Job Requirements
      ↓
Job Embedding
```

Then:

```text
Resume representation
        +
Job representation
        ↓
Matching
```

This is much cleaner than one giant function.

---

# 41. Add a Downloadable Report

A useful application can allow the user to download results.

For example:

```text
resume_report.txt
```

containing:

```text
Resume Match Report

Overall Match: 82%

Strong Matches:
- Python
- Machine Learning
- SQL

Related Matches:
- OpenCV → Computer Vision

Potential Gaps:
- AWS
- Kubernetes
```

Streamlit provides download functionality.

The exact implementation can be an exercise.

---

# 42. Why Reporting Matters

We have now separated:

```text
Analysis
```

from:

```text
Presentation
```

The result exists as structured data.

The UI displays it.

A report can display it.

An API could eventually return it.

This is another advantage of having a clean matching engine.

---

# 43. Optional API Layer

Once our core application is independent from Streamlit, we could expose it through an API.

For example:

```text
POST /match
```

with:

```text
resume
job_description
```

returning:

```json
{
    "score": 0.82,
    "matched_skills": [],
    "missing_skills": []
}
```

We don't necessarily need to build this now.

The important lesson is:

> **A clean application core can support multiple interfaces.**

---

# 44. Deployment

Our application currently runs locally:

```bash
streamlit run app.py
```

A natural next step is deployment.

The exact deployment platform is less important than understanding the process:

```text
Local project
      ↓
Git repository
      ↓
Dependencies
      ↓
Application configuration
      ↓
Deployment environment
      ↓
Running application
```

The application should not depend on:

```text
"works on my machine"
```

---

# 45. Deployment Checklist

Before deployment:

```text
□ requirements.txt
□ README.md
□ .gitignore
□ no secrets committed
□ model loading works
□ OCR works
□ tests pass
□ empty inputs handled
□ invalid files handled
□ logs available
□ reasonable error messages
□ evaluation examples tested
```

This is the difference between:

```text
demo
```

and:

```text
software
```

---

# 46. Security Considerations

Resumes contain personal information.

They may contain:

```text
names
emails
phone numbers
addresses
employment history
education
```

Therefore, students should think about:

```text
Where is the file stored?
How long is it retained?
Who can access it?
Is it sent to an external service?
Is it logged?
```

Do not log the entire resume text unnecessarily.

For example, prefer:

```python
logger.info(
    "Processed resume with %d characters",
    len(text)
)
```

over:

```python
logger.info(
    "Resume text: %s",
    text
)
```

---

# 47. Privacy by Design

A good default principle is:

> **Only collect and retain the information the application actually needs.**

For our local educational application, we can process the resume in memory where practical.

If we later store resumes:

```text
storage
+
retention
+
deletion
```

become application design decisions.

---

# 48. AI-Specific Failure Handling

AI systems can fail in unusual ways.

For example:

```text
OCR produces incorrect text.
```

Then:

```text
Parser extracts wrong skills.
```

Then:

```text
Matcher produces a misleading score.
```

This is a chain of errors.

Our application should therefore make intermediate outputs inspectable.

For example:

```text
Extracted Text
      ↓
Parsed Resume
      ↓
Detected Skills
      ↓
Semantic Matches
      ↓
Final Score
```

If the final answer is wrong, we can locate where the error began.

---

# 49. Add an "Inspect Results" Section

In Streamlit:

```python
with st.expander(
    "Inspect extracted text"
):

    st.text(
        resume_text
    )
```

And:

```python
with st.expander(
    "Inspect parsed resume"
):

    st.json(
        resume
    )
```

And:

```python
with st.expander(
    "Inspect matching details"
):

    st.json(
        result
    )
```

This is incredibly useful during development.

---

# 50. The Application Is Now Observable

We can inspect:

```text
Input
 ↓
Intermediate representation
 ↓
Model output
 ↓
Decision
```

This property is often called **observability**.

Even a small student project benefits from it.

---

# 51. Refactor the Scoring Engine

Create:

```text
scoring.py
```

Move scoring logic into functions.

For example:

```python
def calculate_skill_coverage(
    matched,
    required
):
    ...
```

Then:

```python
def calculate_final_score(
    skill_coverage,
    semantic_coverage,
    document_similarity,
    weights
):
    ...
```

This makes the scoring system independently testable.

---

# 52. Test the Score

Suppose:

```python
score = calculate_final_score(
    skill_coverage=0.8,
    semantic_coverage=0.9,
    document_similarity=0.7,
    weights={
        "skill": 0.60,
        "semantic": 0.25,
        "document": 0.15
    }
)
```

We can verify the formula independently.

This is much better than testing the score only by clicking through Streamlit.

---

# 53. Avoid Hidden Constants

Bad:

```python
score = (
    skill * 0.6
    +
    semantic * 0.25
    +
    similarity * 0.15
)
```

Better:

```python
score = calculate_final_score(
    skill,
    semantic,
    similarity,
    weights
)
```

where:

```python
weights = {
    "skill": 0.60,
    "semantic": 0.25,
    "document": 0.15
}
```

Now the design decision is visible.

---

# 54. Add Version Information

As the project evolves:

```text
Version 1
Version 2
Version 3
```

we can expose:

```python
APP_VERSION = "1.0.0"
```

Then display:

```text
Resume Matcher v1.0.0
```

This becomes useful once deployed.

---

# 55. Git Tags

Instead of only commits, we can create milestones:

```bash
git tag v1.0.0
```

For example:

```text
v0.1
Prototype

v0.5
Resume Parser

v0.8
Semantic Matching

v1.0
Resume Job Matcher
```

This shows students that Git is not just:

```text
backup.py
```

It is part of the development lifecycle.

---

# 56. The Development Lifecycle

We have now returned to the workflow introduced in Phase 0:

```text
Experiment
     ↓
Develop
     ↓
Git Checkpoint
     ↓
Test
     ↓
Iterate
```

But now the loop is much larger:

```text
Experiment
     ↓
Prototype
     ↓
Build
     ↓
Evaluate
     ↓
Refactor
     ↓
Test
     ↓
Git Checkpoint
     ↓
Deploy
     ↓
Monitor
     ↓
Iterate
```

This is the real developer workflow.

---

# 57. Final Architecture

Our complete Phase 4 application can now be visualized as:

```text
                           USER
                             │
                             ▼
                      Streamlit UI
                             │
             ┌───────────────┴───────────────┐
             │                               │
             ▼                               ▼
          Resume                       Job Description
             │                               │
             ▼                               ▼
      Document Reader                   Job Parser
             │                               │
             ▼                               ▼
          Raw Text                       Requirements
             │                               │
             ▼                               │
       Resume Parser                         │
             │                               │
             ▼                               │
      Structured Resume                      │
             │                               │
             └───────────────┬───────────────┘
                             ▼
                      Matching Engine
                             │
               ┌─────────────┼─────────────┐
               ▼             ▼             ▼
            Exact         Semantic      Document
            Match          Match        Similarity
               │             │             │
               └─────────────┼─────────────┘
                             ▼
                       Scoring Engine
                             │
                             ▼
                       Match Report
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
              Streamlit              Download
                  UI                  Report
```

Around this sits:

```text
Configuration
Logging
Testing
Caching
Git
Documentation
Deployment
```

That is the anatomy of a complete intelligent application.

---

# 58. Final Project Checklist

Before calling the project complete:

## Python

```text
□ Functions
□ Modules
□ Classes / dataclasses where useful
□ File handling
□ Exceptions
```

## NLP

```text
□ Text cleaning
□ Regex extraction
□ Skill extraction
□ Embeddings
□ Semantic similarity
```

## Machine Learning

```text
□ Evaluation
□ Precision
□ Recall
□ F1
□ Thresholds
```

## Deep Learning

```text
□ Embedding model
□ Model loading
□ Model caching
```

## Computer Vision

```text
□ Resume image input
□ OCR
□ Document preprocessing
```

## Software Engineering

```text
□ Modular architecture
□ Configuration
□ Logging
□ Tests
□ Error handling
□ Input validation
□ Git
□ README
□ Requirements
```

## Application

```text
□ Streamlit UI
□ Resume upload
□ Job description input
□ Match score
□ Strong matches
□ Semantic matches
□ Potential gaps
□ Explainable results
```

---

# 59. The Phase 4 Capstone

At this point, students should be able to look at the application and trace almost every component back to something they learned earlier.

```text
Python
   ↓
Program structure

EDA
   ↓
Understand messy real-world data

Regex
   ↓
Extract predictable information

Computer Vision
   ↓
Read document images

OCR
   ↓
Image → Text

NLP
   ↓
Process language

TF-IDF
   ↓
Represent text lexically

Cosine Similarity
   ↓
Compare vectors

Embeddings
   ↓
Represent semantic meaning

Machine Learning
   ↓
Evaluate decisions

Deep Learning
   ↓
Use learned representations

Streamlit
   ↓
Build the interface

Git
   ↓
Track development

Testing
   ↓
Prevent regressions

Deployment
   ↓
Turn the project into usable software
```

This is the point of Phase 4.

We are not trying to teach students one more library.

We are teaching them to **assemble the things they already know into a system**.

---

# 60. Final Challenge — Rebuild It From Scratch

The final exercise should be:

> **Build the application again without following the tutorial line by line.**

Give students the requirements:

```text
Input:
    Resume
    Job Description

Output:
    Extracted resume information
    Required skills
    Exact matches
    Semantic matches
    Missing skills
    Overall match score
    Explanation
```

And the architectural constraints:

```text
Python
Streamlit
OCR
Regex
Scikit-learn
Embeddings
Git
Tests
```

Students should decide:

```text
Which modules?
Which functions?
Which data structures?
Which thresholds?
Which scoring formula?
Which UI?
```

This is where tutorial-following becomes engineering.

---

# 61. Final Git Checkpoint

Once the application is complete:

```bash
git status
```

Run the tests:

```bash
pytest
```

Run the application:

```bash
streamlit run app.py
```

Then:

```bash
git add .
```

and:

```bash
git commit -m "Complete intelligent resume matching application"
```

Optionally:

```bash
git tag v1.0.0
```

We now have a meaningful milestone in the repository.

---

# 62. The Full Phase 4 Journey

The entire phase can now be understood as:

```text
PHASE 4
Building Intelligent Systems
│
├── Anatomy of an Intelligent Application
│
├── Project 1
│   └── Document Reader
│       Image → OCR → Text
│
├── Project 2
│   └── Resume Parser
│       Text → Rules → Structure
│
├── Project 2.1
│   └── Reliable Parser
│       Test → Evaluate → Improve
│
├── Project 2.2
│   └── TF-IDF Matching
│       Text → Vectors → Similarity
│
├── Project 2.3
│   └── Embeddings
│       Text → Semantic Vectors → Similarity
│
├── Project 3
│   └── Resume ↔ Job Matching
│       Resume + Job → Match
│
└── Project 4
    └── Production-Like Application
        Build → Test → Refactor → Deploy
```

And the conceptual journey is:

```text
DATA
 ↓
INFORMATION
 ↓
REPRESENTATION
 ↓
SIMILARITY
 ↓
DECISION
 ↓
APPLICATION
 ↓
SOFTWARE
```

That is the final lesson of Phase 4:

> **An intelligent application is not just an AI model. It is a complete system built around data, models, rules, evaluation, interfaces, and software engineering.**
