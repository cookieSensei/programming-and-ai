# Project 3 — Resume ↔ Job Matching

## From Information Extraction to Decision Support

We have spent the previous projects building the pieces of an intelligent application.

We started with:

```text
Image
 ↓
OCR
 ↓
Text
```

Then:

```text
Text
 ↓
Regex / Rules
 ↓
Structured Resume
```

Then:

```text
Text
 ↓
TF-IDF
 ↓
Cosine Similarity
```

And finally:

```text
Text
 ↓
Embeddings
 ↓
Cosine Similarity
```

Now we are going to combine those pieces.

Our application will answer a much more useful question:

> **How well does this resume match this job description?**

This is the first point in Phase 4 where the individual techniques become one complete application.

---

# 1. What Are We Building?

The user will provide:

```text
Resume
+
Job Description
```

Our application will produce something like:

```text
Overall Match: 82%

Strong Matches
✓ Python
✓ Machine Learning
✓ Computer Vision

Potential Gaps
✗ Kubernetes
✗ AWS

Relevant Experience
✓ Software development
✓ Machine learning projects
```

The score is not a hiring decision.

It is a **decision-support signal**.

That distinction matters.

---

# 2. The Complete Pipeline

Our application now looks like:

```text
                    Resume
                       │
                       ▼
                Document Reader
                       │
                       ▼
                     Text
                       │
                       ▼
                Resume Parser
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
    Structured Data             Resume Text
          │                         │
          │                         ▼
          │                    Embedding
          │                         │
          │                         ▼
          │                    Resume Vector
          │                         │
          └────────────┐            │
                       │            │
                       ▼            ▼
                  Matching Engine
                       ▲
                       │
                 Job Description
                       │
                       ▼
                   Embedding
                       │
                       ▼
                  Job Vector
```

The result is:

```text
Resume
   +
Job
   ↓
Similarity
   ↓
Analysis
   ↓
Streamlit UI
```

---

# 3. Start With a Simple Problem

Before writing code, let's simplify the problem.

Suppose the job description says:

```text
We are looking for a Machine Learning Engineer.

Requirements:

Python
Machine Learning
SQL
Computer Vision
AWS

Experience with Docker is preferred.
```

And the resume says:

```text
Software Developer

Experienced Python developer working on
machine learning and computer vision projects.

Skills:

Python
Machine Learning
SQL
OpenCV
Docker
```

A human can compare these immediately.

We want our program to identify:

```text
Strong overlap:

Python
Machine Learning
SQL
Computer Vision

Partial / related:

OpenCV
Docker

Potential gap:

AWS
```

---

# 4. Don't Start With One Giant Score

It is tempting to immediately write:

```python
score = cosine_similarity(...)
```

and display:

```text
82%
```

But that hides too much.

A useful application should be able to explain:

```text
Why is the score high?

What matched?

What didn't?

Which requirements were found?

Which requirements were missing?
```

So our architecture will produce several signals.

---

# 5. Extract Requirements From the Job

We first need to understand what the job is asking for.

Start with a known skills vocabulary:

```python
KNOWN_SKILLS = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "computer vision",
    "opencv",
    "tensorflow",
    "pytorch",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "linux"
]
```

We can reuse the same idea from the resume parser.

---

# 6. Exact Skill Extraction

Create:

```python
def extract_required_skills(
    job_text,
    known_skills
):

    normalized = job_text.lower()

    found = []

    for skill in known_skills:

        pattern = rf"\b{re.escape(skill)}\b"

        if re.search(
            pattern,
            normalized
        ):

            found.append(skill)

    return found
```

This gives us:

```text
Job Description
       ↓
Known Skill Vocabulary
       ↓
Required Skills
```

For example:

```python
[
    "python",
    "machine learning",
    "sql",
    "computer vision",
    "aws",
    "docker"
]
```

---

# 7. Extract Skills From the Resume

We already have this capability from Project 2.

For example:

```python
resume = parse_resume(
    resume_text
)
```

Then:

```python
resume_skills = resume["skills"]
```

We now have two sets:

```text
Resume Skills
```

and:

```text
Job Skills
```

---

# 8. Exact Skill Matching

Let's compare them.

```python
resume_skills = {
    skill.lower()
    for skill in resume["skills"]
}

job_skills = {
    skill.lower()
    for skill in required_skills
}
```

