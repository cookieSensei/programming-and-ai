# Project 2.3 — Embeddings for Semantic Matching

## From Words to Meaning

Our resume matcher has now gone through two stages.

### Version 1

```text
Resume
 ↓
Regex / Rules
 ↓
Exact Skills
```

### Version 2

```text
Resume
 ↓
TF-IDF
 ↓
Cosine Similarity
 ↓
Similar Skills
```

TF-IDF improved our system because we no longer require an exact phrase.

But we discovered a limitation.

Consider:

```text
Resume:

Developed convolutional neural networks
for image classification.
```

and:

```text
Skill:

Computer Vision
```

A human can immediately see a relationship.

TF-IDF may struggle because the important words are different.

We now want a representation that captures more of the **meaning** of text.

This leads us to:

> **Embeddings**

---

# 1. What Is an Embedding?

An embedding is a numerical representation of some data.

For text:

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

For example, conceptually:

```text
"Python programming"
        ↓
[0.12, -0.34, 0.71, ...]
```

The actual vector is usually much larger than this.

The important idea is:

> **Similar pieces of text should ideally produce vectors that are close together in the embedding space.**

---

# 2. Compare This With TF-IDF

Our previous system was:

```text
Text
 ↓
TF-IDF
 ↓
Vector
```

TF-IDF primarily represents:

```text
Which words occur?
How important are those words?
```

An embedding model attempts to represent:

```text
What does this text mean?
```

This is a major conceptual shift.

---

# 3. Same Similarity Function, Better Representation

This is an important point.

We can still use:

```python
cosine_similarity()
```

The difference is what we put into it.

Previously:

```text
TF-IDF vectors
      ↓
Cosine similarity
```

Now:

```text
Embedding vectors
      ↓
Cosine similarity
```

So:

> **Cosine similarity is the comparison mechanism. The embedding is the representation.**

This distinction is worth remembering.

---

# 4. Install an Embedding Library

We will use:

```text
sentence-transformers
```

Install it:

```bash
pip install sentence-transformers
```

Add it to:

```text
requirements.txt
```

```text
sentence-transformers
```

We will continue using:

```python
from sklearn.metrics.pairwise import cosine_similarity
```

for the actual similarity calculation.

---

# 5. Load an Embedding Model

Import:

```python
from sentence_transformers import SentenceTransformer
```

Then:

```python
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
```

The first time the model is loaded, the library may need to download the model files.

After loading, we can give it text.

---

# 6. Generate an Embedding

For example:

```python
text = "Python developer"

embedding = model.encode(
    text
)

print(
    embedding.shape
)
```

The result is a numerical vector.

Conceptually:

```text
"Python developer"
        ↓
Embedding model
        ↓
[0.12, -0.08, 0.41, ...]
```

We can inspect:

```python
print(embedding)
```

But don't try to interpret individual dimensions.

Unlike a simple feature such as:

```text
number of times "Python" occurs
```

an embedding dimension does not usually have an intuitive standalone meaning.

---

# 7. Generate Multiple Embeddings

We can encode multiple pieces of text:

```python
texts = [
    "computer vision",
    "image classification using neural networks",
    "database administration"
]

embeddings = model.encode(
    texts
)
```

Now:

```text
embeddings
```

contains one vector per text.

Conceptually:

```text
Text 1 ──→ Vector 1
Text 2 ──→ Vector 2
Text 3 ──→ Vector 3
```

---

# 8. Calculate Similarity

We can use the same tool from scikit-learn:

```python
from sklearn.metrics.pairwise import cosine_similarity
```

Then:

```python
scores = cosine_similarity(
    [embeddings[0]],
    embeddings[1:]
)

print(scores)
```

Now we can compare:

```text
computer vision
```

against:

```text
image classification using neural networks
```

and:

```text
database administration
```

The embedding representation can capture relationships that are difficult for simple word overlap.

