# Project 4.3 — Observability, Feedback, and Continuous Improvement

## A Deployed Application Is Not Finished

We have now:

```text
Built
 ↓
Tested
 ↓
Evaluated
 ↓
Deployed
```

It is tempting to think:

```text
Deployment = Done
```

But real software does not work that way.

Once users begin using the application, we discover things that our original test cases did not contain.

For example:

```text
A resume format we never saw before
A strange PDF
A skill with an unusual name
A job description with unexpected formatting
A slow OCR operation
A semantic match that looks wrong
```

The application is now producing information in the real world.

We need a way to understand what is happening.

This leads us to:

> **Observability and feedback.**

---

# 1. What Is Observability?

At a simple level:

> Observability means being able to understand what is happening inside a system by looking at the information the system produces.

For our application, that means being able to answer:

```text
Did the application start?

Did the resume upload successfully?

Did OCR succeed?

How long did OCR take?

How much text was extracted?

How many skills were detected?

How long did embedding take?

What similarity scores were produced?

Did the matching engine fail?

Did the user receive a result?
```

We don't need to expose all of this to the user.

But the developers should have enough information to diagnose problems.

---

# 2. Three Useful Signals

A simple mental model is:

```text
Logs
Metrics
Errors
```

### Logs

Tell us:

```text
What happened?
```

### Metrics

Tell us:

```text
How often / how much / how fast?
```

### Errors

Tell us:

```text
What failed?
```

Together:

```text
System
  ↓
Observability
  ↓
Understanding
```

---

# 3. Logging

We have already introduced:

```python
import logging
```

For example:

```python
logger.info(
    "Starting resume processing"
)
```

We can log major stages:

```python
logger.info(
    "Starting OCR"
)

logger.info(
    "OCR completed"
)

logger.info(
    "Extracting skills"
)

logger.info(
    "Generating embeddings"
)

logger.info(
    "Calculating match score"
)
```

This gives us a trace of what happened.

---

# 4. Don't Log Everything

More logs are not automatically better.

Imagine:

```text
10,000 lines of logs
```

for one resume.

Finding the actual problem becomes harder.

Prefer meaningful events:

```text
INFO:
Resume processing started

INFO:
OCR completed in 2.4 seconds

INFO:
Extracted 4,821 characters

INFO:
Detected 7 skills

INFO:
Matching completed in 0.8 seconds
```

Good logs answer useful questions.

---

# 5. Log the Right Level

Python logging supports levels such as:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

A simple interpretation:

### DEBUG

Detailed information useful during development.

### INFO

Normal application events.

### WARNING

Something unexpected happened, but the application can continue.

### ERROR

A specific operation failed.

### CRITICAL

The application may not be able to continue.

---

# 6. Example

```python
logger.info(
    "Processing uploaded resume"
)
```

If OCR finds almost no text:

```python
logger.warning(
    "Very little text extracted"
)
```

If OCR crashes:

```python
logger.exception(
    "OCR processing failed"
)
```

Now logs communicate severity.

---

# 7. Metrics

Logs tell us individual events.

Metrics help us see patterns.

For example:

```text
Average OCR time
Average embedding time
Number of resumes processed
Number of failed uploads
Number of OCR failures
Average match score
```

Suppose:

```text
OCR failures:
2%
```

That tells us something very different from one individual error message.

---

# 8. Start With Simple Metrics

We don't need a monitoring platform yet.

During development, we can record:

```python
processing_time
```

and perhaps count:

```text
successful requests
failed requests
```

For an educational application, even a simple in-memory or CSV-based experiment can demonstrate the idea.

---

# 9. Measure Each Stage

Our pipeline is:

```text
Upload
 ↓
OCR
 ↓
Parsing
 ↓
Embedding
 ↓
Matching
 ↓
Scoring
```

Measure each stage separately.

For example:

```text
Upload validation: 0.02 sec
OCR:               2.41 sec
Parsing:           0.03 sec
Embedding:         0.81 sec
Matching:          0.04 sec
```

Now we know:

```text
OCR
```

is our most expensive stage.

---

# 10. Timing Utility

We can create a small helper:

```python
import time


def timed_call(
    function,
    *args,
    **kwargs
):

    start = time.perf_counter()

    result = function(
        *args,
        **kwargs
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    return result, elapsed
```

Then:

```python
text, elapsed = timed_call(
    process_document,
    uploaded_file
)
```

Now:

```python
logger.info(
    "Document processing took %.2f seconds",
    elapsed
)
```

This is a simple example of measuring software rather than guessing.

---

# 11. User Feedback Is Another Signal

Technical metrics aren't enough.