Intersection:

```python
matched_skills = (
    resume_skills
    &
    job_skills
)
```

Missing:

```python
missing_skills = (
    job_skills
    -
    resume_skills
)
```

For our example:

```text
Matched:

Python
Machine Learning
SQL
Computer Vision
Docker

Missing:

AWS
```

This is already useful.

---

# 9. Exact Matching Is Not Enough

Now consider:

```text
Resume:

OpenCV
```

Job:

```text
Computer Vision
```

Exact matching says:

```text
No match
```

But we know:

```text
OpenCV
```

is strongly associated with:

```text
Computer Vision
```

This is where our embedding matcher becomes useful.

We can retain:

```text
Exact matching
```

and add:

```text
Semantic matching
```

---

# 10. Build a Skill Relationship Layer

Our earlier skill descriptions can be reused.

```python
SKILL_DESCRIPTIONS = {

    "python": """
    Python programming language
    software development scripting
    """,

    "machine learning": """
    machine learning predictive modeling
    classification regression supervised learning
    """,

    "computer vision": """
    computer vision image processing
    image classification object detection
    OpenCV CNN
    """,

    "deep learning": """
    deep learning neural networks
    CNN transformers representation learning
    """,

    "sql": """
    SQL databases relational databases
    querying data
    """,

    "docker": """
    Docker containers containerization
    software deployment
    """,

    "aws": """
    Amazon Web Services cloud computing
    cloud infrastructure deployment
    """
}
```

Now we have a semantic representation for each requirement.

---

# 11. Match Resume Skills to Job Skills

Instead of comparing the entire resume to the entire job description immediately, we can first compare individual skills.

For each job requirement:

```text
Job Skill
    ↓
Embedding
    ↓
Compare against
    ↓
Resume Skills
    ↓
Best semantic match
```

For example:

```text
Job requirement:
Computer Vision

Resume skills:
Python
OpenCV
TensorFlow
SQL
```

The system may find:

```text
Computer Vision
        ↓
OpenCV
        ↓
High similarity
```

This gives us an explainable relationship.

---

# 12. Build a Skill Matching Function

Conceptually:

```python
def match_job_skills(
    resume_skills,
    job_skills,
    model
):
    ...
```

For every job skill:

```text
job skill
   ↓
compare with every resume skill
   ↓
find highest score
   ↓
store best match
```

The result might look like:

```python
[
    {
        "job_skill": "computer vision",
        "resume_skill": "opencv",
        "score": 0.81
    },

    {
        "job_skill": "machine learning",
        "resume_skill": "machine learning",
        "score": 1.00
    }
]
```

The exact scores will depend on the embedding model.

---

# 13. Why Compare Skills Instead of Entire Documents?

We could calculate:

```text
Resume embedding
        vs.
Job description embedding
```

and get one score.

That is useful.

But one number doesn't explain much.

Consider:

```text
Overall similarity = 0.79
```

What does that mean?

We don't know.

By comparing individual requirements, we can say:

```text
Python           → matched
Machine Learning → matched
Computer Vision  → matched through OpenCV
AWS              → missing
Kubernetes       → missing
```

That is much more useful.

---

# 14. Overall Document Similarity

We should still calculate the full-document similarity.

```python
resume_embedding = model.encode(
    resume_text
)

job_embedding = model.encode(
    job_text
)

overall_score = cosine_similarity(
    [resume_embedding],
    [job_embedding]
)[0][0]
```

This gives us:

```text
Resume ↔ Job similarity
```

But we should treat it as **one signal**, not the entire decision.

---

# 15. Why One Score Can Be Misleading

Imagine two resumes.

### Resume A

```text
Python
Machine Learning
Computer Vision
SQL
AWS
```

### Resume B

```text
Marketing
Sales
Business
Python
```

The second resume might contain some generic words that produce a reasonable document similarity.

But it doesn't satisfy the technical requirements.

This demonstrates:

> **Overall semantic similarity and requirement satisfaction are not the same thing.**

So we need multiple signals.

---

# 16. Build a Match Report

Our matching engine should eventually return something like:

```python
{
    "overall_similarity": 0.82,

    "matched_skills": [
        "python",
        "machine learning",
        "sql"
    ],

    "semantic_matches": [
        {
            "job_skill": "computer vision",
            "resume_skill": "opencv",
            "score": 0.81
        }
    ],

    "missing_skills": [
        "aws"
    ]
}
```