The exact score depends on the embedding model and text.

---

# 9. Important: Similarity Is Not Understanding

Do not make this mistake:

> "Embeddings understand language exactly like humans."

They don't.

An embedding model is a learned representation.

It can encode useful patterns about language and semantic relationships.

But it can still:

- misunderstand text
- produce unexpected similarities
- miss important context
- reflect biases in its training data
- fail on specialized terminology

So embeddings are a more powerful representation.

They are not magic.

---

# 10. Compare TF-IDF and Embeddings

Let's create a small experiment.

```python
resume_text = """
Developed convolutional neural networks
for image classification and object detection.
"""
```

And:

```python
skill = "computer vision"
```

First:

```text
TF-IDF
```

Then:

```text
Embedding
```

The experiment is:

```text
                 Resume
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
       TF-IDF             Embedding
          │                   │
          ▼                   ▼
       Vector              Vector
          │                   │
          └─────────┬─────────┘
                    ▼
             Cosine Similarity
```

The similarity function stays the same.

The representation changes.

---

# 11. Build an Embedding Skill Matcher

Let's reuse our earlier skill knowledge base.

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
    """,

    "deep learning": """
    deep learning neural networks
    CNN transformers representation learning
    """,

    "sql": """
    SQL databases relational databases
    querying data
    """
}
```

We can embed every skill description.

---

# 12. Encode Skill Descriptions

```python
skills = list(
    SKILL_DESCRIPTIONS.keys()
)

skill_descriptions = list(
    SKILL_DESCRIPTIONS.values()
)

skill_embeddings = model.encode(
    skill_descriptions
)
```

Now:

```text
Python description
        ↓
Vector

Machine Learning description
        ↓
Vector

Computer Vision description
        ↓
Vector
```

---

# 13. Encode the Resume

```python
resume_embedding = model.encode(
    resume_text
)
```

Now we have:

```text
Resume
   ↓
Vector
```

and:

```text
Skill descriptions
   ↓
Vectors
```

All vectors come from the same embedding model.

This is important because they now exist in the same representation space.

---

# 14. Compare the Resume With Every Skill

```python
scores = cosine_similarity(
    [resume_embedding],
    skill_embeddings
)[0]
```

Now we have:

```text
Python              → score
Machine Learning    → score
Computer Vision     → score
Deep Learning       → score
SQL                 → score
```

Let's create readable results.

```python
results = []

for skill, score in zip(
    skills,
    scores
):

    results.append({
        "skill": skill,
        "score": float(score)
    })
```

Sort them:

```python
results = sorted(
    results,
    key=lambda x: x["score"],
    reverse=True
)
```

Now we have a ranked list.

---

# 15. Build a Reusable Function

Create:

```python
def calculate_embedding_skill_scores(
    resume_text,
    skill_descriptions,
    model
):

    skills = list(
        skill_descriptions.keys()
    )

    descriptions = list(
        skill_descriptions.values()
    )

    resume_embedding = model.encode(
        resume_text
    )

    skill_embeddings = model.encode(
        descriptions
    )

    scores = cosine_similarity(
        [resume_embedding],
        skill_embeddings
    )[0]

    results = []

    for skill, score in zip(
        skills,
        scores
    ):

        results.append({
            "skill": skill,
            "score": float(score)
        })

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )
```

Then:

```python
results = calculate_embedding_skill_scores(
    resume_text,
    SKILL_DESCRIPTIONS,
    model
)
```

---

# 16. Compare With the TF-IDF Version

We now have two functions:

```python
calculate_skill_scores(...)
```

using:

```text
TF-IDF
```

and:

```python
calculate_embedding_skill_scores(...)
```

using:

```text
Embeddings
```

Both return approximately the same type of result:

```python
[
    {
        "skill": "...",
        "score": 0.42
    }
]
```

This is excellent for comparison.

---

# 17. Create a Side-by-Side Experiment

For the same resume, calculate:

```python
tfidf_results = calculate_skill_scores(
    resume_text,
    SKILL_DESCRIPTIONS
)

embedding_results = (
    calculate_embedding_skill_scores(
        resume_text,
        SKILL_DESCRIPTIONS,
        model
    )
)
```

Then display:

```text
Skill                TF-IDF       Embedding

Computer Vision      0.12         0.71
Deep Learning        0.18         0.76
Machine Learning     0.24         0.68
Python               0.43         0.51
SQL                  0.00         0.08
```

The numbers above are illustrative.

Your results will depend on:

- the exact text
- the descriptions
- the model
- preprocessing

The important thing is to compare the behavior, not memorize a particular score.

---

# 18. What Changed?

The pipeline changed from:

```text
Resume
 ↓
TF-IDF
 ↓
Word-based vector
 ↓
Cosine similarity
```

to:

```text
Resume
 ↓
Embedding model
 ↓
Semantic vector
 ↓
Cosine similarity
```

The final mathematical operation is still:

```python
cosine_similarity(...)
```

But the representation has changed dramatically.

---

# 19. Why Embeddings Can Capture More

Suppose we have:

```text
Text A:

Built object detection systems.
```

and:

```text
Text B:

Computer vision experience.
```

There may be little literal word overlap.

But an embedding model may have learned from language patterns that these concepts frequently occur in related contexts.

So the vectors may be closer.

Conceptually:

```text
Object Detection
       │
       │ semantic relationship
       │
       ▼
Computer Vision
```

This is what we mean by **semantic similarity**.

---

# 20. Test Synonyms and Related Concepts

Create experiments such as:

```python
pairs = [
    (
        "machine learning",
        "predictive modeling"
    ),

    (
        "computer vision",
        "image recognition"
    ),

    (
        "SQL",
        "relational database querying"
    ),

    (
        "deep learning",
        "neural network training"
    )
]
```

Calculate the similarity for each pair.

Then compare with unrelated pairs:

```python
unrelated_pairs = [
    (
        "computer vision",
        "accounting"
    ),

    (
        "Python programming",
        "graphic design"
    )
]
```

The goal is to observe the geometry of the embedding space.

---

# 21. Do Not Assume Every High Score Is Correct

Suppose the model gives:

```text
Computer Vision
0.82
```

Does that prove the person knows computer vision?

No.

It means:

> According to this representation, the two pieces of text are highly similar.

That is different from:

```text
The person definitely has this skill.
```

This distinction becomes extremely important when we later build systems that make decisions.

---

# 22. Similarity vs. Classification

We currently have:

```text
Resume
+
Skill
 ↓
Similarity Score
```

We do not yet have:

```text
Yes / No
```

If we introduce:

```python
if score >= threshold:
    matched = True
```

we have created a simple decision rule.

So:

```text
Similarity
    ↓
Threshold
    ↓
Decision
```

The threshold is an application-level decision, not something automatically guaranteed by the embedding model.

---

# 23. Find the Threshold Experimentally

Create a labeled dataset.

For example:

```python
TEST_CASES = [
    {
        "resume": "...",
        "expected_skills": [
            "python",
            "machine learning"
        ]
    },

    {
        "resume": "...",
        "expected_skills": [
            "sql"
        ]
    }
]
```

Run the embedding matcher.

Then try:

```text
0.30
0.40
0.50
0.60
0.70
```

For each threshold:

```text
Predictions
    ↓
Precision
Recall
F1
```

Compare the results.

This is much better than arbitrarily deciding:

```text
"0.7 sounds like a good threshold."
```

---

# 24. Why Thresholds Are Domain-Specific

A score of:

```text
0.70
```

does not have the same meaning across every embedding model and every dataset.

For example:

```text
Model A:
0.70 → strong similarity

Model B:
0.70 → moderate similarity
```

Even within the same model:

```text
technical resumes
```

may produce a different score distribution from:

```text
general documents
```

Therefore:

> **Thresholds should be evaluated on the data and task where the system will actually be used.**

---

# 25. Batch Embeddings

Our previous implementation encodes everything at once.

That is usually better than repeatedly encoding one item at a time.

For example:

```python
skill_embeddings = model.encode(
    skill_descriptions
)
```

instead of:

```python
for description in skill_descriptions:

    model.encode(description)
```

Batching can make processing more efficient.

The general principle is:

> **When a model supports batch processing, use it for collections of inputs.**

---

# 26. Cache the Model in Streamlit

There is another practical issue.

If Streamlit reruns the script, we don't want to load the embedding model from scratch every time.

Streamlit provides caching mechanisms.

For example:

```python
@st.cache_resource
def load_embedding_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )
```

Then:

```python
model = load_embedding_model()
```

The application can reuse the loaded model.

This makes the interface much more responsive.

---

# 27. Upgrade the Streamlit UI

Our application can now show:

```text
Resume
  ↓
Extract Text
  ↓
Semantic Skill Analysis
```

For example:

```python
st.subheader(
    "Semantic Skill Matches"
)

for result in results:

    st.write(
        result["skill"],
        f"{result['score']:.3f}"
    )
```

We can also display the TF-IDF and embedding scores together.

---

# 28. Build a Comparison Table

A useful UI could look conceptually like:

```text
| Skill | Exact | TF-IDF | Embedding |
|---|---|---:|---:|
| Python | ✓ | 0.42 | 0.51 |
| SQL | ✗ | 0.00 | 0.08 |
| Computer Vision | ✗ | 0.12 | 0.71 |
| Deep Learning | ✗ | 0.18 | 0.76 |
```

This is one of the best demonstrations in this module.

Students can directly see:

```text
Exact matching
      ↓
TF-IDF
      ↓
Embeddings
```

---

# 29. Understand the Trade-Off

We have gained something.

Embeddings can capture semantic relationships better than simple lexical matching.

But we also introduced:

```text
Model
 ↓
Computation
 ↓
Memory
 ↓
Dependency
```

TF-IDF is extremely lightweight.

An embedding model is more computationally expensive.

So the engineering decision is not:

```text
Embeddings are better
therefore always use embeddings.
```

Instead:

> **Use the simplest representation that provides enough quality for the task.**

---

# 30. Interpretability

Compare:

### Rule-based

```text
Python found because
the word "Python" appeared.
```

Very interpretable.

### TF-IDF

```text
Similarity is high because
important terms overlap.
```

Still relatively interpretable.

### Embeddings

```text
Similarity is high because
the model places these texts
near each other in its learned space.
```

This is harder to explain.

So we have a trade-off:

```text
More semantic power
        ↕
Less direct interpretability
```

This is an important property of modern AI systems.

---

# 31. Embeddings Are Not the End

We now have:

```text
Resume
   ↓
Embedding
   ↓
Similarity
   ↓
Skills
```

But we still have a problem.

A resume is not just a collection of skills.

A job description contains:

```text
Required skills
Responsibilities
Experience
Education
Seniority
Location
Industry
```

We need to compare two much larger documents.

That becomes:

```text
Resume
   +
Job Description
   ↓
Matching
```

This is a more interesting application.

---

# 32. Prepare for Resume ↔ Job Matching

Suppose we have:

### Resume

```text
Python developer with experience
building machine learning models,
computer vision systems and data pipelines.
```

### Job Description

```text
Looking for a machine learning engineer
with Python experience, computer vision
knowledge and experience building data
processing systems.
```

A human would probably say:

```text
Strong match
```

Our system should eventually produce something like:

```text
Overall Match: 0.82
```

and ideally explain:

```text
Strong matches:
- Python
- Machine Learning
- Computer Vision

Potential gaps:
- Cloud deployment
- Kubernetes
```

This is where our components start becoming a genuine software product.

---

# 33. A Better Architecture

Our system is now evolving toward:

```text
                         Resume
                            │
                            ▼
                       OCR / Text
                            │
                            ▼
                    Resume Parser
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
        Structured Data              Resume Text
              │                           │
              │                           ▼
              │                      Embeddings
              │                           │
              └─────────────┬─────────────┘
                            │
                            ▼
                     Matching Engine
                            ▲
                            │
                       Job Description
                            │
                            ▼
                       Embeddings
```

We now have the beginnings of a real intelligent application architecture.

---

# 34. Project Exercise — Build the Semantic Matcher

Your task is to create:

```text
semantic_matcher.py
```

with:

```python
def calculate_embedding_skill_scores(
    resume_text,
    skill_descriptions,
    model
):
    ...
```

Then connect it to:

```text
app.py
```

Your application should allow the user to:

1. Upload a resume.
2. Extract its text.
3. Run the rule-based parser.
4. Run TF-IDF matching.
5. Run embedding matching.
6. Compare the results.
7. Adjust a similarity threshold.
8. Display the resulting skill matches.

---

# 35. Suggested Project Structure

At this point:

```text
resume-parser/
│
├── app.py
├── document_reader.py
├── resume_parser.py
├── semantic_matcher.py
├── evaluation_data.py
├── evaluate_parser.py
├── requirements.txt
└── README.md
```

The responsibilities are becoming clear:

```text
document_reader.py
        ↓
Image → Text

resume_parser.py
        ↓
Text → Structured Information

semantic_matcher.py
        ↓
Text → Semantic Similarity

app.py
        ↓
User Interface
```

---

# 36. Git Checkpoint

Once the embedding matcher works:

```bash
git status
```

Then:

```bash
git add .
```

Then:

```bash
git commit -m "Add embedding based semantic skill matching"
```

We now have another checkpoint:

```text
Rules
 ↓
TF-IDF
 ↓
Embeddings
 ↓
Git checkpoint
```

---

# 37. What We Have Learned

We started with:

```text
Exact keyword matching
```

Then:

```text
TF-IDF
```

Then:

```text
Embeddings
```

The key progression is:

```text
                  Representation

Exact Match  →   Words
TF-IDF       →   Weighted Words
Embeddings   →   Learned Semantic Representation
```

And the comparison mechanism can remain:

```text
Cosine Similarity
```

This is one of the most important conceptual lessons of the project.

---

# 38. The Evolution of the Resume Parser

Our application has now evolved through:

```text
Version 1
─────────
Regex + Rules
```

to:

```text
Version 2
─────────
Regex + Rules
+
TF-IDF + Cosine Similarity
```

to:

```text
Version 3
─────────
Regex + Rules
+
TF-IDF + Cosine Similarity
+
Embeddings + Cosine Similarity
```

We have gradually increased complexity only when the previous approach showed a limitation.

That is the engineering mindset we want.

---

# 39. What Comes Next

We are finally ready to leave the question:

```text
"What skills does this resume contain?"
```

and ask the much more useful question:

```text
"How well does this resume match this job?"
```

That becomes:

# Project 3 — Resume ↔ Job Matching

We will combine:

```text
Document Reader
       +
Resume Parser
       +
Embeddings
       +
Similarity
       +
Rules
       +
Streamlit
```

The output will move from:

```text
Skills:
Python
Computer Vision
Machine Learning
```

to something closer to:

```text
Match Score: 84%

Strong matches:
✓ Python
✓ Machine Learning
✓ Computer Vision

Potential gaps:
✗ Kubernetes
✗ AWS

Relevant experience:
✓ 3 years software development
```

The important shift is:

```text
Extraction
    ↓
Representation
    ↓
Similarity
    ↓
Decision Support
```

We are no longer simply demonstrating individual AI techniques.

We are assembling them into a useful application.