Suppose:

```text
Application response time:
0.8 seconds
```

Excellent.

But users report:

```text
"The match score doesn't make sense."
```

The system is technically fast.

But the product is not useful.

Therefore:

```text
System performance
```

and:

```text
User usefulness
```

are different things.

---

# 12. Add a Feedback Mechanism

A simple Streamlit interface could ask:

```text
Was this result useful?

[ Yes ] [ No ]
```

Or:

```text
How useful was this match?

1 2 3 4 5
```

We don't need to build a sophisticated feedback platform.

The educational lesson is:

> A deployed intelligent system can learn from feedback even if the model itself is not being retrained.

---

# 13. Feedback Is Data

Suppose users review results.

We might collect:

```text
Resume
Job
Predicted Match
User Feedback
```

For example:

```text
Score: 0.82
User: Incorrect
```

Now we have a valuable example.

We can inspect:

```text
Why did the system think this was a strong match?
```

Maybe:

```text
Generic words created high document similarity.
```

Now we have an error case.

---

# 14. The Feedback Loop

The application now has:

```text
User
 ↓
Application
 ↓
Prediction
 ↓
Feedback
 ↓
Error Analysis
 ↓
Improvement
 ↓
New Version
 ↓
Deployment
```

This is a continuous improvement loop.

---

# 15. Feedback Does Not Mean Automatically Retraining

A common misconception is:

```text
User feedback
 ↓
Automatically retrain model
```

We should not do this blindly.

Instead:

```text
Feedback
 ↓
Review
 ↓
Understand
 ↓
Label
 ↓
Evaluate
 ↓
Decide whether to change system
```

This keeps development controlled.

---

# 16. Create an Error Taxonomy

When a result is wrong, categorize the reason.

For example:

```text
OCR Error
Parser Error
Skill Extraction Error
Semantic Matching Error
Scoring Error
UI Error
User Input Error
```

This is extremely useful.

Suppose we collect 100 errors:

```text
OCR             10
Parser          25
Skill extraction 30
Semantic         20
Scoring           5
UI                5
Input             5
```

Now we know where improvement effort may have the greatest impact.

---

# 17. Pareto Thinking

In many systems, a small number of problem categories account for a large portion of failures.

For example:

```text
Skill extraction
+
Parser section detection
```

might explain most errors.

Instead of improving everything simultaneously:

```text
Focus on the biggest sources of failure.
```

This is a practical engineering mindset.

---

# 18. Error Analysis Example

Suppose:

```text
Job:
Computer Vision Engineer
```

and:

```text
Resume:
Built CNN-based image classifiers.
```

Our parser finds:

```text
No explicit "computer vision"
```

and the system gives:

```text
Weak match
```

A human says:

```text
This looks wrong.
```

Let's trace the pipeline:

```text
OCR
 ✓

Text extraction
 ✓

Resume parser
 ✓

Skill extraction
 ✗

Embedding
 never received useful skill information

Scoring
 technically correct based on bad input
```

The root cause is:

```text
Skill extraction
```

not:

```text
Scoring
```

This is why intermediate results matter.

---

# 19. Observability Helps Debug AI

AI systems can fail in ways that aren't obvious.

A final score:

```text
0.42
```

doesn't tell us why.

But if we inspect:

```text
Extracted skills:
Python

Job skills:
Python
Computer Vision
Machine Learning

Semantic matches:
None
```

we can start investigating.

This is why an intelligent application should expose enough intermediate state for debugging.

---

# 20. Add an Internal Debug View

Our Streamlit app can contain:

```python
with st.expander(
    "Developer Details"
):
    st.json(result)
```

During development, we might also show:

```text
Extracted text
Detected sections
Detected skills
Job requirements
Similarity scores
Weights
Threshold
Final score
```

This can be hidden or removed from the public version later.

---

# 21. Explainability

Our application should ideally answer:

> Why did I get this result?

Instead of:

```text
Match Score: 82%
```

show:

```text
Match Score: 82%

Required skills matched:
4 / 5

Semantic relationships:
OpenCV → Computer Vision

Potential gaps:
AWS

Document similarity:
0.76
```

This gives the user a path from:

```text
Input
```

to:

```text
Output
```

---

# 22. Explanation Is Not Proof

We should be careful.

An explanation such as:

```text
OpenCV → Computer Vision
```

does not prove that the candidate is actually competent in computer vision.

It explains:

> Why the system considered these concepts related.

This distinction matters when presenting AI results.

---

# 23. Confidence vs Similarity

Students should also avoid saying:

```text
Similarity = confidence
```

A cosine similarity score is not automatically:

```text
probability
```

For example:

```text
0.82
```

does not mean:

```text
82% probability that the candidate knows the skill.
```

It means something closer to:

> The two representations are relatively close according to the chosen similarity measure.

Our application converts this into a score using additional rules.

---

# 24. Monitor Score Distributions

After deployment, collect aggregate information such as:

```text
Average score
Median score
Minimum
Maximum
```

Suppose suddenly:

```text
Average score:
0.51 → 0.87
```

after a model update.

That is interesting.

Maybe the new model produces generally higher similarity scores.

If our threshold remains:

```text
0.60
```

our matching behavior may change dramatically.

This is called a **distribution shift** in the behavior of the system.

---

# 25. Model Updates Need Evaluation

Suppose we replace:

```text
Model A
```

with:

```text
Model B
```

Don't simply deploy it because:

```text
Model B is newer.
```

Run:

```text
Evaluation dataset
      ↓
Model A
      ↓
Metrics

Evaluation dataset
      ↓
Model B
      ↓
Metrics
```

Compare:

```text
Precision
Recall
F1
Latency
Memory
```

Then make the decision.

---

# 26. Monitor Application Performance Too

A model can be more accurate but much slower.

For example:

```text
Model A
F1: 0.81
Latency: 0.8 sec

Model B
F1: 0.84
Latency: 6.5 sec
```

Is Model B better?

Not automatically.

It depends on the application's requirements.

We are now making an engineering trade-off:

```text
Quality
   ↕
Speed
   ↕
Cost
```

---

# 27. Quality vs Cost

A larger model may produce:

```text
Better semantic matching
```

but require:

```text
More RAM
More CPU
Longer startup
More expensive hosting
```

A smaller model may be:

```text
Slightly less accurate
```

but:

```text
Much faster
Much cheaper
Easier to deploy
```

Real engineering is often about choosing a good balance.

---

# 28. Regression After Deployment

Suppose version 1 gives:

```text
F1 = 0.82
```

We improve the parser.

Version 2 gives:

```text
F1 = 0.85
```

Great.

But perhaps:

```text
OCR failure rate:
2% → 8%
```

We improved one component while damaging another.

Therefore evaluate the whole system after meaningful changes.

---

# 29. System-Level Metrics

Our dashboard might eventually contain:

```text
Documents processed
Successful analyses
Failed analyses
Average processing time
OCR failure rate
Average match score
User feedback score
```

This gives us a picture of system health.

---

# 30. Don't Optimize a Single Metric Blindly

Suppose:

```text
Average match score
```

increases.

That doesn't necessarily mean:

```text
Application quality increased.
```

Maybe we simply lowered the threshold.

For example:

```text
Threshold:
0.70 → 0.40
```

Now many more skills are considered matches.

The average score may look better while precision gets worse.

Always connect metrics to the behavior they represent.

---

# 31. Build an Evaluation Dashboard

For educational purposes, create a simple Streamlit page:

```text
Model Evaluation

Precision    0.84
Recall       0.79
F1           0.81

Average OCR Time
2.4 sec

Average Embedding Time
0.8 sec
```

Then show:

```text
Threshold Experiment
```

and:

```text
Error Categories
```

This gives students a concrete view of system evaluation.

---

# 32. Separate User UI From Developer UI

The user may only need:

```text
Match Score
Strengths
Gaps
Explanation
```

The developer may need:

```text
Raw text
Embeddings
Threshold
Timing
Errors
Model version
```

These are different audiences.

A useful design might have:

```text
Main application
```

and:

```text
Developer / Evaluation mode
```

---

# 33. Feature Flags

A simple configuration can control development features:

```python
DEBUG = True
```

Then:

```python
if DEBUG:

    st.write(
        result
    )
```

In deployment:

```text
DEBUG = False
```

This is an introduction to the concept of **feature flags** and environment-specific behavior.

---

# 34. Reproducible Experiments

Every meaningful experiment should record:

```text
Code version
Model
Threshold
Weights
Dataset
Metrics
Notes
```

For example:

```text
Experiment: semantic-threshold-03

Code:
commit abc123

Model:
all-MiniLM-L6-v2

Threshold:
0.65

F1:
0.83

Notes:
Reduced false positives.
```

This makes experiments understandable later.

---

# 35. Git as the Experiment Timeline

This connects directly to Phase 0.

Remember:

```text
Experiment
 ↓
Develop
 ↓
Git Checkpoint
```

Now:

```text
Experiment
 ↓
Measure
 ↓
Git Commit
 ↓
Deploy
 ↓
Observe
 ↓
Feedback
 ↓
Improve
```

Git gives us a history of how the system evolved.