Now the UI has meaningful information to display.

---

# 17. Create a Match Score

We can combine several signals.

For example:

```text
Exact skill coverage
+
Semantic skill coverage
+
Overall document similarity
```

One simple educational formula could be:

```text
Final Score =

0.60 × Skill Coverage
+
0.25 × Semantic Coverage
+
0.15 × Document Similarity
```

The weights are **not universal**.

We are choosing them for our demonstration.

The important lesson is:

> **A composite score is a design decision.**

---

# 18. Calculate Skill Coverage

Suppose:

```text
Job requires:

Python
SQL
Machine Learning
Computer Vision
AWS
```

That's:

```text
5 requirements
```

Suppose:

```text
Python
SQL
Machine Learning
Computer Vision
```

are matched.

Then:

```text
Skill Coverage =
4 / 5
```

or:

```text
0.80
```

In Python:

```python
skill_coverage = (
    len(matched_skills)
    /
    len(job_skills)
)
```

Be careful when:

```python
len(job_skills) == 0
```

because division by zero would occur.

---

# 19. Semantic Coverage

Now suppose:

```text
Exact matches:

Python
SQL
Machine Learning

Semantic match:

OpenCV → Computer Vision
```

Then we can count:

```text
Exact + accepted semantic matches
```

against:

```text
Total job requirements
```

This gives us a richer measure.

---

# 20. Don't Double Count

Suppose:

```text
Computer Vision
```

was already exactly matched.

We should not also count:

```text
OpenCV → Computer Vision
```

as another requirement.

The unit we care about is:

```text
Job requirement
```

not:

```text
Number of matches generated
```

This sounds small, but it is an important data-modeling decision.

---

# 21. Required vs Preferred Skills

Real job descriptions often contain:

```text
Required:
Python
SQL
Machine Learning

Preferred:
AWS
Docker
Kubernetes
```

We should distinguish them.

For example:

```python
required_skills = [
    "python",
    "sql",
    "machine learning"
]

preferred_skills = [
    "aws",
    "docker",
    "kubernetes"
]
```

Now missing AWS should not necessarily be treated the same way as missing Python.

This is an important improvement to our application.

---

# 22. Weight Requirements

We can assign weights:

```text
Required skill   → weight 1.0
Preferred skill  → weight 0.5
```

Then:

```text
Weighted Coverage =
matched weight
----------------
total weight
```

For example:

```text
Required:
Python       1.0
SQL          1.0
ML           1.0

Preferred:
AWS          0.5
Docker       0.5
```

Total:

```text
4.0
```

If all required skills and Docker match:

```text
3.5 / 4.0
```

This is more informative than treating every skill equally.

---

# 23. Extracting Required vs Preferred

For our first implementation, we can use section and keyword heuristics.

Look for phrases such as:

```text
required
must have
requirements
qualifications
```

and:

```text
preferred
nice to have
bonus
plus
desired
```

This is still rule-based.

Again, we are deliberately using the simplest solution first.

---

# 24. A More Realistic Job Description

Create:

```text
job_description.txt
```

For example:

```text
Machine Learning Engineer

We are looking for a Machine Learning Engineer
to build and deploy machine learning systems.

Required Qualifications:

Python
Machine Learning
SQL
Computer Vision

Preferred:

AWS
Docker
Kubernetes

Responsibilities:

Build predictive models.
Develop computer vision systems.
Deploy machine learning services.
Work with data pipelines.
```

Now our application has realistic input.

---

# 25. Test With a Strong Resume

Create:

```text
resume_strong.txt
```

```text
John Smith

Python developer and machine learning engineer.

Skills:

Python
SQL
Machine Learning
OpenCV
TensorFlow
Docker

Experience:

Built image classification systems using
convolutional neural networks.

Developed predictive models and data pipelines.
```

We expect a strong match.

---

# 26. Test With a Weak Resume

Create:

```text
resume_weak.txt
```

```text
Jane Smith

Software developer.

Skills:

Java
JavaScript
HTML
CSS

Experience:

Built web applications and ecommerce websites.
```

We expect:

```text
low technical match
```

The application should not simply produce a score.

It should explain why.

---

# 27. Test With a Partial Resume

Create:

```text
resume_partial.txt
```

