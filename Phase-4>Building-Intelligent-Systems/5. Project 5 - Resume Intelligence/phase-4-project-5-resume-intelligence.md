# Project 5 - Resume Intelligence

## Bringing Everything Together

We have now built several smaller intelligent applications.

We learned how to:

```text
Read documents
Extract text
Clean text
Extract information
Compare text
Classify images
Train machine-learning models
Use deep-learning models
Use embeddings
Build Streamlit applications
```

Now we are going to combine these ideas.

The goal is not to introduce a completely new AI technique.

The goal is:

> **Take the tools we already know and combine them into one larger intelligent application.**

Our application will analyze a resume and produce useful information about it.

---

# 1. The Problem

A resume is more than a block of text.

It contains:

```text
Personal information
Education
Experience
Skills
Projects
Certifications
```

It may also arrive as:

```text
PDF
Image
Scanned document
```

A useful application therefore needs to solve several smaller problems.

We want to build a system that can:

```text
Read a resume
      ↓
Extract its text
      ↓
Clean the text
      ↓
Extract useful information
      ↓
Analyze the resume
      ↓
Compare it with a job description
      ↓
Produce useful results
```

---

# 2. This Is a Pipeline

Our application is not one model.

It is a collection of components.

```text
Resume
  ↓
Document Processing
  ↓
OCR / Text Extraction
  ↓
Text Cleaning
  ↓
Information Extraction
  ↓
Structured Resume
  ↓
Analysis
  ↓
Job Matching
  ↓
Results
  ↓
Streamlit
```

This is the main lesson of Project 5.

> **An intelligent application can contain many small intelligent and non-intelligent components.**

---

# 3. Start With What We Already Built

We already have pieces of this system from earlier projects.

From Project 1:

```text
OCR
OpenCV
Regex
Streamlit
```

From Project 2:

```text
Resume parsing
Information extraction
Structured data
```

From Project 3:

```text
TF-IDF
Cosine similarity
BM25
Embeddings
Ranking
```

From Project 4:

```text
Image preprocessing
CNN
Transfer learning
Inference
Streamlit
```

Now we combine them.

---

# 4. The First Version Should Be Simple

Do not start with the complete pipeline.

Begin with:

```text
Resume
  ↓
Text extraction
  ↓
Display text
```

Once this works, add:

```text
Text
  ↓
Information extraction
```

Then:

```text
Information
  ↓
Analysis
```

Then:

```text
Resume + Job Description
  ↓
Matching
```

Build the application incrementally.

---

# 5. Input

Our application can accept:

```text
Resume file
```

For the first version, support:

```text
PDF
PNG
JPG
JPEG
```

We can later expand the supported formats if needed.

---

# 6. Determine the Input Type

A PDF may contain:

```text
Machine-readable text
```

or:

```text
Scanned images
```

These require different processing.

Conceptually:

```text
Resume
  ↓
Is text available?
  │
  ├── Yes → Extract text
  │
  └── No  → OCR
```

This gives us a simple document-processing decision.

---

# 7. Text Extraction

For a text-based document:

```text
PDF
 ↓
Text extraction
 ↓
Raw text
```

The goal is to convert the document into something the NLP pipeline can understand.

---

# 8. OCR

For a scanned document:

```text
Image
 ↓
OpenCV preprocessing
 ↓
OCR
 ↓
Text
```

We already learned the components individually.

Now they become part of a larger system.

---

# 9. OpenCV Preprocessing

OCR can sometimes perform better after preprocessing.

Possible steps include:

```text
Image
 ↓
Grayscale
 ↓
Resize
 ↓
Threshold
 ↓
Noise reduction
 ↓
OCR
```

Do not assume every preprocessing operation is always beneficial.

Inspect the result.

---

# 10. Text Cleaning

Raw OCR text may contain:

```text
Extra whitespace
Special characters
Repeated characters
Broken lines
```

Use the techniques already learned.

For example:

```python
import re

text = re.sub(
    r"\s+",
    " ",
    text
).strip()
```

The goal is to produce cleaner text without destroying useful information.

---

# 11. Preserve the Original Text

Do not immediately overwrite the raw extraction.

Keep:

```text
raw_text
```

and:

```text
clean_text
```

This is useful when debugging extraction errors.

For example:

```python
resume = {
    "raw_text": raw_text,
    "clean_text": clean_text
}
```

---

# 12. Information Extraction

Now we convert:

```text
Large block of text
```

into:

```text
Structured information
```

For example:

```python
resume = {
    "name": "...",
    "email": "...",
    "phone": "...",
    "skills": [],
    "education": [],
    "experience": [],
    "projects": []
}
```

The exact schema can evolve during the project.

---

# 13. Regex

Regex is useful for deterministic patterns.

For example:

```text
Email
Phone number
URLs
Years
```

Example:

```python
email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
```

Then:

```python
emails = re.findall(
    email_pattern,
    text
)
```

Regex should handle patterns that are reasonably predictable.

---

# 14. Skill Extraction

Skills are less deterministic.

We can begin with a known skill list.

For example:

```python
skills = [
    "python",
    "java",
    "sql",
    "tensorflow",
    "pytorch",
    "opencv",
    "streamlit"
]
```

Then search the cleaned text.

This is a simple baseline.

---

# 15. Why a Skill List?

We do not need a sophisticated NLP system immediately.

A baseline can be:

```text
Resume text
     ↓
Normalize
     ↓
Compare against known skills
     ↓
Detected skills
```

For example:

```text
Resume:

"I built computer vision applications using
Python, OpenCV and TensorFlow."

        ↓

Detected:

Python
OpenCV
TensorFlow
```

---

# 16. Structured Resume

Eventually we want:

```python
{
    "contact": {
        "email": "...",
        "phone": "..."
    },
    "skills": [
        "Python",
        "OpenCV",
        "TensorFlow"
    ],
    "education": [],
    "experience": [],
    "projects": []
}
```

This is much easier for the rest of the application to work with than raw text.

---

# 17. Resume Analysis

Once we have structured information, we can calculate simple statistics.

For example:

```text
Number of detected skills
Number of projects
Number of education entries
Number of experience entries
```

We can also show:

```text
Skill categories
Technical skills
Tools
Programming languages
Frameworks
```

The exact categories depend on the implementation.

---

# 18. EDA Comes Into the Application

We learned EDA earlier.

Now we can use it on resume information.

For example:

```text
Most common skills
Number of skills per resume
Experience distribution
Education distribution
```

If we eventually analyze many resumes, we can visualize these distributions.

---

# 19. Resume + Job Description

Now we add a second input:

```text
Job Description
```

The application becomes:

```text
Resume
   +
Job Description
       ↓
    Analysis
```

We want to answer:

> How relevant is this resume to this job?

---

# 20. Baseline: Exact Skill Matching

Start simply.

Extract:

```text
Resume skills
```

and:

```text
Job skills
```

Then calculate:

```text
Matched skills
Missing skills
```

For example:

```text
Resume:
Python
SQL
OpenCV

Job:
Python
SQL
TensorFlow
PyTorch
```

Result:

```text
Matched:
Python
SQL

Missing:
TensorFlow
PyTorch
```

This is easy to understand.

---

# 21. Skill Match Score

A simple score could be:

```text
matched required skills
-----------------------
total required skills
```

For example:

```text
2 / 4 = 0.50
```

or:

```text
50%
```

This is a baseline, not a complete measure of suitability.

---

# 22. Why Exact Matching Is Not Enough

Consider:

```text
Resume:
"computer vision"

Job:
"OpenCV"
```

An exact string match may fail.

But these concepts can be related.

Likewise:

```text
Resume:
"deep learning"

Job:
"neural networks"
```

The words differ.

This is where semantic matching becomes useful.

---

