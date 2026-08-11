# Project 4.7 — Independent Project Blueprint

## From Following Projects to Choosing Problems

Phase 4 has taught us how to build an intelligent application from beginning to end.

Now we remove the structure.

There is no:

```text
"Build this exact application."
```

Instead:

> **Choose a problem and design your own intelligent system.**

This is the bridge between:

```text
Course Project
```

and:

```text
Independent Project
```

---

# 1. Start With a Problem

Do not begin with:

```text
"I want to use a transformer."
```

Start with:

```text
"I have a problem."
```

For example:

```text
People have difficulty organizing documents.
```

Then ask:

```text
What information exists?
What makes the task difficult?
Could software help?
Where could AI be useful?
```

---

# 2. Problem Statement

Write a one-paragraph problem statement.

Use:

```text
Who?
What problem?
Why does it matter?
What does the application do?
```

For example:

```text
Students often receive large collections of lecture
documents and have difficulty finding relevant material.

The application will allow users to upload documents,
search them semantically, and return the most relevant
sections with explanations.
```

Keep it specific.

---

# 3. Define the User

Identify:

```text
Primary user
```

For example:

```text
Student
Recruiter
Teacher
Developer
Researcher
Small business owner
```

Then ask:

> What does this person actually need?

This prevents building a technically interesting application that nobody can use.

---

# 4. Define the Input

Every intelligent application begins with some input.

Examples:

```text
PDF
Image
CSV
Text
Audio
Video
User question
Web page
Database record
```

Write:

```text
Input:
PDF documents
```

Then define:

```text
Expected format
Maximum size
Potential problems
```

---

# 5. Define the Output

What should the application produce?

For example:

```text
Input:
Document

Output:
Extracted information
+
Summary
+
Relevant sections
```

Or:

```text
Input:
Image

Output:
Detected objects
+
Bounding boxes
+
Classification
```

The output should be observable and testable.

---

# 6. Draw the Simplest Pipeline

Before writing code, draw:

```text
INPUT
  ↓
PROCESSING
  ↓
REPRESENTATION
  ↓
MODEL / RULES
  ↓
OUTPUT
```

Then make it specific.

For example:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
Similarity Search
 ↓
Relevant Sections
```

This becomes the first architecture draft.

---

# 7. Choose the Simplest Technique

Do not automatically choose deep learning.

Ask:

> What is the simplest method that could reasonably solve this problem?

Possible approaches:

```text
Rules
Regex
Keyword matching
TF-IDF
Cosine similarity
Classical ML
Embeddings
Neural networks
Computer vision
LLMs
```

Start as low in the list as practical.

---

# 8. Build a Baseline

Before building an advanced system, create a baseline.

For example:

```text
Version 0

Keyword matching
```

Then:

```text
Version 1

TF-IDF
+
Cosine similarity
```

Then:

```text
Version 2

Embeddings
+
Semantic similarity
```

Now you can measure whether each additional layer actually helps.

---

# 9. Why Baselines Matter

Suppose:

```text
Keyword system:
F1 = 0.74
```

and:

```text
Embedding system:
F1 = 0.75
```

The sophisticated model improved the metric only slightly.

That is important information.

Maybe:

```text
The simpler system is preferable.
```

This is a real engineering conclusion.

---

# 10. Define Success Before Building

Write down:

```text
What does "good" mean?
```

For a classification system:

```text
Accuracy
Precision
Recall
F1
```

For regression:

```text
MAE
MSE
RMSE
R²
```

For retrieval:

```text
Precision@K
Recall@K
MRR
```

For an application:

```text
Latency
Failure rate
User feedback
Task completion
```

The exact metric depends on the problem.

---

# 11. Create a Small Dataset

Do not wait until you have:

```text
100,000 examples
```

Start with:

```text
20
50
100
```

good examples.

The purpose is to learn:

```text
What does the data actually look like?
```

---

# 12. Inspect the Data

Use the EDA skills from earlier phases.

Ask:

```text
Are values missing?