```text
Alex Johnson

Python developer.

Skills:

Python
SQL
Docker

Experience:

Built data processing systems using Python
and SQL.
```

Expected:

```text
Strong:
Python
SQL

Potential:
Docker

Missing:
Machine Learning
Computer Vision
AWS
Kubernetes
```

This is an excellent test case because it sits between:

```text
strong match
```

and:

```text
weak match
```

---

# 28. Build the Matching Engine

Create:

```text
job_matcher.py
```

We want functions such as:

```python
def extract_job_requirements(
    job_text
):
    ...


def match_exact_skills(
    resume_skills,
    job_skills
):
    ...


def match_semantic_skills(
    resume_skills,
    job_skills,
    model
):
    ...


def calculate_document_similarity(
    resume_text,
    job_text,
    model
):
    ...


def calculate_match_score(
    ...
):
    ...


def build_match_report(
    ...
):
    ...
```

The module should contain the matching logic.

`app.py` should remain primarily concerned with the UI.

---

# 29. The Matching Engine API

A useful main function could be:

```python
def match_resume_to_job(
    resume_text,
    resume_skills,
    job_text,
    job_skills,
    model
):
    ...
```

It could return:

```python
{
    "overall_similarity": ...,
    "skill_coverage": ...,
    "matched_skills": ...,
    "semantic_matches": ...,
    "missing_skills": ...,
    "final_score": ...
}
```

This is our application's central business logic.

---

# 30. Streamlit Interface

Our UI should have two inputs.

For example:

```python
resume_file = st.file_uploader(
    "Upload Resume",
    type=["png", "jpg", "jpeg", "pdf"]
)
```

and:

```python
job_text = st.text_area(
    "Paste Job Description"
)
```

The user then clicks:

```text
Analyze Match
```

---

# 31. The User Workflow

The UI should feel like:

```text
1. Upload Resume
        ↓
2. Paste Job Description
        ↓
3. Analyze Match
        ↓
4. Extract Resume Information
        ↓
5. Extract Job Requirements
        ↓
6. Compare Skills
        ↓
7. Calculate Semantic Similarity
        ↓
8. Generate Match Report
```

This is a complete application workflow.

---

# 32. Display the Overall Score

For example:

```python
st.metric(
    "Overall Match",
    f"{final_score * 100:.1f}%"
)
```

But remember:

> This is our application's scoring formula. It is not an objective probability that someone will succeed in the job.

Use language such as:

```text
Match Score
```

rather than:

```text
Probability of Hiring
```

---

# 33. Display Strong Matches

```python
st.subheader(
    "Strong Matches"
)

for skill in matched_skills:

    st.write(
        f"✓ {skill}"
    )
```

This immediately tells the user what the resume satisfies.

---

# 34. Display Semantic Matches

For example:

```python
st.subheader(
    "Related Skills"
)

for match in semantic_matches:

    st.write(
        f"{match['resume_skill']} "
        f"→ "
        f"{match['job_skill']} "
        f"({match['score']:.2f})"
    )
```

The user might see:

```text
OpenCV → Computer Vision (0.81)
```

This is much more useful than a mysterious overall score.

---

# 35. Display Missing Skills

```python
st.subheader(
    "Potential Gaps"
)

for skill in missing_skills:

    st.write(
        f"✗ {skill}"
    )
```

This transforms the application from:

```text
Scoring system
```

into:

```text
Decision-support tool
```

---

# 36. Explain the Score

We should show how the final score was calculated.

For example:

```text
Final Match Score

Skill Coverage       80%
Semantic Coverage    90%
Document Similarity  76%

Weights:

60% Skill Coverage
25% Semantic Coverage
15% Document Similarity
```

This makes the scoring system inspectable.

---

# 37. Avoid False Precision

Suppose the application says:

```text
82.374921%
```

That looks more scientific than it actually is.

Our score is based on:

```text
heuristics
+
embedding similarity
+
chosen weights
```

So display something like:

```text
82%
```

or:

```text
Strong Match
```

rather than pretending that:

```text
82.374921%
```

is an objective measurement.

---

# 38. Add Match Categories

We can create simple categories.

For example:

```python
if score >= 0.80:
    category = "Strong Match"

elif score >= 0.60:
    category = "Moderate Match"

else:
    category = "Weak Match"
```

Again, these thresholds are application choices.

