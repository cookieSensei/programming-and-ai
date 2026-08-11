# Project 2.2 - Semantic Skill Matching with TF-IDF and Cosine Similarity

## From Exact Keywords to Similarity

Our resume parser currently uses rules.

For example:

```text
Does the resume contain "Python"?
        ↓
Yes → Python skill found
No  → Python skill not found
```

This works for exact matches.

But language is more flexible than that.

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

There is no exact:

```text
"computer vision"
```

inside the resume.

A keyword matcher may therefore miss the relationship.

We now want to move from:

```text
Exact Match
```

to:

```text
Similarity
```

Our first attempt will use something we already learned:

```text
TF-IDF
+
Cosine Similarity
```

This is **not** the final semantic solution.

In fact, this project is designed to show where this approach works and where it fails.

---

# 1. What Are We Trying to Measure?

Suppose we have a skill:

```text
Computer Vision
```

and a piece of resume text:

```text
Developed image classification systems
using convolutional neural networks.
```

We want to calculate something like:

```text
How similar are these two pieces of text?
```

Instead of:

```python
if "computer vision" in text:
    ...
```

we want:

```text
Resume Text
     ↓
Numerical Representation
     ↓
Skill Representation
     ↓
Similarity Score
```

This is the basic idea behind our new component.

---

# 2. Why Convert Text to Numbers?

Computers can compare numbers very easily.

For example:

```text
5
```

and:

```text
5.1
```

are numerically close.

But:

```text
"Python"
```

and:

```text
"machine learning"
```

are strings.

We need a representation that turns text into numbers.

One approach is:

> **TF-IDF**

---

# 3. Quick Review: TF-IDF

TF-IDF stands for:

> **Term Frequency - Inverse Document Frequency**

It creates a numerical representation of text.

Very roughly:

```text
Text
 ↓
Vocabulary
 ↓
Numerical vector
```

For example:

```text
"Python SQL machine learning"
```

might become something conceptually like:

```text
[0.4, 0.7, 0.2, 0.6, ...]
```

The actual numbers depend on the documents and vocabulary.

The important thing is:

```text
Text
 ↓
Vector
```

Now we can perform mathematical operations on the text.

---

# 4. A Small Example

Let's start with two documents:

```python
documents = [
    "Python developer with machine learning experience",
    "Machine learning engineer using Python"
]
```

Import:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
```

Create a vectorizer:

```python
vectorizer = TfidfVectorizer()
```

Fit it:

```python
vectors = vectorizer.fit_transform(
    documents
)
```

Now:

```python
print(
    vectors.shape
)
```

The result tells us:

```text
number of documents
×
number of vocabulary terms
```

The important transformation is:

```text
Documents
   ↓
TF-IDF
   ↓
Vectors
```

---

# 5. Inspect the Vocabulary

We can inspect what vocabulary the vectorizer learned:

```python
print(
    vectorizer.get_feature_names_out()
)
```

We might see:

```text
[
    "developer",
    "engineer",
    "experience",
    "learning",
    "machine",
    "python",
    "using"
]
```

Each term corresponds to a dimension in the vector space.

So the text has become a point in a high-dimensional space.

---

# 6. Why a Vector Space?

Imagine a much simpler world where we only have two words:

```text
Python
SQL
```

A document might be represented as:

```text
Python = 0.8
SQL    = 0.2
```

So:

```text
Document
   ↓
(0.8, 0.2)
```

Another document:

```text
Python = 0.7
SQL    = 0.3
```

becomes:

```text
(0.7, 0.3)
```

These points are relatively close.

This gives us a geometric interpretation of text.

---

# 7. Cosine Similarity

Now we can compare vectors.

The technique we already used in our chatbot project is:

> **Cosine similarity**

The idea is to compare the angle between two vectors.

Conceptually:

```text
Vector A
    ↗
   /
  /
 ●────────→
      Vector B
