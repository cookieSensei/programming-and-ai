# Project 3 — Resume ↔ Job Matching

This project combines the earlier Document Reader, Resume Parser,
TF-IDF matcher, and embedding matcher into a decision-support application.

The intended progression is:

```text
Resume
  ↓
Document Reader
  ↓
Text
  ↓
Resume Parser
  ↓
Structured Resume + Resume Text
  ↓
Matching Engine
  ├── Exact Match
  ├── TF-IDF Similarity
  ├── Embedding Similarity
  └── Document Similarity
  ↓
Scoring Engine
  ↓
Match Report
  ↓
Streamlit UI
```

## Folder structure

All helper modules live in the same folder as `app.py`.

```text
resume-job-matcher/
├── app.py
├── document_reader.py
├── resume_parser.py
├── semantic_matcher.py
├── tfidf_matcher.py
├── job_matcher.py
├── evaluation_data.py
├── evaluate_parser.py
├── requirements.txt
└── README.md
```

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

If your Cloud Lab already has these packages installed, you can simply run:

```bash
streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.enableXsrfProtection false \
  --server.enableCORS false
```

## Important note about Project 2 integration

The included `resume_parser.py` is a self-contained version so this project can
run independently. If your Project 2 folder already contains your students'
working `resume_parser.py`, replace this file with that version.

Likewise, if Project 1 already provides `document_reader.py`, replace the
included simple text/PDF reader with the Project 1 implementation.

The matching engine should not need to know how OCR or parsing works.

## What the UI demonstrates

1. Upload or paste a resume.
2. Provide a job description.
3. Extract resume skills with rules.
4. Extract job requirements with a known skill vocabulary.
5. Compare exact skills.
6. Compare resume text with job skills using TF-IDF.
7. Compare resume text with job skills using embeddings.
8. Adjust the embedding similarity threshold.
9. Display exact matches, semantic matches, gaps, and comparison scores.
10. Produce an inspectable composite match score.

The curriculum specifies a composite demonstration score of:

```text
60% Skill Coverage
25% Semantic Coverage
15% Document Similarity
```

The displayed score should be treated as a design artifact and decision-support
signal, not as an objective measure of candidate quality.

## Model

The embedding implementation uses:

```text
sentence-transformers
all-MiniLM-L6-v2
```

The model is cached with Streamlit's `st.cache_resource`.

## Safety / framing

This is resume-to-job matching and decision support.

It should not claim:

```text
Hire this person.
Reject this candidate.
```

A resume is only one source of information, and the score can inherit bias from
the vocabulary, job descriptions, embedding model, and scoring rules.
