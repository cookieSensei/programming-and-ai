# Project 4.8 — Build a Second Intelligent Application

## Transfer What You Learned

Our first major Phase 4 application was a:

```text
Resume ↔ Job Matcher
```

It taught us how to combine:

```text
Document Processing
+
OCR
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
```

But there is an important danger in project-based learning.

A student may become very good at building:

```text
the project they were shown
```

without becoming good at:

```text
transferring the ideas to a new problem
```

So our next challenge is intentionally different.

We will build:

# An Intelligent Document Search Application

The underlying techniques are familiar.

The problem is new.

---

# 1. The Problem

Imagine a user has:

```text
10
50
100
```

documents.

They want to ask:

```text
"Where does this document talk about train/test split?"
```

or:

```text
"Find information about Streamlit deployment."
```

or:

```text
"Which document explains cosine similarity?"
```

Opening every document manually is inconvenient.

We want an application that can:

```text
Read documents
      ↓
Understand their text
      ↓
Represent their content
      ↓
Search for relevant information
      ↓
Return the best passages
```

---

# 2. The Important Difference

Our resume matcher asked:

```text
How well does this resume match this job?
```

Our new application asks:

```text
Which pieces of these documents are relevant
to this query?
```

This is a different task.

The same underlying technologies can still be useful.

That is the lesson.

---

# 3. The Core Pipeline

Start with:

```text
Documents
   ↓
Text Extraction
   ↓
Text Cleaning
   ↓
Chunking
   ↓
Embeddings
   ↓
Similarity Search
   ↓
Top Results
   ↓
Streamlit UI
```

This is our first architecture.

---

# 4. Why Chunking?

Suppose a document contains:

```text
10,000 words
```

We could create:

```text
one embedding
```

for the entire document.

But then:

```text
Query
   ↓
Document embedding
```

only tells us:

> How similar is the query to the entire document?

It does not tell us:

> Which section contains the relevant information?

Instead, divide the document into smaller pieces.

```text
Document
   ↓
Chunk 1
Chunk 2
Chunk 3
Chunk 4
...
```

Then embed each chunk.

---

# 5. Example

Suppose a document contains:

```text
Python Basics

Variables are used to store values...

Jupyter notebooks allow users to execute
Python code interactively...

Git is used to track changes...

Train/test split separates data for training
and evaluation...
```

A query:

```text
Why do we use train/test split?
```

should ideally retrieve:

```text
Train/test split separates data for training
and evaluation...
```

rather than:

```text
Git is used to track changes...
```

This is the core retrieval problem.

---

# 6. First Baseline: Keyword Search

Before embeddings, create a simple baseline.

For example:

```text
Query:
train test split
```

Search for documents containing:

```text
train
test
split
```

This is intentionally simple.

The baseline gives us something to compare against.

---

# 7. Second Baseline: TF-IDF

Use the technique learned earlier.

Represent:

```text
Document chunks
```

with:

```text
TF-IDF vectors
```

Then:

```text
Query
 ↓
TF-IDF
 ↓
Cosine Similarity
 ↓
Rank chunks
```

This should already produce a useful retrieval system.

---

# 8. Third Version: Embeddings

Now replace:

```text
TF-IDF
```

with:

```text
Sentence Embeddings
```

The pipeline becomes:

```text
Chunk
 ↓
Embedding
 ↓
Vector
```

and:

```text
Query
 ↓
Embedding
 ↓
Vector
```

Then:

```text
Cosine Similarity
```

compares the vectors.

---

# 9. Why Embeddings Help

Keyword search may struggle with:

```text
"evaluate a model on unseen data"
```

when the document says:

```text
"train/test split"
```

The words are different.

Semantic representations can potentially recognize that the concepts are related.

That is the reason we introduce embeddings.

---

# 10. Keep the Baselines

Do not delete the earlier versions.

Keep:

```text
Version 1:
Keyword

Version 2:
TF-IDF

Version 3:
Embeddings
```

Then compare them.

This turns the project into an experiment rather than simply:

```text
Use embeddings because embeddings are better.
```

---

# 11. Document Ingestion

The application should accept documents.

For the first version, support:

```text
TXT
PDF
```

Optionally:

```text
DOCX
```

later.

The document reader should produce:

```python
{
    "filename": "...",
    "text": "..."
}
```

Keep document loading separate from retrieval.

---

# 12. OCR

Some PDFs may contain images rather than selectable text.

The application can use the document-processing knowledge from the earlier project:

```text
PDF
 ↓
Text extraction
```

and if necessary:

```text
Image
 ↓
OCR
 ↓
Text
```

The retrieval system should receive:

```text
text
```

regardless of how that text was obtained.

---

# 13. Clean the Text

Use the techniques already learned.

For example:

```python
import re

text = re.sub(
    r"\s+",
    " ",
    text
)
```

You can also remove unwanted characters where appropriate.

But be careful.

Over-cleaning text can destroy useful information.

---

# 14. Chunking Strategy

Start with a simple chunker.

For example:

```python
def chunk_text(
    text,
    chunk_size=500
):
    ...
```

A simple character-based approach is enough initially.

Later we can improve it using:

```text
Sentence boundaries
Paragraph boundaries
Overlap
Token counts
Headings
```

---

# 15. Why Overlap?

Suppose:

```text
Chunk 1:
...train/test split is useful because...

Chunk 2:
...it prevents information leakage...
```

If the boundary cuts between related sentences, important context may be separated.

Overlap can help:

```text
Chunk 1
   ↓
shared context
   ↓
Chunk 2
```

For example:

```text
Chunk size:
500 characters

Overlap:
100 characters
```

The exact values should be experimented with.

---

# 16. Chunk Metadata

Do not store only:

```text
chunk_text
```

Store metadata too.

For example:

```python
{
    "document": "ml_notes.pdf",
    "chunk_id": 12,
    "text": "...",
    "page": 4
}
```

Metadata lets the UI tell the user where the result came from.

---

# 17. Retrieval Result

A retrieval result might look like:

```python
{
    "document": "ml_notes.pdf",
    "page": 4,
    "chunk_id": 12,
    "score": 0.81,
    "text": "..."
}
```

This is much more useful than returning:

```text
0.81
```

alone.

---

# 18. Top-K Retrieval

Usually we don't return every chunk.

We return the:

```text
Top K
```

results.

For example:

```text
K = 5
```

Then:

```text
Query
 ↓
All chunks
 ↓
Similarity scores
 ↓
Sort descending
 ↓
Top 5
```

This is the basic retrieval algorithm.

---

# 19. Ranking

Suppose:

```text
Chunk A: 0.91
Chunk B: 0.83
Chunk C: 0.78
Chunk D: 0.52
Chunk E: 0.41
```

The application returns:

```text
A
B
C
```

if:

```text
K = 3
```

The ranking is part of the application.

---

# 20. Similarity Threshold

Top-K alone may return poor results.

Suppose:

```text
Top result:
0.21
```

That may not be meaningfully relevant.

We can introduce:

```text
Minimum similarity threshold
```

For example:

```python
if score >= 0.50:
    return result
```

Again:

> The threshold should be evaluated rather than chosen arbitrarily.

---

# 21. Query Flow

The complete query process becomes:

```text
User Query
    ↓
Clean Query
    ↓
Generate Query Embedding
    ↓
Compare With Chunk Embeddings
    ↓
Calculate Similarity
    ↓
Filter Threshold
    ↓
Rank
    ↓
Top-K
    ↓
Display
```

This is a small but complete information retrieval system.

---

# 22. Streamlit Interface

The UI could contain:

```text
Upload Documents

[ file uploader ]

Ask a Question

[ text input ]

[ Search ]
```

Then:

```text
Results
```

Each result could show:

```text
Document: ml_notes.pdf
Page: 4
Similarity: 0.81

Relevant passage:
...
```

---

# 23. Add Document Management

A useful second version can show:

```text
Documents loaded:

✓ python.md
✓ ml.md
✓ nlp.md
✓ deployment.md
```

The user should know what is currently searchable.

---

# 24. Don't Recompute Everything

Suppose the user uploads:

```text
100 documents
```

and asks:

```text
Question 1
```

then:

```text
Question 2
```

We should not regenerate every document embedding for every query.

Instead:

```text
Documents
 ↓
Chunks
 ↓
Embeddings
 ↓
Cache / Store
```

Then each query only requires:

```text
Query embedding
 ↓
Compare
```

This is a major performance improvement.

---

# 25. Embedding Cache

Conceptually:

```text
Document chunk
      ↓
Embedding
      ↓
Store
```

Then:

```text
Same chunk
      ↓
Reuse embedding
```

This connects directly to our earlier observability and deployment lessons.

---

# 26. Scaling the Retriever

For a small project:

```python
cosine_similarity(
    query_embedding,
    chunk_embeddings
)
```

is perfectly reasonable.

But suppose we have:

```text
1 million chunks
```

Comparing against every chunk becomes expensive.