Are labels balanced?

Are there duplicates?

Are there strange inputs?

Are some categories underrepresented?

Are there obvious errors?
```

The dataset is part of the application.

---

# 13. Create Ground Truth

If your application makes predictions, define what the correct answer means.

For example:

```text
Document A
Query B

Expected:
Relevant
```

or:

```text
Image A
Expected class:
Cat
```

Without a definition of correctness:

```text
Evaluation
```

becomes difficult.

---

# 14. Separate Development and Evaluation Data

Do not repeatedly tune the system on the exact same examples you use to report final performance.

Use:

```text
Development examples
```

for experimentation.

Keep:

```text
Final evaluation examples
```

for the final check.

This connects back to the train/test split concepts from Phase 3.

---

# 15. Error Analysis Comes Before Complexity

Suppose the baseline fails.

Do not immediately add:

```text
A larger neural network
```

First ask:

```text
Why did it fail?
```

Possible reasons:

```text
Bad input
Missing data
Incorrect preprocessing
Wrong threshold
Weak features
Incorrect labels
Model limitation
```

The answer tells you what to improve.

---

# 16. Decide Where AI Is Needed

Not every part of the application needs AI.

For example:

```text
File validation
→ Rule

Text cleaning
→ Regex

Date parsing
→ Rule / library

Semantic matching
→ Embeddings

Final score
→ Explicit formula
```

This is often better than:

```text
AI everywhere
```

---

# 17. AI Should Solve a Specific Subproblem

Instead of:

```text
"Build an AI application."
```

think:

```text
"Use semantic representations to solve
the ambiguity in document matching."
```

This creates a clearer architecture.

---

# 18. Keep Deterministic Logic Deterministic

If something can be solved reliably with:

```python
if ...
```

there is often no reason to replace it with a model.

For example:

```text
Allowed file type
```

should be deterministic.

So should:

```text
Maximum file size
```

and often:

```text
Score calculation
```

AI should be used where uncertainty or representation is genuinely useful.

---

# 19. Design the Application Boundary

Separate:

```text
User Interface
```

from:

```text
Core Logic
```

For example:

```text
app.py
   ↓
service layer
   ↓
core modules
```

This makes the application easier to test.

---

# 20. Design Functions Around Responsibilities

Prefer:

```python
extract_text()
parse_resume()
extract_skills()
generate_embeddings()
find_matches()
calculate_score()
```

over:

```python
do_everything()
```

A function should have a clear responsibility.

---

# 21. Build One Vertical Slice

Do not build:

```text
10 modules
```

before testing anything.

Instead:

```text
Input
 ↓
One transformation
 ↓
One result
```

Make that work.

Then expand.

This is often called:

> Building a vertical slice.

---

# 22. Example Vertical Slice

Suppose the project is:

```text
Invoice Analyzer
```

Start with:

```text
Upload one invoice
 ↓
Extract text
 ↓
Find total amount
 ↓
Display total
```

Once this works:

```text
Add date
Add vendor
Add line items
Add validation
Add evaluation
```

This reduces complexity.

---

# 23. Version the Project

Use:

```text
v0.1
```

for the first working prototype.

Then:

```text
v0.2
```

after a meaningful improvement.

Eventually:

```text
v1.0
```

when the core application is complete.

Git becomes the project timeline.

---

# 24. Keep an Experiment Log

Create:

```text
experiments.md
```

Record:

```text
Experiment
Hypothesis
Change
Metric
Result
Conclusion
```

Example:

```text
Experiment:
Semantic threshold

Hypothesis:
0.65 will reduce false positives.

Result:
F1 improved from 0.78 to 0.82.

Conclusion:
Use 0.65 for the next version.
```

---

# 25. Don't Hide Failed Experiments

A failed experiment is useful.

For example:

```text
Tried:
Larger embedding model

