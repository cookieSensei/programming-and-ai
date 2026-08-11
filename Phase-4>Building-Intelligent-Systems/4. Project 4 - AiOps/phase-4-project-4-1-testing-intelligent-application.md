# Project 4.1 — Testing an Intelligent Application

## From "It Works" to "We Know It Works"

Our resume matcher now has a lot of moving parts:

```text
Streamlit
   ↓
Document Reader
   ↓
OCR
   ↓
Resume Parser
   ↓
Job Parser
   ↓
Embeddings
   ↓
Similarity
   ↓
Scoring
   ↓
Match Report
```

If something goes wrong, where is the problem?

It could be:

```text
OCR
Parser
Skill extraction
Embedding model
Similarity
Threshold
Scoring
UI
```

This is why testing becomes increasingly important as an application grows.

The goal of this module is to learn how to test an intelligent application at **multiple levels**.

---

# 1. Three Different Questions

When we test the application, we should distinguish three questions.

### Question 1

> Does the Python function work?

This is a **software test**.

### Question 2

> Does the AI component perform well?

This is **model/system evaluation**.

### Question 3

> Does the whole application solve the user's problem?

This is **application evaluation**.

These are related, but they are not the same thing.

---

# 2. Unit Tests

A unit test checks a small piece of code.

For example:

```python
def add(a, b):
    return a + b
```

A test could be:

```python
def test_add():

    assert add(2, 3) == 5
```

The unit is:

```text
add()
```

We test it independently.

Our resume project should do the same.

---

# 3. Test the Email Extractor

Suppose we have:

```python
def extract_email(text):
    ...
```

Create:

```text
tests/test_resume_parser.py
```

Then:

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

We want:

```text
PASSED
```

---

# 4. Test the Missing Case

We should also test:

```text
No email
```

For example:

```python
def test_missing_email():

    text = """
    John Smith
    Python Developer
    """

    assert extract_email(text) is None
```

This is important because real data is messy.

A good test suite should contain both:

```text
Expected input
```

and:

```text
Unexpected / missing input
```

---

# 5. Test Skill Extraction

Suppose:

```python
def extract_skills(text):
    ...
```

Test:

```python
def test_extract_skills():

    text = """
    Python developer
    with SQL and TensorFlow experience.
    """

    skills = extract_skills(
        text
    )

    assert "Python" in skills
    assert "SQL" in skills
    assert "TensorFlow" in skills
```

This gives us a contract:

> Given this input, these skills should be detected.

---

# 6. Test Section Parsing

For example:

```python
def test_parse_sections():

    text = """
    Skills
    Python
    SQL

    Education
    BSc Computer Science
    """

    sections = parse_sections(
        text
    )

    assert "Python" in (
        sections["skills"]
    )

    assert "BSc Computer Science" in (
        sections["education"]
    )
```

Now a future refactor can tell us if section parsing breaks.

---

# 7. Why Tests Matter During Refactoring

Imagine we change:

```python
normalize_line()
```

to improve:

```text
Technical Expertise
```

Maybe it accidentally breaks:

```text
Skills:
```

Without tests:

```text
The application appears to work.
```

With tests:

```text
FAILED
```

We immediately know that an old behavior has broken.

This is called **regression detection**.

---

# 8. Regression Testing

A regression is when:

> Something that previously worked stops working after a change.

Our workflow becomes:

```text
Change code
   ↓
Run tests
   ↓
Tests pass?
   ├── Yes → Continue
   └── No  → Investigate
```

This is one of the main reasons tests become valuable as projects grow.

---

# 9. Testing the Exact Matcher

Our exact matcher is deterministic.

For example:

```python
def match_exact_skills(
    resume_skills,
    job_skills
):

    resume_skills = set(
        resume_skills
    )

    job_skills = set(
        job_skills
    )

    matched = (
        resume_skills
        &
        job_skills
    )

    missing = (
        job_skills
        -
        resume_skills
    )

    return matched, missing
```

This is excellent material for unit tests.

---

# 10. Test Exact Matching