# 23. TF-IDF Matching

We can represent:

```text
Resume text
```

and:

```text
Job description
```

using TF-IDF.

Then:

```text
TF-IDF vectors
       ↓
Cosine similarity
       ↓
Similarity score
```

This gives us a second matching approach.

---

# 24. Embedding Matching

Now we can use the embedding technique from Project 3.

Conceptually:

```text
Resume
  ↓
Embedding
  ↓
Vector
```

and:

```text
Job Description
  ↓
Embedding
  ↓
Vector
```

Then:

```text
Cosine similarity
```

compares them.

This can capture some semantic relationships that exact matching misses.

---

# 25. Combine Signals

Now we have multiple signals:

```text
Exact skill match
+
TF-IDF similarity
+
Semantic similarity
```

We can combine them into a simple score.

For example:

```text
Final Score =
    0.5 × skill_score
  + 0.2 × tfidf_score
  + 0.3 × semantic_score
```

The weights are examples.

Students should experiment with them rather than treating them as universally correct.

---

# 26. Ranking

Suppose we have several resumes:

```text
Resume A → 0.82
Resume B → 0.71
Resume C → 0.64
Resume D → 0.48
```

Sort them:

```text
A
B
C
D
```

Now the system becomes a simple ranking application.

---

# 27. What the Score Means

Be careful with interpretation.

A score such as:

```text
82%
```

does not mean:

```text
82% probability the candidate will succeed.
```

It means something closer to:

> The candidate and job produced a relatively high score according to our chosen matching formula.

The scoring method should be explained in the application.

---

# 28. Streamlit Interface

The final application can contain:

```text
Resume Intelligence
```

then:

```text
Upload Resume
[ Choose file ]

Job Description
[ Text area ]

[ Analyze ]
```

Then display:

```text
Resume Information
```

and:

```text
Job Match
```

---

# 29. Resume Information View

For example:

```text
Name:
Jane Doe

Email:
jane@example.com

Skills:
Python
TensorFlow
OpenCV
SQL

Projects:
3

Education:
B.Sc. Computer Science
```

This demonstrates the parser independently from the matcher.

---

# 30. Match Results View

For example:

```text
Overall Match Score
82%

Matched Skills
✓ Python
✓ SQL
✓ OpenCV

Missing Skills
• PyTorch
• Kubernetes
```

Then:

```text
Semantic Similarity:
0.78
```

The user can understand where the result came from.

---

# 31. Explain the Score

Do not simply display:

```text
82%
```

Show the components:

```text
Skill Match:        90%
TF-IDF Similarity:  74%
Semantic Match:     78%
```

Then:

```text
Final Score:        82%
```

This makes the application more interpretable.

---

# 32. The Complete Pipeline

We now have:

```text
                    RESUME
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
    Text-based PDF                Image
          │                         │
          ▼                         ▼
    Text Extraction             OpenCV
          │                         │
          │                        OCR
          │                         │
          └────────────┬────────────┘
                       ▼
                  Clean Text
                       │
                       ▼
              Information Extraction
                       │
              ┌────────┴────────┐
              ▼                 ▼
           Regex              NLP
              │                 │
              └────────┬────────┘
                       ▼
                Structured Resume
                       │
                       │
                + Job Description
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
            Skills   TF-IDF  Embeddings
              │        │        │
              └────────┼────────┘
                       ▼
                    Ranking
                       │
                       ▼
                  Streamlit UI
                       │
                       ▼
                      User
```

This is the culmination of the guided projects.

---

# 33. What We Have Combined

This single project uses ideas from almost the entire curriculum.

### Python

```text
Functions
Modules
Data structures
File handling
```

### Regex

```text
Pattern extraction
Text cleaning
```

### Computer Vision

```text
OpenCV
Image preprocessing
OCR
```

### NLP

```text
Text processing
Information extraction
```

### EDA

```text
Resume statistics
Skill distributions
```

### Machine Learning