This introduces:

```text
Vector databases
Approximate nearest neighbor search
FAISS
Indexes
```

We do not need these for the first version.

The important lesson is:

> Architecture changes when data size changes.

---

# 27. Evaluation Dataset

Create queries with known relevant passages.

For example:

```text
Query:
What is train/test split?

Expected:
ml_notes.pdf chunk 18
```

Another:

```text
Query:
How does Git track changes?

Expected:
developer_workflow.md chunk 7
```

Now retrieval can be measured.

---

# 28. Retrieval Metrics

Use:

```text
Precision@K
Recall@K
```

For example:

```text
Precision@5
```

asks:

> Of the five results returned, how many were relevant?

And:

```text
Recall@5
```

asks:

> Of the relevant results available, how many did we retrieve in the top five?

---

# 29. Mean Reciprocal Rank

Another useful retrieval metric is:

```text
MRR
```

It rewards systems that place the first relevant result near the top.

For example:

```text
Relevant result at position 1
```

is better than:

```text
Relevant result at position 5
```

for many search experiences.

---

# 30. Compare Retrieval Methods

Create an evaluation table:

```text
| Method | Precision@5 | Recall@5 | MRR |
|---|---:|---:|---:|
| Keyword | ... | ... | ... |
| TF-IDF | ... | ... | ... |
| Embeddings | ... | ... | ... |
```

Now students can answer:

> Did semantic search actually improve retrieval?

with evidence.

---

# 31. Error Analysis

Inspect failed queries.

Possible errors:

```text
Wrong chunk
Correct document, wrong section
Relevant result ranked too low
Query ambiguity
Poor OCR
Bad chunk boundary
```

Again, classify the failure before changing the system.

---

# 32. Chunking Errors

Suppose the correct answer is split across:

```text
Chunk 10
Chunk 11
```

but neither chunk contains enough context to look relevant.

The problem may not be:

```text
Embedding model
```

It may be:

```text
Chunking strategy
```

This demonstrates why the entire pipeline must be evaluated.

---

# 33. Metadata Errors

Suppose retrieval finds the right passage but displays:

```text
Page 7
```

when it actually came from:

```text
Page 8
```

The retrieval may be correct.

The metadata layer is wrong.

Again:

```text
Final output
```

depends on multiple components.

---

# 34. Add Source Citations

Every search result should ideally show:

```text
Source
```

For example:

```text
ml_notes.pdf — Page 4
```

This makes retrieval more trustworthy.

The user can inspect the source rather than blindly accepting the returned passage.

---

# 35. Search Is Not Generation

Our application retrieves:

```text
Existing text
```

It does not need an LLM to generate an answer.

The flow is:

```text
Question
 ↓
Find relevant passages
 ↓
Show passages
```

This is an important distinction.

We are building:

> **Retrieval**

not:

> **Generative question answering**

---

# 36. Why This Is a Good Second Project

It reuses previous knowledge:

```text
Python
Regex
Beautiful Soup
OCR
NLP
Cosine Similarity
Embeddings
Streamlit
Testing
Evaluation
Deployment
```

but combines them differently.

The student must understand:

```text
What changed?
```

rather than merely copying the old architecture.

---

# 37. Optional Web Crawler

The application can optionally support:

```text
Website URL
```

instead of only uploaded files.

Then:

```text
URL
 ↓
Crawler
 ↓
HTML
 ↓
Beautiful Soup
 ↓
Clean text
 ↓
Chunks
 ↓
Embeddings
 ↓
Search
```

This connects directly to the web crawler work from earlier phases.

---

# 38. Crawl Carefully

If adding crawling, students should:

```text
Stay within the target domain
Avoid duplicate URLs
Respect crawl limits
Handle broken links
Avoid infinite loops
```

The crawler should maintain:

```python
visited = set()
```

This prevents processing the same page repeatedly.

---

# 39. Relative Links

The crawler should understand:

```text
/about
/curriculum
/projects
```

as links relative to:

```text
https://example.com
```

Use appropriate URL resolution rather than manually concatenating strings.

This connects to the earlier website crawler project.

---

# 40. Crawl → Search Architecture

The full system could become:

```text
Website
   ↓
Crawler
   ↓
Pages
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embeddings
   ↓
Search Index
   ↓
User Query
   ↓
Relevant Pages
```

Now we have built a miniature semantic website search engine.

---

# 41. Streamlit Application

The UI might have two modes:

```text
Document Search
```

and:

```text
Website Search
```

But students should implement the simpler version first.

Start with:

```text
Uploaded documents
```