```python
def test_exact_skill_matching():

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

Because the function is deterministic, this test should be stable.

---

# 11. Test Empty Inputs

Always think about:

```text
What if the input is empty?
```

For example:

```python
def test_empty_resume():

    matched, missing = (
        match_exact_skills(
            set(),
            {"python"}
        )
    )

    assert matched == set()

    assert missing == {
        "python"
    }
```

And:

```python
def test_empty_job():

    matched, missing = (
        match_exact_skills(
            {"python"},
            set()
        )
    )

    assert matched == set()

    assert missing == set()
```

Edge cases are where many real bugs appear.

---

# 12. Test the Scoring Function

Suppose our scoring formula is:

```text
Final Score =

0.60 × Skill Coverage
+
0.25 × Semantic Coverage
+
0.15 × Document Similarity
```

We should isolate it.

```python
def calculate_final_score(
    skill_coverage,
    semantic_coverage,
    document_similarity
):

    return (
        0.60 * skill_coverage
        +
        0.25 * semantic_coverage
        +
        0.15 * document_similarity
    )
```

Then test:

```python
def test_final_score():

    score = calculate_final_score(
        1.0,
        1.0,
        1.0
    )

    assert score == 1.0
```

This verifies the basic mathematical contract.

---

# 13. Test the Opposite Case

If everything is zero:

```python
def test_zero_score():

    score = calculate_final_score(
        0.0,
        0.0,
        0.0
    )

    assert score == 0.0
```

Now we have tested the two extremes.

---

# 14. Test Intermediate Values

```python
def test_intermediate_score():

    score = calculate_final_score(
        0.8,
        0.6,
        0.7
    )

    expected = (
        0.60 * 0.8
        +
        0.25 * 0.6
        +
        0.15 * 0.7
    )

    assert score == expected
```

This makes the scoring formula explicit.

---

# 15. Avoid Fragile Floating-Point Tests

Sometimes floating-point calculations produce tiny differences.

Instead of:

```python
assert score == 0.7348291
```

we can use:

```python
import pytest

assert score == pytest.approx(
    expected
)
```

This is a useful general Python testing technique.

---

# 16. Test Embedding Behavior Differently

Embedding models are different from deterministic functions.

We shouldn't normally test:

```python
assert similarity == 0.782341
```

because:

```text
model version
+
text preprocessing
+
library version
```

can affect the result.

Instead, test relationships.

For example:

```text
Similar sentence
    >
Unrelated sentence
```

---

# 17. Semantic Ranking Test

Suppose:

```python
query = (
    "image classification using CNNs"
)

related = (
    "computer vision and object detection"
)

unrelated = (
    "financial accounting and auditing"
)
```

Calculate:

```python
related_score = similarity(
    query,
    related
)

unrelated_score = similarity(
    query,
    unrelated
)
```

Then test:

```python
assert (
    related_score
    >
    unrelated_score
)
```

We are testing the behavior we actually care about.

---

# 18. Model Tests Are Not Unit Tests

This distinction is important.

A unit test says:

```text
Does this function behave correctly?
```

A model evaluation says:

```text
Does the model perform well on representative examples?
```

For example:

```text
pytest
```

might tell us:

```text
extract_email() works
```

but it cannot tell us:

```text
the embedding model is good at resume matching
```

We need a dataset for that.

---

# 19. Create an Evaluation Dataset

Create:

```text
data/evaluation/
```

Each example can contain:

```text
resume
job description
expected relationship
```

For example:

```python
{
    "resume": """
    Python developer with machine
    learning and SQL experience.
    """,

    "job": """
    Looking for a Python machine
    learning engineer with SQL.
    """,

    "expected": "strong"
}
```

Another:

```python
{
    "resume": """
    Frontend developer specializing
    in JavaScript and CSS.
    """,

    "job": """
    Machine learning engineer
    with Python and TensorFlow.
    """,

    "expected": "weak"
}
```

---

# 20. Evaluation Is Data-Driven

We now have:

```text
Test cases
    ↓
Application
    ↓
Predictions
    ↓