```text
TF-IDF
Similarity
Ranking
```

### Deep Learning

```text
Embeddings
Neural representations
```

### Application Development

```text
Streamlit
```

---

# 34. This Is Not One Big Model

The application does not need one neural network that does everything.

Instead:

```text
Small deterministic components
+
Machine-learning components
+
Deep-learning components
+
Application code
```

work together.

This is the central lesson of Phase 4.

---

# 35. Start With a Working Baseline

The first complete version should be:

```text
PDF
 ↓
Text extraction
 ↓
Regex
 ↓
Skill matching
 ↓
Simple score
 ↓
Streamlit
```

Make this work first.

Then add:

```text
TF-IDF
```

Then:

```text
Embeddings
```

Then:

```text
OCR
```

Do not build the entire pipeline at once.

---

# 36. Version the Application

A useful progression is:

### Version 1

```text
Resume
 ↓
Text extraction
 ↓
Skill extraction
 ↓
Streamlit
```

### Version 2

```text
Resume + Job
 ↓
Exact skill matching
```

### Version 3

```text
TF-IDF
+
Cosine similarity
```

### Version 4

```text
Embeddings
+
Semantic matching
```

### Version 5

```text
Scanned resume
+
OCR
```

### Version 6

```text
Complete Resume Intelligence application
```

---

# 37. Test Each Stage

Because this is a pipeline, test individual pieces.

For example:

```text
Does PDF extraction work?

Does OCR work?

Does email extraction work?

Does skill extraction work?

Does similarity work?

Does scoring work?

Does Streamlit display the result?
```

If the final score looks wrong, we need to know which component caused the problem.

---

# 38. Use Known Examples

Create a few example resumes and job descriptions where you already know what should happen.

For example:

```text
Resume A:
Strong Python + ML background

Job:
Python ML Engineer
```

Expected:

```text
High match
```

Another:

```text
Resume B:
Graphic design background

Job:
Python ML Engineer
```

Expected:

```text
Low match
```

These examples help us sanity-check the system.

---

# 39. Error Analysis

When something looks wrong, inspect the pipeline.

Suppose:

```text
Resume has Python
```

but the application says:

```text
Python missing
```

Possible causes:

```text
OCR error
Text cleaning error
Regex error
Skill normalization error
```

The problem may not be the similarity model.

Trace the data.

---

# 40. Normalization

Different text forms can refer to the same thing.

For example:

```text
Python
python
PYTHON
```

should usually become:

```text
python
```

Similarly:

```text
Tensor Flow
TensorFlow
```

may need normalization.

Normalization improves deterministic matching.

---

# 41. Skill Synonyms

We can optionally create simple mappings.

For example:

```python
skill_aliases = {
    "tf": "tensorflow",
    "sklearn": "scikit-learn",
    "opencv": "opencv"
}
```

This is still deterministic logic.

Later, embeddings can help with more semantic relationships.

---

# 42. What Should Be Deterministic?

Use deterministic methods where they make sense:

```text
Email extraction → Regex
Phone extraction → Regex
File validation → Rules
Skill normalization → Rules
Score formula → Explicit calculation
```

Use ML/DL where representations or predictions are useful:

```text
OCR
Semantic similarity
Document classification
```

This keeps the application understandable.

---

# 43. Final Streamlit Layout

A simple final interface might look like:

```text
====================================
        RESUME INTELLIGENCE
====================================

Upload Resume
[ resume.pdf ]

Job Description
[                           ]
[                           ]
[                           ]

             [ Analyze ]

------------------------------------

RESUME

Name: Jane Doe
Email: jane@example.com

Skills
Python | SQL | OpenCV | TensorFlow

------------------------------------

JOB MATCH

Overall Score: 82%

Matched Skills
✓ Python
✓ SQL
✓ OpenCV

Missing Skills
• PyTorch
• Kubernetes

Similarity
TF-IDF:       0.74
Semantic:     0.78
```