Then add crawling as an extension.

---

# 42. Security Considerations for URLs

If users can enter arbitrary URLs, the application should not blindly fetch everything.

At minimum consider:

```text
Allowed domains
Request limits
Timeouts
Maximum page size
Number of pages
```

This connects deployment security to application design.

---

# 43. Final Architecture

A mature version could look like:

```text
                    USER
                      │
                      ▼
                STREAMLIT UI
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     DOCUMENTS                  WEBSITE
          │                       │
          │                  CRAWLER
          │                       │
          └───────────┬───────────┘
                      ▼
                 TEXT EXTRACTION
                      │
                      ▼
                    CLEAN
                      │
                      ▼
                   CHUNKING
                      │
                      ▼
                 EMBEDDINGS
                      │
                      ▼
                 SEARCH INDEX
                      │
                      ▼
                   QUERY
                      │
                      ▼
              QUERY EMBEDDING
                      │
                      ▼
              SIMILARITY SEARCH
                      │
                      ▼
                 RANK RESULTS
                      │
                      ▼
                 TOP-K RESULTS
                      │
                      ▼
                   SOURCES
                      │
                      ▼
                     USER
```

---

# 44. Version Roadmap

Build the project progressively.

### Version 0.1

```text
TXT files
+
keyword search
```

### Version 0.2

```text
PDF extraction
+
TF-IDF
```

### Version 0.3

```text
Chunking
+
cosine similarity
```

### Version 0.4

```text
Embeddings
+
semantic search
```

### Version 0.5

```text
Streamlit UI
```

### Version 0.6

```text
Evaluation
+
metrics
```

### Version 0.7

```text
Caching
+
performance improvements
```

### Version 0.8

```text
Web crawler
```

### Version 1.0

```text
Tested
Evaluated
Deployed
Documented
```

---

# 45. Student Challenge

Build the application without copying the resume matcher architecture directly.

Start with:

```text
TXT
```

and:

```text
Keyword Search
```

Then improve it.

Every improvement should answer:

```text
What problem does this solve?
```

and:

```text
How do we know it helped?
```

---

# 46. Required Deliverables

Submit:

```text
Git repository
+
Streamlit application
+
Evaluation dataset
+
Automated tests
+
README
+
Architecture diagram
+
Experiment log
```

The README should include:

```text
Problem
Architecture
Methods
Evaluation
Limitations
Deployment
```

---

# 47. Final Comparison

Students should compare:

```text
Resume Matcher
```

and:

```text
Document Search
```

Ask:

```text
What components are reusable?

What components changed?

Where is the AI?

Where is deterministic logic?

How is evaluation different?

How is the UI different?

How does the data flow differ?
```

This exercise teaches abstraction.

---

# 48. The Reusable Components

Students may discover that some code naturally becomes reusable:

```text
Document Reader
Text Cleaner
Embedding Model Loader
Similarity Function
Streamlit Utilities
Evaluation Utilities
```

This is the beginning of building a small internal library.

---

# 49. From Project Code to Components

The first project may have:

```text
resume_parser.py
```

The second project might reveal that:

```text
document_reader.py
```

is useful elsewhere.

Then the architecture becomes:

```text
Reusable Components
       ↓
Application-Specific Logic
```

This is an important software engineering transition.

---

# 50. Don't Over-Abstract

However, don't immediately create:

```text
framework/
core/
base/
abstract/
factory/
manager/
```

for a tiny project.

Abstraction should emerge from repeated needs.

A good rule:

> **Reuse what you have evidence should be reused.**

---

# 51. Final Engineering Lesson

The second application demonstrates something important:

```text
The techniques are transferable.
```

OCR isn't:

```text
"the resume OCR technique."
```

It is:

```text
a document-processing component.
```

Embeddings aren't:

```text
"the resume matching technique."
```

They are:

```text
a representation technique.
```

Cosine similarity isn't:

```text
"a resume algorithm."
```

It is:

```text
a way to compare vectors.
```

This is how students should begin thinking about technology.

---

# 52. Final Takeaway

The first project taught:

> **How to build an intelligent application.**

The second project teaches:

> **How to transfer the architecture to a new problem.**

That distinction matters.

The ultimate goal is not for students to become experts at:

```text
Resume matching.
```

It is for them to become capable of looking at a new problem and thinking:

```text
What is the input?
What is the output?
What representation do I need?
Where does AI help?
What is the baseline?
How will I evaluate it?
How will I deploy it?
How will I know when it fails?
```

That is independent intelligent-systems engineering.