Compare with expected
```

This is different from:

```text
Run one resume
Look at the output
Say "looks good"
```

A system should be evaluated on multiple examples.

---

# 21. Define the Expected Output

For a resume/job pair, we might record:

```python
{
    "expected_category": "strong",

    "expected_skills": [
        "python",
        "machine learning",
        "sql"
    ]
}
```

This is our ground truth.

---

# 22. Precision and Recall for Skills

Suppose the job requires:

```text
Python
SQL
Machine Learning
AWS
```

The system predicts:

```text
Python
SQL
Machine Learning
Docker
```

Then:

```text
True Positives:
Python
SQL
Machine Learning

False Positive:
Docker

False Negative:
AWS
```

Therefore:

```text
Precision =
3 / 4
```

and:

```text
Recall =
3 / 4
```

This is more informative than simply saying:

```text
3 skills were correct.
```

---

# 23. F1 Score

We can calculate:

```text
F1 =
2 × Precision × Recall
----------------------
Precision + Recall
```

Or use scikit-learn:

```python
from sklearn.metrics import f1_score
```

For binary labels, we can represent:

```text
1 = matched
0 = not matched
```

Then:

```python
f1_score(
    y_true,
    y_pred
)
```

The important part is understanding what the metric means before using the function.

---

# 24. Evaluate Thresholds

Our semantic matcher uses a threshold:

```python
threshold = 0.60
```

But why?

We can experiment.

```python
thresholds = [
    0.40,
    0.50,
    0.60,
    0.70,
    0.80
]
```

For each:

```text
Threshold
   ↓
Predictions
   ↓
Precision
Recall
F1
```

Then compare.

---

# 25. Threshold Trade-Off

Generally:

```text
Lower threshold
      ↓
More matches
      ↓
Higher recall
      ↓
Potentially lower precision
```

Whereas:

```text
Higher threshold
      ↓
Fewer matches
      ↓
Potentially higher precision
      ↓
Potentially lower recall
```

The actual behavior must be measured on our data.

---

# 26. Plot the Threshold Experiment

We can create a simple table:

```text
| Threshold | Precision | Recall | F1 |
|---:|---:|---:|---:|
| 0.40 | ... | ... | ... |
| 0.50 | ... | ... | ... |
| 0.60 | ... | ... | ... |
| 0.70 | ... | ... | ... |
| 0.80 | ... | ... | ... |
```

Then choose a threshold based on the application's goals.

This is much more defensible than:

```text
0.6 because it feels reasonable.
```

---

# 27. End-to-End Tests

Unit tests test:

```text
one function
```

But we can also test:

```text
whole workflow
```

For example:

```text
Resume text
    ↓
Parser
    ↓
Job parser
    ↓
Matcher
    ↓
Score
```

We can create a known example and verify:

```text
Expected:
strong match
```

This is an **integration test**.

---

# 28. Unit Test vs Integration Test

### Unit test

```text
extract_email()
```

### Integration test

```text
resume text
 ↓
parser
 ↓
matcher
 ↓
result
```

### Application test

```text
Upload file
 ↓
Streamlit
 ↓
OCR
 ↓
Parser
 ↓
Matcher
 ↓
UI
```

Each level catches different classes of problems.

---

# 29. Why We Don't Test Everything Through Streamlit

It is possible to manually click through:

```text
Upload
Analyze
Look at result
```

But this is:

```text
slow
manual
hard to reproduce
easy to forget
```

We want most logic to be testable without the UI.

That is another reason we separated:

```text
UI
```

from:

```text
application logic
```

---

# 30. The Testing Pyramid

We can visualize our testing strategy as:

```text
              /\
             /  \
            / UI \
           /------\
          / Integr \
         /  ation   \
        /------------\
       / Unit Tests   \
      /________________\
```

We generally want:

```text
many unit tests
some integration tests
fewer UI tests
```

because UI tests tend to be more expensive and fragile.

---

# 31. Test the Application's Failure Modes

Create tests for:

```text
Missing resume
Empty resume
Unreadable resume
Empty job description
No skills detected
No semantic matches
Invalid file type
OCR failure
Model loading failure
```

Not every failure needs the same response.

The important thing is to decide:

```text
What should the user see?
What should the developer see?
```

---

# 32. Graceful Failure

Bad:

```text
Traceback...
ValueError...
IndexError...
```

Better:

```text
We couldn't extract readable text
from this document.