They should eventually be evaluated against real examples.

---

# 39. The Important Evaluation Question

Now we have a scoring system.

But:

> **Does the score actually correspond to useful matching behavior?**

We need labeled examples.

Create:

```text
evaluation/
```

with:

```text
strong_match
partial_match
weak_match
```

For each resume/job pair, manually record:

```text
Expected category
```

Then compare:

```text
System category
vs.
Human category
```

---

# 40. Evaluate More Than the Final Score

We should evaluate:

### Skill extraction

```text
Did we find the right requirements?
```

### Exact matching

```text
Did known skills match correctly?
```

### Semantic matching

```text
Did related skills match correctly?
```

### Final classification

```text
Did strong/medium/weak match make sense?
```

This lets us identify where errors originate.

---

# 41. Confusion Matrix

If we use:

```text
Strong
Moderate
Weak
```

we can create a confusion matrix.

Conceptually:

```text
                 Predicted

              Strong  Medium  Weak

Actual Strong
Actual Medium
Actual Weak
```

This is the same evaluation mindset we used in classification.

We are now applying it to an intelligent application.

---

# 42. Important Limitation — Resume Matching Is Not Hiring

Our system should not make claims such as:

```text
Hire this person.
```

or:

```text
Reject this candidate.
```

A resume is only one source of information.

It does not fully capture:

- actual ability
- communication
- interviews
- work samples
- context
- career goals
- team fit
- accommodations
- many other factors

Our project should therefore be framed as:

> **Resume-to-job matching and decision support.**

Not:

> **Automated hiring.**

---

# 43. Another Important Limitation — Bias

A resume matching system can inherit bias from:

```text
training data
+
skill dictionaries
+
job descriptions
+
embedding models
+
scoring rules
```

For example, a system may favor particular terminology even when two candidates have equivalent abilities.

This is another reason not to treat:

```text
Match Score
```

as:

```text
Objective Candidate Quality
```

The score is an engineering artifact produced by our system.

---

# 44. Challenge — Add Explanations

For every semantic match, store:

```python
{
    "job_skill": "computer vision",
    "resume_skill": "opencv",
    "score": 0.81,
    "reason": "Semantic similarity"
}
```

For exact matches:

```python
{
    "job_skill": "python",
    "resume_skill": "python",
    "score": 1.0,
    "reason": "Exact skill match"
}
```

Now the application can explain its output.

---

# 45. Challenge — Let the User Adjust Weights

Add Streamlit sliders:

```python
skill_weight = st.slider(
    "Skill Coverage Weight",
    0.0,
    1.0,
    0.60
)
```

and:

```python
semantic_weight = st.slider(
    "Semantic Coverage Weight",
    0.0,
    1.0,
    0.25
)
```

and:

```python
document_weight = st.slider(
    "Document Similarity Weight",
    0.0,
    1.0,
    0.15
)
```

Then ensure:

```text
skill_weight
+
semantic_weight
+
document_weight
=
1
```

This is a good exercise in turning an algorithmic assumption into an application parameter.

---

# 46. Challenge — Compare Different Models

Our embedding model is currently:

```text
all-MiniLM-L6-v2
```

Research another sentence-transformer model.

Compare:

```text
Model A
vs.
Model B
```

using the same resume/job evaluation set.

Record:

```text
Model
Average similarity
Precision
Recall
F1
Speed
```

This teaches an important lesson:

> **A model is part of the system, not the entire system.**

---

# 47. Challenge — Cache Job Embeddings

If the same job description is analyzed against many resumes, we don't need to encode the job every time.

We can calculate:

```text
Job Description
      ↓
Embedding
      ↓
Store vector
```

Then:

```text
Resume 1 → embedding → compare
Resume 2 → embedding → compare
Resume 3 → embedding → compare
```

This is a simple example of thinking about system performance.

---

# 48. Challenge — Batch Resume Matching

Once one resume works, try:

```text
10 resumes
```

against:

```text
1 job description
```

The application should produce:

```text
Candidate        Match Score

John Smith       84%
Alex Johnson     71%
Jane Doe         43%
```

Now we have moved from:

```text
Single-document application
```

to:

```text
Ranking system
```

---

# 49. Ranking Changes the Problem

If we have:

```text
Candidate A → 84%
Candidate B → 71%
Candidate C → 43%
```