Keep the interface simple enough that the underlying system remains visible.

---

# 44. Optional Resume Ranking

A natural extension is to allow:

```text
Multiple resumes
+
One job description
```

Then:

```text
Resume A → 0.87
Resume B → 0.79
Resume C → 0.63
```

and display them ranked.

This connects directly to the ranking concepts from Project 3.

---

# 45. Optional Job Ranking

We can reverse the problem:

```text
One resume
+
Multiple jobs
```

Then:

```text
Job A → 0.87
Job B → 0.79
Job C → 0.63
```

The same matching engine can support both directions.

This is a useful demonstration of reusable logic.

---

# 46. Optional Document Classification

We can also connect Project 4.

Before parsing:

```text
Uploaded document
        ↓
Document Classifier
        ↓
Is this a resume?
```

Then:

```text
If Resume:
    continue to parser
```

Conceptually:

```text
Document
   ↓
Classifier
   ↓
Resume?
 ┌─┴─┐
Yes No
 │   │
 ▼   ▼
Parse Reject / Inform
```

This shows how separate intelligent components can be composed.

---

# 47. The Full Phase 4 System

At this point we have:

```text
                 DOCUMENT
                    │
                    ▼
             DOCUMENT CLASSIFIER
                    │
                    ▼
                  RESUME
                    │
             ┌──────┴──────┐
             ▼             ▼
            OCR       TEXT EXTRACTION
             │             │
             └──────┬──────┘
                    ▼
               TEXT CLEANING
                    │
                    ▼
             RESUME PARSER
                    │
                    ▼
            STRUCTURED DATA
                    │
                    ├─────────────┐
                    ▼             ▼
                  EDA         JOB DESCRIPTION
                    │             │
                    │      ┌──────┴──────┐
                    │      ▼             ▼
                    │    TF-IDF      EMBEDDINGS
                    │      │             │
                    │      └──────┬──────┘
                    │             ▼
                    │         SIMILARITY
                    │             │
                    └──────┬──────┘
                           ▼
                        RANKING
                           │
                           ▼
                       STREAMLIT
```

This is a **substantial application** without requiring us to introduce production engineering.

---

# 48. What Makes This Project Important

The important achievement is not the resume parser.

It is the realization that:

```text
AI application
```

does not mean:

```text
one giant AI model.
```

It can mean:

```text
OCR
+
Regex
+
NLP
+
ML
+
DL
+
Similarity
+
Python
+
UI
```

each doing a small part of the job.

---

# 49. Final Questions

Before moving to the final capstone, you should be able to answer:

```text
1. Why is an intelligent application a pipeline?

2. Why do we separate OCR from NLP?

3. Why is regex useful even when we have ML?

4. Why start with exact skill matching?

5. What problem does TF-IDF solve?

6. What problem do embeddings solve?

7. Why do we use cosine similarity?

8. Why should the score be explainable?

9. What is the difference between a model and an application?

10. How can the document classifier become part of this system?

11. Which components are reusable?

12. Where can the pipeline fail?
```

---

# 50. Final Takeaway

We started Phase 4 with individual components:

```text
OCR
Regex
NLP
ML
DL
CV
Similarity
Streamlit
```

Now we have assembled them:

```text
                 INTELLIGENT APPLICATION

                       RESUME
                          ↓
                  DOCUMENT PROCESSING
                          ↓
                     TEXT / OCR
                          ↓
                    INFORMATION
                      EXTRACTION
                          ↓
                   STRUCTURED DATA
                          ↓
                  MATCHING + ANALYSIS
                          ↓
                       RANKING
                          ↓
                      STREAMLIT
```

The important lesson is:

> **You do not need one magical model to build an intelligent application. You can build intelligence by combining many understandable components.**

That is what Phase 4 has been preparing us for.

Next comes the final guided step:

# Project 6 - Final Capstone

For the capstone, the problem will no longer be provided.

You will choose what to build.