Try uploading a clearer PDF or image.
```

And in logs:

```text
OCR processing failed
```

with technical details.

The user shouldn't need to understand Python exceptions.

---

# 33. Test Data Is a Product Asset

Our evaluation resumes and job descriptions are valuable.

They allow us to answer:

```text
Did version 2 improve over version 1?
```

For example:

```text
Version 1 F1: 0.71
Version 2 F1: 0.79
Version 3 F1: 0.84
```

Now improvement is measurable.

Without an evaluation dataset, we are mostly guessing.

---

# 34. Build a Regression Dataset

Every time we discover a meaningful failure:

```text
New failure
    ↓
Add example to evaluation set
```

For example:

```text
Resume uses:
"Technical Expertise"

Parser fails.

Add this resume to test data.

Fix parser.

Run tests.

```

Now that failure should not return unnoticed.

This creates a continuously growing knowledge base for the application.

---

# 35. Golden Examples

Some examples can become permanent reference cases.

For example:

```text
golden/
├── standard_resume
├── unusual_sections
├── missing_email
├── semantic_skill_match
└── weak_job_match
```

These are examples where we know what the system should produce.

Future versions should continue to behave acceptably on them.

---

# 36. Version Your Evaluation

As the application changes:

```text
evaluation_v1
evaluation_v2
```

may become useful.

More commonly, keep one evolving dataset and record:

```text
commit
model version
metrics
threshold
```

For example:

```text
Model:
all-MiniLM-L6-v2

Threshold:
0.62

F1:
0.84
```

This makes experiments reproducible.

---

# 37. Experiment Tracking

Even a simple CSV can help:

```text
experiment,model,threshold,f1
baseline,MiniLM,0.50,0.72
threshold_test,MiniLM,0.60,0.79
threshold_test,MiniLM,0.70,0.76
```

Now we can compare experiments.

Students don't need a sophisticated experiment-tracking platform yet.

The important lesson is:

> **Record what you changed and what happened.**

---

# 38. Model Versioning

Our code currently says:

```python
MODEL_NAME = (
    "all-MiniLM-L6-v2"
)
```

If we change models, our results may change.

Therefore record:

```text
Model name
Model version
Embedding dimension
Threshold
Evaluation dataset
```

Then:

```text
Model change
    ↓
Re-run evaluation
    ↓
Compare metrics
```

Never assume a new model is automatically better.

---

# 39. Data Leakage

There is another important ML concept.

Suppose we tune the threshold repeatedly using our evaluation set:

```text
Try threshold
 ↓
Look at F1
 ↓
Change threshold
 ↓
Look at F1
 ↓
Repeat
```

Eventually we may optimize specifically for that dataset.

Then the score may look excellent on the evaluation set but perform worse on new data.

This is similar to overfitting.

---

# 40. Train / Validation / Test Thinking

Even though our application is not training a traditional classifier here, the same principle applies.

Conceptually:

```text
Development Data
      ↓
Tune rules / thresholds
      ↓
Validation Data
      ↓
Choose configuration
      ↓
Final Test Data
      ↓
Estimate generalization
```

Don't repeatedly optimize against the final test set.

This connects directly back to the train/test split concepts from Phase 3.

---

# 41. Why This Matters

Earlier we learned:

```text
Training data
```

is used to learn.

And:

```text
Test data
```

is used to estimate performance on unseen examples.

Here, even though we may not train a classifier, we still have choices such as:

```text
threshold
weights
skill aliases
semantic rules
```

If we tune all of them on the same final evaluation set, our evaluation becomes less trustworthy.

---

# 42. Application Evaluation

A useful evaluation report might contain:

```text
Parser

Email Precision: ...
Email Recall: ...

Skill Extraction

Precision: ...
Recall: ...
F1: ...

Semantic Matching

Precision: ...
Recall: ...
F1: ...

End-to-End Matching

Strong / Moderate / Weak accuracy: ...
```

Now we can see where the system performs well and where it doesn't.

---

# 43. Error Analysis

Metrics tell us:

```text
Something is wrong.
```

Error analysis tells us:

```text
Why?
```

For example:

```text
False Negative:

Resume:
"Built CNN-based image classifiers."

Job:
"Computer Vision Engineer"