we can sort them.

But now we have another question:

> Does a higher score actually mean a better candidate?

This brings us back to evaluation.

A ranking system should be tested with realistic examples.

---

# 50. Architecture of the Complete Project

Our application now looks like:

```text
                           USER
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
           Resume                      Job Description
              │                             │
              ▼                             ▼
       Document Reader               Requirement Parser
              │                             │
              ▼                             ▼
          Resume Text                  Job Skills
              │                             │
              ▼                             ▼
        Resume Parser                Job Requirements
              │                             │
              └──────────────┬──────────────┘
                             ▼
                       Matching Engine
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         Exact Match    Semantic Match   Doc Similarity
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                       Scoring Engine
                             │
                             ▼
                        Match Report
                             │
                             ▼
                        Streamlit UI
```

This is now a genuine intelligent application.

---

# 51. Project Structure

Our project can now look like:

```text
resume-job-matcher/
│
├── app.py
│
├── document_reader.py
│
├── resume_parser.py
│
├── semantic_matcher.py
│
├── job_matcher.py
│
├── evaluation_data.py
│
├── evaluate_parser.py
│
├── requirements.txt
│
├── README.md
│
└── test_data/
    ├── resumes/
    └── jobs/
```

Each module has a clear responsibility.

---

# 52. What We Have Combined

This single project now uses almost everything we have learned.

### Python

Functions, modules, dictionaries, sets, files.

### Regex

Emails, phones, URLs, section detection.

### EDA mindset

Inspecting and understanding messy real-world text.

### Machine Learning

Evaluation, precision, recall, F1, thresholds.

### Deep Learning

Embedding models.

### NLP

Text processing and semantic representation.

### Computer Vision

OCR and image preprocessing.

### Streamlit

Building the user-facing application.

This is why this project belongs in Phase 4.

We are no longer learning isolated APIs.

We are combining the concepts.

---

# 53. The Complete Learning Journey

Look at what happened.

We began Phase 4 with:

```text
"I have an image."
```

Then:

```text
Image
 ↓
OCR
 ↓
Text
```

Then:

```text
Text
 ↓
Rules
 ↓
Information
```

Then:

```text
Text
 ↓
TF-IDF
 ↓
Similarity
```

Then:

```text
Text
 ↓
Embeddings
 ↓
Semantic Similarity
```

Now:

```text
Resume
+
Job
 ↓
Information
+
Similarity
 ↓
Decision Support
```

This is the anatomy of an intelligent application in practice.

---

# 54. Git Checkpoint

Once the application works:

```bash
git status
```

Then:

```bash
git add .
```

Then:

```bash
git commit -m "Build resume job matching application"
```

This is a major Phase 4 checkpoint.

At this point we have:

```text
Project 1
Document Reader
        ↓
Project 2
Resume Parser
        ↓
Project 3
Resume ↔ Job Matcher
```

---

# 55. Final Project Challenge

Before moving on, try turning this into something you would actually show someone.

The application should:

```text
1. Accept a resume
2. Extract its text
3. Parse basic information
4. Accept a job description
5. Extract requirements
6. Find exact skill matches
7. Find semantic skill matches
8. Calculate document similarity
9. Calculate a transparent match score
10. Show strengths
11. Show potential gaps
12. Explain the result
```

Then ask yourself:

> **Would another person understand what the application is doing without seeing the source code?**

If the answer is yes, you have moved from:

```text
AI experiment
```

to:

```text
AI application
```

---

# 56. What Comes Next?

We now have a substantial intelligent application.

But there is one final question:

> **Can we make the entire system more robust, maintainable, and production-like?**

The final stage of Phase 4 will focus on turning our collection of experiments into a polished application.

We will look at:

```text
Configuration
Logging
Caching
Testing
Error handling
Data validation
Application architecture
Model management
Deployment
```

The final architecture will be:

```text
                  Intelligent Application
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
       ▼                   ▼                   ▼
   Interface          Intelligence          Data
       │                   │                   │
   Streamlit       OCR + NLP + ML + DL     Files / Text
       │                   │                   │
       └───────────────────┼───────────────────┘
                           ▼
                       Evaluation
                           │
                           ▼
                      Deployment
```

At that point, Phase 4 stops being a collection of tutorials.

It becomes:

> **A complete journey from Python experiment to intelligent software.**