---

# 36. Version the Application

Use a version:

```python
APP_VERSION = "1.1.0"
```

Then the UI can show:

```text
Resume Matcher v1.1.0
```

If a user reports:

```text
"The result looked wrong."
```

we can ask:

```text
Which version?
```

That is much more useful than:

```text
"It was the latest version."
```

---

# 37. Semantic Versioning

A simple version format is:

```text
MAJOR.MINOR.PATCH
```

For example:

```text
1.0.0
```

A rough educational interpretation:

```text
MAJOR
Breaking changes

MINOR
New features

PATCH
Bug fixes
```

Students don't need to follow this perfectly.

The important lesson is to identify application versions clearly.

---

# 38. Release Notes

For a meaningful release, write:

```text
Version 1.1.0

Added:
- Semantic skill explanations
- Developer evaluation view

Improved:
- Section detection

Fixed:
- Empty job description crash
```

This gives users and developers a record of what changed.

---

# 39. User Feedback → Regression Test

This is one of the most valuable loops.

Suppose a user reports:

> "My resume says 'Technical Expertise' instead of 'Skills', and the parser missed everything."

We should:

```text
User report
 ↓
Reproduce
 ↓
Add example to test data
 ↓
Fix parser
 ↓
Run tests
 ↓
Evaluate
 ↓
Deploy
```

Now that failure should be much less likely to return.

---

# 40. User Feedback → Better Dataset

Another user might report:

> "The system thinks OpenCV and computer vision are unrelated."

Add the example:

```text
OpenCV
Computer Vision
```

to the semantic evaluation dataset.

Now future models and thresholds can be evaluated against it.

The application becomes better partly because its **evaluation data becomes better**.

---

# 41. The Dataset Becomes an Asset

At the beginning:

```text
Evaluation data
```

was a small collection of examples.

Over time:

```text
Real failure cases
+
Validated examples
+
Human feedback
```

create a valuable dataset.

This dataset helps us:

```text
test
compare
debug
improve
```

future versions.

---

# 42. Human-in-the-Loop

Our system can be thought of as:

```text
AI
 ↓
Suggestion
 ↓
Human
 ↓
Feedback
```

The human remains part of the decision process.

This is particularly appropriate for our resume application.

The system can say:

```text
Potential Match
```

rather than:

```text
Definitive Candidate Decision
```

---

# 43. Why Human Review Matters

Our system can miss:

```text
Transferable skills
Unusual terminology
Context
Career changes
Equivalent experience
```

A human can recognize these things.

Therefore the application should support:

```text
Human review
```

rather than pretending the score is infallible.

---

# 44. Build for Inspection

A strong intelligent application should make it easy to inspect:

```text
What did the system read?

What did it extract?

What did it compare?

What did it consider a match?

How was the score calculated?
```

This is especially important when the output affects someone's decisions.

---

# 45. Final Architecture

Our application now has a feedback loop around it:

```text
                       ┌───────────────┐
                       │     USER      │
                       └───────┬───────┘
                               │
                               ▼
                        Streamlit App
                               │
                               ▼
                         AI Pipeline
                               │
                               ▼
                           Result
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
                 User                  Logs
               Feedback                Metrics
                    │                     │
                    └──────────┬──────────┘
                               ▼
                         Error Analysis
                               │
                               ▼
                         Evaluation Data
                               │
                               ▼
                            Improve
                               │
                               ▼
                         New Version
                               │
                               ▼
                           Deploy
                               │
                               └──────────────→
```

This is the mature version of our development loop.

---

# 46. The Complete Intelligent System

At this point:

```text
Data
 ↓
Processing
 ↓
Representation
 ↓
AI
 ↓
Decision
 ↓
Interface
 ↓
Deployment
 ↓
Observation
 ↓
Feedback
 ↓
Evaluation
 ↓
Improvement
```

The system continuously moves through this cycle.

That is what makes it an **intelligent application**, rather than simply a script that calls a model.

---

# 47. Student Challenge

Add an evaluation / developer mode to the application.

It should display:

```text
Application Version
Model Version
Threshold
Processing Times
Extracted Skills
Matched Skills
Missing Skills
Similarity Scores
```

Then add:

```text
Feedback:
[Useful]
[Not Useful]
```

Store development feedback in a simple local file or dataset.

Do not store unnecessary personal information.

---

# 48. Student Challenge — Error Analysis

Take at least:

```text
20 resume/job examples
```

and manually inspect incorrect results.

Create:

```text
error_analysis.csv
```

with columns such as:

```text
example_id
expected
predicted
error_type
notes
```

Then calculate:

```text
Errors by category
```

Ask:

> Which part of the pipeline causes the most problems?

---

# 49. Student Challenge — Improve the System

Choose the largest error category.

For example:

```text
Skill extraction
```

Improve it.

Then:

```text
Run tests
 ↓
Run evaluation
 ↓
Compare metrics
```

Record:

```text
Before:
F1 = ...

After:
F1 = ...
```

Now students have demonstrated an actual engineering improvement.

---

# 50. Student Challenge — Release a New Version

After the improvement:

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
git commit -m "Improve semantic skill matching"
```

Update:

```text
APP_VERSION
```

and write:

```text
CHANGELOG
```

Then deploy.

This completes the loop:

```text
Problem
 ↓
Experiment
 ↓
Change
 ↓
Test
 ↓
Evaluate
 ↓
Commit
 ↓
Release
 ↓
Deploy
```

---

# 51. Final Phase 4 Architecture

Students can now draw the entire system:

```text
                         USER
                           │
                           ▼
                    STREAMLIT UI
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
          RESUME                    JOB DESCRIPTION
              │                         │
              ▼                         ▼
       DOCUMENT READER              JOB PARSER
              │                         │
              ▼                         │
            OCR                         │
              │                         │
              ▼                         │
        RESUME PARSER                   │
              │                         │
              └────────────┬────────────┘
                           ▼
                    MATCHING ENGINE
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          EXACT        SEMANTIC       DOCUMENT
          MATCH         MATCH         SIMILARITY
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                      SCORING
                           │
                           ▼
                     MATCH REPORT
                           │
                           ▼
                         USER
                           │
                     ┌─────┴─────┐
                     ▼           ▼
                  FEEDBACK     LOGS
                     │           │
                     └─────┬─────┘
                           ▼
                    ERROR ANALYSIS
                           │
                           ▼
                     EVALUATION
                           │
                           ▼
                       IMPROVE
                           │
                           ▼
                       RELEASE
                           │
                           ▼
                       DEPLOY
                           │
                           └───────────→ USER
```

This is the complete lifecycle.

---

# 52. What Students Should Understand Now

The important takeaway is not:

```text
How to add logging.
```

or:

```text
How to create a Streamlit feedback button.
```

The important takeaway is:

> **Once software is deployed, the real world becomes part of the development process.**

Users create new inputs.

New inputs reveal failures.

Failures become evaluation examples.

Evaluation examples drive improvements.

Improvements become new releases.

---

# 53. The Final Engineering Loop

The entire curriculum can now be summarized as:

```text
                  EXPERIMENT
                       │
                       ▼
                    BUILD
                       │
                       ▼
                     TEST
                       │
                       ▼
                   EVALUATE
                       │
                       ▼
                    DEPLOY
                       │
                       ▼
                   OBSERVE
                       │
                       ▼
                  GET FEEDBACK
                       │
                       ▼
                 ANALYZE ERRORS
                       │
                       ▼
                   IMPROVE
                       │
                       ▼
                  GIT CHECKPOINT
                       │
                       └──────────────→ EXPERIMENT
```

This is the software engineering loop behind intelligent systems.

---

# 54. Final Phase 4 Capstone

The final application should now demonstrate:

```text
Python
        ↓
Real-world data
        ↓
EDA mindset
        ↓
Regex
        ↓
OCR
        ↓
Computer Vision
        ↓
NLP
        ↓
TF-IDF
        ↓
Cosine Similarity
        ↓
Embeddings
        ↓
Machine Learning evaluation
        ↓
Deep Learning representation
        ↓
Streamlit
        ↓
Testing
        ↓
Deployment
        ↓
Observability
        ↓
Feedback
        ↓
Iteration
```

Students should be able to explain not only:

> **"How does this model work?"**

but also:

> **"How does this entire system work, how do we know it works, and what do we do when it doesn't?"**

That is the real endpoint of Phase 4.

---

# 55. Final Git Checkpoint

When the feedback and observability layer is complete:

```bash
git status
```

Run:

```bash
pytest
```

Run the evaluation:

```text
evaluation/
```

Then:

```bash
git add .
```

and:

```bash
git commit -m "Add observability feedback and continuous improvement"
```

The application now has a complete development lifecycle.

---

# 56. Final Takeaway

We began Phase 4 with individual techniques.

Now they form a system:

```text
OCR
 +
Parsing
 +
NLP
 +
Embeddings
 +
Similarity
 +
Scoring
 +
Streamlit
 +
Testing
 +
Deployment
 +
Feedback
```

And the final mental model is:

> **Build the system, measure the system, learn from the system, and improve the system.**

That is how intelligent software is developed in the real world.