System:
Computer Vision not detected.
```

We can classify the error:

```text
Semantic vocabulary gap
```

Then decide:

```text
Add description?
Change model?
Change threshold?
Add rule?
```

This is much more useful than simply increasing the score.

---

# 44. Create an Error Log

A simple table:

```text
| Input | Expected | Predicted | Error Type |
|---|---|---|---|
| CNN image classifier | CV | None | Semantic gap |
| Technical Expertise | Skills | None | Section alias |
| AWS Cloud | AWS | None | Phrase matching |
```

Now development becomes:

```text
Error
 ↓
Understand
 ↓
Classify
 ↓
Fix
 ↓
Add regression case
 ↓
Re-evaluate
```

This is a professional workflow.

---

# 45. The Intelligent Application Loop

We have now expanded our development loop:

```text
Build
 ↓
Run
 ↓
Observe
 ↓
Evaluate
 ↓
Analyze Errors
 ↓
Improve
 ↓
Test
 ↓
Commit
 ↓
Repeat
```

This loop is one of the most important lessons of Phase 4.

---

# 46. Final Testing Architecture

Our project now has:

```text
                 APPLICATION
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        Unit       Integration    UI
        Tests        Tests       Tests
          │           │           │
          └───────────┼───────────┘
                      ▼
                System Evaluation
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Precision     Recall       F1
                      │
                      ▼
                Error Analysis
                      │
                      ▼
                   Improve
```

This is the complete quality loop.

---

# 47. Student Challenge

Take the current resume-job matcher and add:

```text
1. tests/
2. at least 10 parser tests
3. at least 5 matcher tests
4. at least 3 edge-case tests
5. an evaluation dataset
6. threshold experiments
7. precision / recall / F1
8. an error-analysis table
```

Then run:

```bash
pytest
```

and generate a small evaluation report.

---

# 48. Final Exercise — Break Your Own Application

Don't just test examples that work.

Try to break the system.

Upload:

```text
Empty document
```

Try:

```text
Image with almost no text
```

Try:

```text
Resume with unusual headings
```

Try:

```text
Resume with no skills section
```

Try:

```text
Job with no explicit skills
```

Try:

```text
Very long job description
```

Try:

```text
Resume in an unexpected format
```

For each failure:

```text
Record it
 ↓
Understand it
 ↓
Decide whether to fix it
 ↓
Add a regression test
```

This is how software becomes robust.

---

# 49. The Bigger Lesson

At the beginning of Phase 4, we asked:

> How do we build an intelligent application?

We might have answered:

```text
Use an AI model.
```

Now we know that is incomplete.

A useful intelligent application requires:

```text
Data
+
Preprocessing
+
Models
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
Software Architecture
```

The AI model is only one component.

---

# 50. Final Phase 4 Checkpoint

Once the tests and evaluation are working:

```bash
git status
```

Then:

```bash
pytest
```

Then:

```bash
git add .
```

Then:

```bash
git commit -m "Add automated testing and evaluation"
```

We now have a measurable, testable intelligent application rather than a collection of demos.

---

# 51. Phase 4 Is Complete When...

A student should be able to explain this pipeline:

```text
User Input
    ↓
Validation
    ↓
Document Processing
    ↓
Text Extraction
    ↓
Information Extraction
    ↓
Representation
    ↓
Similarity / Prediction
    ↓
Scoring
    ↓
Evaluation
    ↓
User Interface
```

And, importantly, answer:

> **What happens when one of these steps fails?**

If they can answer that, they are thinking like a software engineer rather than only an ML practitioner.

---

# 52. Final Mental Model

The final mental model for Phase 4 is:

```text
                ┌──────────────────┐
                │      DATA        │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │   PROCESSING     │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │  REPRESENTATION  │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │   INTELLIGENCE   │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │    DECISION      │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │   APPLICATION    │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │    EVALUATION    │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │    ITERATION     │
                └──────────────────┘
```

That loop is the core of building intelligent systems.

We don't simply:

```text
Train model → Done
```

We:

```text
Build
→ Measure
→ Understand
→ Improve
→ Test
→ Deploy
→ Observe
→ Iterate
```

And that brings us back to the development workflow introduced at the very beginning of the curriculum.