```

If the vectors point in similar directions:

```text
High similarity
```

If they point in very different directions:

```text
Low similarity
```

The value is commonly between:

```text
-1 and 1
```

For many TF-IDF text applications, we commonly encounter values between:

```text
0 and 1
```

because TF-IDF vectors are non-negative.

---

# 8. Calculate Cosine Similarity

Import:

```python
from sklearn.metrics.pairwise import cosine_similarity
```

Suppose:

```python
documents = [
    "Python developer with machine learning experience",
    "Machine learning engineer using Python"
]
```

Then:

```python
vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform(
    documents
)

similarity = cosine_similarity(
    vectors[0],
    vectors[1]
)

print(similarity)
```

We get a matrix containing the similarity score.

---

# 9. Build a Skill Matcher

Now let's adapt this idea to our resume parser.

Suppose we have:

```python
skills = [
    "python",
    "sql",
    "machine learning",
    "computer vision",
    "deep learning",
    "data analysis"
]
```

And resume text:

```python
resume_text = """
Developed image classification systems
using convolutional neural networks.
Worked with Python and predictive models.
"""
```

We want to ask:

```text
Which skills are related to this resume?
```

---

# 10. Create Candidate Documents

We can treat each skill as a tiny document.

```python
skill_documents = [
    "python",
    "sql",
    "machine learning",
    "computer vision",
    "deep learning",
    "data analysis"
]
```

Then:

```python
documents = [
    resume_text
] + skill_documents
```

Now the first document is:

```text
Resume
```

and the remaining documents are:

```text
Skill descriptions
```

---

# 11. Vectorize Everything Together

This is important.

We want the resume and skill descriptions to live in the **same vector space**.

```python
vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform(
    documents
)
```

Now:

```text
vectors[0]
```

represents the resume.

And:

```text
vectors[1:]
```

represent the candidate skills.

---

# 12. Compare Resume With Every Skill

We can calculate:

```python
scores = cosine_similarity(
    vectors[0],
    vectors[1:]
)
```

The result gives us one similarity score for each skill.

Conceptually:

```text
Resume
   │
   ├── Python          → 0.42
   ├── SQL             → 0.00
   ├── Machine Learning → 0.18
   ├── Computer Vision → 0.00
   ├── Deep Learning   → 0.15
   └── Data Analysis   → 0.04
```

These numbers are illustrative.

The actual scores depend on the input text and vectorizer configuration.

---

# 13. The First Surprise

You might expect:

```text
"convolutional neural networks"
```

to be strongly similar to:

```text
"computer vision"
```

But TF-IDF may give us:

```text
very low similarity
```

Why?

Because TF-IDF is based heavily on **shared vocabulary**.

The two texts may not contain the same words.

We have:

```text
Resume:
convolutional
neural
networks
image
classification
```

versus:

```text
Skill:
computer
vision
```

There is little or no word overlap.

So:

```text
Semantic relationship
```

does not automatically mean:

```text
TF-IDF similarity
```

This is a critical lesson.

---

# 14. TF-IDF Is Not Semantic Understanding

We should be precise about what our system is doing.

TF-IDF gives us:

```text
Lexical representation
```

and cosine similarity measures:

```text
Similarity between those lexical representations
```

It does not inherently understand that:

```text
CNN
```

is related to:

```text
Computer Vision
```

or that:

```text
PostgreSQL
```

is related to:

```text
SQL
```

or that:

```text
predictive modeling
```

is related to:

```text
machine learning
```

This distinction matters.

---

# 15. Improve the Skill Descriptions

We can make our candidate descriptions richer.

Instead of:

```python
skills = [
    "computer vision"
]
```

we could use:

```python
skills = [
    """
    computer vision image processing
    image classification object detection
    convolutional neural networks
    """,

    """
    machine learning predictive modeling
    classification regression supervised learning
    """,

    """
    deep learning neural networks
    CNN transformers representation learning
    """
]
```

Now the vocabulary overlaps more with resume text.

This can improve TF-IDF matching.

But notice what happened.

We had to manually provide related terms.

That means our system still doesn't truly understand the meaning.

---

# 16. This Is Feature Engineering

Adding related terms is a form of feature engineering.

We are telling the system:

```text
These words are useful signals
for this concept.
```

For example:

```text
Computer Vision
    ↓