Result:
F1 +0.01
Latency +4x

Decision:
Keep smaller model.
```

This demonstrates engineering judgment.

---

# 26. Architecture Evolves

Your first architecture may be:

```text
app.py
```

Then:

```text
app.py
parser.py
matcher.py
```

Then:

```text
app.py
services/
models/
tests/
data/
```

This is normal.

Architecture should evolve as understanding improves.

---

# 27. Define Non-Goals

Write:

```text
This project will NOT:
```

For example:

```text
- Make autonomous hiring decisions
- Store resumes permanently
- Support every document format
- Train a custom foundation model
```

Non-goals protect the project from uncontrolled scope.

---

# 28. Define Constraints

Examples:

```text
Maximum project duration:
2 weeks

Maximum upload:
10 MB

Supported files:
PDF and PNG

Deployment:
Streamlit

Model:
Pretrained embedding model
```

Constraints make the project manageable.

---

# 29. MVP

Define the:

> **Minimum Viable Product**

The MVP should be the smallest useful version.

For example:

```text
MVP:

Upload PDF
 ↓
Extract text
 ↓
Search relevant content
 ↓
Display result
```

Everything else is secondary.

---

# 30. Features After the MVP

Create:

```text
MVP
 ↓
Feature 1
 ↓
Feature 2
 ↓
Feature 3
```

Do not attempt everything simultaneously.

Possible future features:

```text
History
Export
Authentication
Multiple documents
Better visualization
Advanced model
Feedback
```

---

# 31. Evaluate Every Major Feature

If you add:

```text
Embeddings
```

evaluate them.

If you add:

```text
OCR
```

evaluate it.

If you add:

```text
New scoring weights
```

evaluate them.

Do not assume:

```text
New feature = Better system
```

---

# 32. Test the Happy Path

First test:

```text
Normal input
 ↓
Expected processing
 ↓
Expected result
```

Then test:

```text
Bad input
```

Then:

```text
Edge cases
```

Then:

```text
Unexpected combinations
```

This creates layered confidence.

---

# 33. Build a Regression Suite

Every important bug should become:

```text
A test case
```

For example:

```text
Bug:
Two-column PDF lost skills.

Fix:
Improved extraction.

Regression test:
two_column_resume.pdf
```

Now future changes should not silently reintroduce the bug.

---

# 34. Deploy Early

Do not wait until:

```text
Everything is perfect.
```

Deploy a small version early.

For example:

```text
MVP
 ↓
Deploy
 ↓
Test externally
 ↓
Find problems
 ↓
Improve
```

Deployment reveals problems that local development may hide.

---

# 35. Observe Real Usage

If users can provide feedback, collect:

```text
What worked?
What failed?
What was confusing?
What result looked wrong?
```

Turn useful feedback into engineering tasks.

---

# 36. Responsible Design

Ask:

```text
Could this system harm someone?

Could the result be misunderstood?

Does it process personal information?

What happens when it is wrong?

Should a human review the output?
```

These questions belong in the design phase, not only at the end.

---

# 37. Final Project Proposal

Before coding, submit a one-page proposal.

Use:

```text
Project Name:

Problem:

Target User:

Input:

Output:

MVP:

AI Component:

Baseline:

Evaluation Metric:

Dataset:

Architecture:

Deployment:

Known Risks:

Non-Goals:

Future Improvements:
```

This proposal becomes the contract for the project.

---

# 38. Project Proposal Example

```text
Project Name:
Document Knowledge Search

Problem:
Users struggle to find relevant information
inside large collections of documents.

Target User:
Students and researchers.

Input:
PDF documents + text query.

Output:
Top relevant passages.

MVP:
Upload PDFs and search them.

AI Component:
Sentence embeddings.

Baseline:
TF-IDF + cosine similarity.

Evaluation:
Precision@5 and manual relevance labels.

Deployment:
Streamlit.

Risk:
Poor retrieval for unusual terminology.
```

Notice that the project is already understandable before any code exists.

---

# 39. Architecture Review

Before implementation, ask another person:

> Can you explain my architecture back to me?

If they cannot:

```text
Simplify the architecture.
```

A good architecture should be understandable before it is complicated.

---

# 40. Implementation Milestones

Break the project into checkpoints.

For example:

```text
Milestone 1
Input works

Milestone 2
Core processing works

Milestone 3
Baseline works

Milestone 4
AI component works

Milestone 5
Evaluation works

Milestone 6
UI works

Milestone 7
Tests pass

Milestone 8
Deployment works

Milestone 9
Documentation complete
```

Commit after meaningful milestones.

---

# 41. Final Evaluation

At the end, report:

```text
Baseline:
...

Final system:
...

Metric:
...

Improvement:
...

Latency:
...

Known failures:
...
```

Do not hide the baseline.

The improvement is part of the story.

---

# 42. Final Demo

The final demonstration should contain:

```text
Problem
 ↓
Architecture
 ↓
Live application
 ↓
Example input
 ↓
Example output
 ↓
Evaluation
 ↓
Failure case
 ↓
Engineering decision
 ↓
Limitation
 ↓
Next step
```

This is enough to communicate the project clearly.

---

# 43. Final Repository

A strong independent project might look like:

```text
my-intelligent-application/
│
├── app.py
│
├── src/
│   ├── processor.py
│   ├── model.py
│   ├── matcher.py
│   └── scoring.py
│
├── tests/
│
├── data/
│   ├── sample/
│   └── evaluation/
│
├── experiments.md
├── requirements.txt
├── .gitignore
├── README.md
└── CHANGELOG.md
```

The exact structure can differ.

The principle is:

```text
Clear
Modular
Testable
Reproducible
Documented
```

---

# 44. Independent Project Rubric

A possible rubric:

| Area | Weight |
|---|---:|
| Problem definition | 10% |
| Architecture | 15% |
| Implementation | 20% |
| AI component | 10% |
| Evaluation | 15% |
| Testing | 10% |
| Deployment | 5% |
| Documentation | 5% |
| Responsible design | 5% |
| Presentation | 5% |

The project should be judged on engineering quality rather than model complexity.

---

# 45. What Not to Reward

Avoid rewarding:

```text
Largest model
Most libraries
Most lines of code
Most complicated architecture
```

A smaller project with:

```text
clear problem
clean architecture
good evaluation
strong testing
honest limitations
```

is often a better engineering project.

---

# 46. The Independence Test

The final question is:

> If the tutorial disappeared, could you build something similar?

If the answer is:

```text
Yes
```

then the student has crossed an important threshold.

They no longer need a tutorial for every step.

They can:

```text
Search documentation
Read examples
Experiment
Debug
Evaluate
Build
```

That is the goal.

---

# 47. Final Transition

At the beginning of Phase 4:

```text
Follow the architecture.
```

Then:

```text
Modify the architecture.
```

Then:

```text
Build the architecture.
```

Finally:

```text
Choose the architecture.
```

This is the progression from:

```text
Student
```

to:

```text
Independent developer.
```

---

# 48. Final Takeaway

The most important skill students should leave Phase 4 with is not:

```text
How to use a particular AI library.
```

It is:

> **How to take an ambiguous problem and turn it into a measurable, testable, deployable software system.**

The tools will change.

The models will change.

The frameworks will change.

The engineering process remains.

---

# 49. End of the Guided Phase

Phase 4 began with:

```text
Anatomy of an Intelligent Application
```

and ends with:

```text
Choose your own problem.
```

That is intentional.

The curriculum has moved from:

```text
"What should I build?"
```

to:

```text
"What should I build, and why?"
```

And eventually:

```text
"How would I design the best system for this problem?"
```

That is where independent engineering begins.