image
classification
object detection
CNN
image processing
```

This can make our similarity system more useful.

But it also creates maintenance work.

What if we forget:

```text
OCR
```

or:

```text
segmentation
```

or:

```text
image recognition
```

The system may still miss relevant resumes.

---

# 17. Create a Skill Knowledge Base

We can represent skills as a dictionary:

```python
SKILL_DESCRIPTIONS = {

    "python": """
    Python programming language
    scripting software development
    """

    ,

    "machine learning": """
    machine learning predictive modeling
    classification regression supervised learning
    """

    ,

    "computer vision": """
    computer vision image processing
    image classification object detection
    convolutional neural networks CNN
    """

    ,

    "deep learning": """
    deep learning neural networks
    CNN transformers representation learning
    """

    ,

    "sql": """
    SQL databases relational databases
    querying data
    """
}
```

Now our matcher has more context than a single keyword.

---

# 18. Build the Matcher Function

```python
def calculate_skill_scores(
    resume_text,
    skill_descriptions
):

    skills = list(
        skill_descriptions.keys()
    )

    documents = [
        resume_text
    ] + list(
        skill_descriptions.values()
    )

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        documents
    )

    scores = cosine_similarity(
        vectors[0],
        vectors[1:]
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

Now:

```python
results = calculate_skill_scores(
    resume_text,
    SKILL_DESCRIPTIONS
)
```

might produce:

```python
[
    {
        "skill": "computer vision",
        "score": 0.32
    },
    {
        "skill": "deep learning",
        "score": 0.24
    },
    {
        "skill": "machine learning",
        "score": 0.18
    }
]
```

Again, these values are illustrative.

---

# 19. Add a Threshold

We don't necessarily want to classify every skill as:

```text
Present
```

just because it has a non-zero score.

We can introduce a threshold:

```python
THRESHOLD = 0.15
```

Then:

```python
matched_skills = [
    result
    for result in results
    if result["score"] >= THRESHOLD
]
```

Now:

```text
score >= threshold
    ↓
Potential match

score < threshold
    ↓
Probably not a match
```

---

# 20. A Threshold Is a Model Decision

The threshold:

```python
0.15
```

is not a universal truth.

A threshold of:

```text
0.05
```

may produce many false positives.

A threshold of:

```text
0.40
```

may produce many false negatives.

So we should not simply pick a number because it "looks good."

We need to evaluate it.

This is exactly the same principle we learned in machine learning.

---

# 21. Evaluate Semantic Skill Matching

Create test cases.

For example:

```python
TEST_CASES = [

    {
        "resume": """
        Developed convolutional neural networks
        for image classification.
        """,

        "expected": [
            "computer vision",
            "deep learning"
        ]
    },

    {
        "resume": """
        Built predictive models for customer
        churn using regression and classification.
        """,

        "expected": [
            "machine learning"
        ]
    }
]
```

Run the matcher.

Then compare:

```text
Expected skills
vs.
Predicted skills
```

---

# 22. Precision and Recall Return

We have already learned:

```text
Precision
Recall
F1
```

They are useful here too.

Suppose:

```text
Expected:
Computer Vision
Deep Learning

Predicted:
Computer Vision
Deep Learning
Machine Learning
```

Then:

```text
Correct = 2
Predicted = 3
Expected = 2
```

So:

```text
Precision = 2 / 3

Recall = 2 / 2
```

The system found everything expected, but it also added an extra skill.

This gives us a measurable way to tune our threshold.

---

# 23. Experiment With the Threshold

Try:

```python
thresholds = [
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30
]
```

For each threshold:

```text
Run matcher
 ↓
Calculate predictions
 ↓
Calculate precision
 ↓
Calculate recall
 ↓
Calculate F1
```

Then compare.

You may discover:

```text
Low threshold
    ↓
High recall
Low precision
```

and:

```text
High threshold
    ↓
Low recall
High precision
```

This is a practical demonstration of the precision-recall trade-off.

---

# 24. Visualize the Scores

Streamlit makes it easy to display the results.

For example:

```python
for result in results:

    st.write(
        result["skill"],
        result["score"]
    )
```

We can make the result more readable:

```python
st.metric(
    result["skill"],
    f"{result['score']:.2f}"
)
```

Or display a table.

The user might see:

```text
Skill              Score

Computer Vision    0.32
Deep Learning      0.24
Machine Learning   0.18
SQL                0.00
```

Now our parser is no longer simply saying:

```text
found / not found
```

It is producing a confidence-like ranking score.

Be careful with the terminology:

> **A cosine similarity score is not automatically a probability or model confidence.**

It is a similarity measurement.

---

# 25. Add This to the Resume Parser

Our structured resume can now contain:

```python
{
    "name": "John Smith",

    "email": "john@example.com",

    "skills": [
        "Python",
        "SQL"
    ],

    "semantic_skills": [
        {
            "skill": "Computer Vision",
            "score": 0.32
        },
        {
            "skill": "Deep Learning",
            "score": 0.24
        }
    ]
}
```

Notice that we don't have to throw away our original rule-based skills.

We can keep both:

```text
Exact skills
+
Similarity-based candidates
```

This is often a better architecture.

---

# 26. Combine Rules and Similarity

Our pipeline becomes:

```text
Resume
   ↓
OCR
   ↓
Text
   │
   ├───────────────┐
   ▼               ▼
Regex / Rules    TF-IDF
   │               │
   ▼               ▼
Exact Skills    Similar Skills
   │               │
   └───────┬───────┘
           ▼
       Final Profile
```

This is a hybrid system.

It uses the simplest technique where possible and a more flexible technique where useful.

---

# 27. Why Cosine Similarity Still Isn't Enough

At this point, our system is better.

But it still has serious limitations.

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

Even after adding some descriptions, we are manually creating relationships.

Now consider:

```text
"developed models for detecting objects"
```

versus:

```text
"computer vision"
```

The relationship may still be difficult for TF-IDF to capture.

The fundamental issue is:

> **TF-IDF represents words, not concepts.**

---

# 28. Synonyms Are Difficult

Consider:

```text
automobile
```

and:

```text
car
```

A human understands that they are closely related.

TF-IDF sees:

```text
automobile
```

and:

```text
car
```

as different terms.

Unless both documents happen to contain the same words, their lexical similarity may be low.

Likewise:

```text
ML
```

and:

```text
machine learning
```

may be treated as unrelated unless we explicitly teach the system the relationship.

---

# 29. Word Order Is Also Limited

Consider:

```text
Python developer with SQL experience
```

and:

```text
SQL experience with Python developer
```

TF-IDF mostly cares about term weights.

It doesn't deeply understand the sentence structure.

Even more importantly:

```text
Python developer
```

and:

```text
Developer using Python
```

can be semantically similar while being textually different.

---

# 30. TF-IDF Has Been Useful Anyway

Don't conclude:

> "TF-IDF is useless."

It isn't.

TF-IDF is useful for many tasks:

```text
Document retrieval
Keyword search
Text classification
Ranking
Similarity
```

It is:

- simple
- fast
- interpretable
- easy to implement
- often surprisingly effective

Our goal is not to replace it because it is "old."

Our goal is to understand its representation.

> **The quality of a similarity method depends heavily on how the data is represented.**

---

# 31. Representation Is the Real Lesson

Our pipeline is currently:

```text
Text
 ↓
TF-IDF
 ↓
Vector
 ↓
Cosine Similarity
```

The cosine similarity calculation itself is not necessarily the problem.

The question is:

> **What do the vectors represent?**

If the vector represents:

```text
word frequency
```

then similarity is largely based on:

```text
word overlap
```

If the vector represents:

```text
semantic meaning
```

then similarity can potentially capture relationships between different words.

This leads us naturally to embeddings.

---

# 32. From TF-IDF to Embeddings

We can now extend our progression:

```text
Text
 ↓
TF-IDF
 ↓
Lexical Vector
 ↓
Cosine Similarity
```

Then:

```text
Text
 ↓
Embedding Model
 ↓
Semantic Vector
 ↓
Cosine Similarity
```

Notice something important.

We may still use:

```text
cosine_similarity()
```

The major change is the **representation**.

The vector has become more semantic.

---

# 33. A Key Concept

Students often hear:

> "Cosine similarity is dumb."

That's not quite the right lesson.

Cosine similarity is simply a mathematical way of comparing vectors.

It does not know what those vectors mean.

If we give it:

```text
TF-IDF vectors
```

we get:

```text
TF-IDF-based similarity
```

If we give it:

```text
embedding vectors
```

we get:

```text
embedding-based similarity
```

So:

```text
Cosine Similarity
```

is the comparison mechanism.

```text
TF-IDF / Embeddings
```

determine what the vectors represent.

This distinction is extremely important.

---

# 34. Experiment - Compare Two Representations

Create a small experiment.

Compare:

```text
"computer vision"
```

with:

```text
"image classification using convolutional neural networks"
```

First use:

```text
TF-IDF
```

Then eventually use:

```text
Embeddings
```

Record the scores.

The goal isn't to memorize the numbers.

The goal is to observe:

```text
Same similarity function
Different representation
Different behavior
```

---

# 35. Challenge - Build a Skill Ranking UI

Upgrade the Streamlit application.

Show:

```text
Semantic Skill Matches
```

Sort by score:

```text
Computer Vision     0.32
Deep Learning       0.24
Machine Learning    0.18
Data Analysis       0.04
SQL                 0.00
```

Then allow the user to change:

```text
Similarity Threshold
```

For example:

```python
threshold = st.slider(
    "Similarity threshold",
    0.0,
    1.0,
    0.15
)
```

Then:

```python
matches = [
    result
    for result in results
    if result["score"] >= threshold
]
```

Now the user can directly observe the effect of the threshold.

---

# 36. Challenge - Build a Comparison Table

Display:

```text
| Skill | Exact Match | TF-IDF Score | Final |
|---|---|---:|---|
| Python | Yes | 0.42 | Yes |
| SQL | No | 0.00 | No |
| Computer Vision | No | 0.32 | Yes |
| Deep Learning | No | 0.24 | Yes |
```

This is a useful demonstration because students can see the difference between:

```text
Literal matching
```

and:

```text
Similarity-based matching
```

---

# 37. What We Have Built

Our resume system has now evolved considerably.

### Version 1

```text
Regex
 ↓
Rules
 ↓
Exact Information
```

### Version 2

```text
Regex
+
Rules
+
TF-IDF
+
Cosine Similarity
 ↓
Exact + Similar Information
```

The architecture is becoming:

```text
                 Resume
                    │
                    ▼
                OCR / Text
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
      Rule-Based          Similarity
       Extraction          Matching
          │                   │
          └─────────┬─────────┘
                    ▼
             Resume Profile
```

---

# 38. The Limitation We Want

Our system should now fail in interesting ways.

For example:

```text
Resume:

Built object detection systems
using convolutional neural networks.

Skill:

Computer Vision
```

TF-IDF may still struggle.

That is not a failure of the tutorial.

It is the next lesson.

We have now demonstrated:

```text
TF-IDF improves upon exact matching
```

but:

```text
TF-IDF still relies heavily on lexical overlap
```

So we need a better representation.

---

# 39. What Comes Next

We are now ready to introduce:

# Project 2.3 - Embeddings for Semantic Matching

We will take the exact same architecture:

```text
Resume Text
     +
Skill Description
     ↓
Vector Representation
     ↓
Cosine Similarity
     ↓
Similarity Score
```

but replace:

```text
TF-IDF
```

with:

```text
Embedding
```

Then we can compare:

```text
TF-IDF similarity
```

against:

```text
Embedding similarity
```

This will let us see the evolution clearly:

```text
Exact Keyword
      ↓
TF-IDF
      ↓
Embeddings
      ↓
Semantic Matching
```

And once we can represent resumes and job descriptions semantically, we are ready for:

# Project 3 - Resume ↔ Job Matching

where the system will move from:

```text
"What skills are in this resume?"
```

to:

```text
"How well does this resume match this job?"
```

That is where our parser becomes an actual decision-support application.
