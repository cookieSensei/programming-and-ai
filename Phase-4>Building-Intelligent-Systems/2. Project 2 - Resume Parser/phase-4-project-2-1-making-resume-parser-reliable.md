# Project 2.1 — Make the Resume Parser Reliable

## From a Working Parser to a Tested Parser

We have a first version of our resume parser.

It can extract things such as:

```text
Name
Email
Phone
URLs
Skills
Sections
```

But we have also discovered something important:

> **A parser that works on one resume is not necessarily a useful parser.**

Real resumes are inconsistent.

People use different:

- section names
- layouts
- punctuation
- date formats
- capitalization
- writing styles
- ways of listing skills

So before adding more sophisticated NLP, we are going to improve the system we already have.

The goal of this module is:

```text
Working Parser
      ↓
Test
      ↓
Find Failures
      ↓
Improve Rules
      ↓
Test Again
```

This is software engineering applied to an AI problem.

---

# 1. Don't Improve Blindly

Suppose our parser produces:

```python
{
    "name": "John Smith",
    "email": "john@example.com",
    "skills": ["python", "sql"]
}
```

We might think:

> "Looks good."

But what does "good" mean?

We need to compare the parser's output with what we actually expected.

For example:

```text
Expected:

Name:
John Smith

Email:
john@example.com

Skills:
Python
SQL
TensorFlow
```

Our parser found:

```text
Name:
John Smith

Email:
john@example.com

Skills:
Python
SQL
```

It missed:

```text
TensorFlow
```

Now we have a concrete failure.

---

# 2. Create Ground Truth

For a small project, we can manually create the expected answer.

This is called **ground truth**.

For example:

```python
expected = {
    "name": "John Smith",
    "email": "john@example.com",
    "skills": [
        "python",
        "sql",
        "tensorflow"
    ]
}
```

Then compare it with the parser output.

The important idea is:

```text
Input
  ↓
Parser
  ↓
Prediction

Input
  ↓
Human / Known Answer
  ↓
Expected Result
```

Now we can compare them.

---

# 3. Build a Small Dataset

Create:

```text
test_resumes/
```

For example:

```text
test_resumes/
│
├── resume_01.txt
├── resume_02.txt
├── resume_03.txt
└── resume_04.txt
```

We can start with text files rather than images.

Why?

Because we are testing the **resume parser**.

We don't want OCR errors to interfere with our evaluation yet.

This gives us:

```text
Text
 ↓
Resume Parser
 ↓
Evaluation
```

Later, the complete application can use:

```text
Image
 ↓
OCR
 ↓
Resume Parser
```

---

# 4. Example Resume

Create:

```text
resume_01.txt
```

with:

```text
John Smith

john@example.com
+1 555 123 4567

Python Developer

Skills
Python
SQL
TensorFlow
OpenCV

Education
BSc Computer Science

Experience
Software Developer
```

Our expected output might be:

```python
{
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "+1 555 123 4567",
    "skills": [
        "python",
        "sql",
        "tensorflow",
        "opencv"
    ]
}
```

---

# 5. Create a Different Resume

Now create:

```text
resume_02.txt
```

```text
JANE DOE

Contact Information
jane.doe@example.com
+44 20 1234 5678

Data Scientist

Technical Expertise
Python, Pandas, NumPy
Scikit-learn
Machine Learning

Academic Background
MSc Data Science

Professional Experience
Data Analyst
```

Notice how different this is.

The same information is present, but the vocabulary changed.

We have:

```text
Skills
```

versus:

```text
Technical Expertise
```

and:

```text
Education
```

versus:

```text
Academic Background
```

and:

```text
Experience
```

versus:

```text
Professional Experience
```

This is exactly the kind of variation that breaks simple rules.

---

# 6. Improve Section Aliases

Our parser already has:

```python
SECTION_ALIASES = {
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "technologies"
    ]
}
```

We can expand it:

```python
SECTION_ALIASES = {

    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "technical expertise",
        "core competencies",
        "technologies"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "professional background"
    ],

    "education": [
        "education",
        "academic background",
        "academic history"
    ],

    "projects": [
        "projects",
        "personal projects",
        "selected projects"
    ]
}
```

Now our parser handles more vocabulary.

But notice what we are doing.

We are manually teaching the program:

```text
Technical Expertise
      ≈
Skills
```

This is useful.

But it also gives us a hint about the limitations of rules.

---

# 7. Normalize Before Comparing

A common source of unnecessary failures is capitalization.

These should ideally be treated the same:

```text
Skills
SKILLS
skills
Skills:
```

Create a normalization function:

```python
def normalize_line(line):

    line = line.strip()

    line = line.lower()

    line = line.rstrip(":")

    return line
```

Now:

```python
normalize_line("Skills:")
```

produces:

```text
skills
```

and:

```python
normalize_line("SKILLS")
```

also produces:

```text
skills
```

This reduces unnecessary special cases.

---

# 8. Normalize Text Carefully

Normalization is useful, but don't destroy information that we need later.

For example:

```text
John Smith
```

can safely become:

```text
john smith
```

for comparison.

But we probably want to preserve the original:

```text
John Smith
```

for displaying to the user.

A useful pattern is:

```text
Original text
      │
      ├──→ Display
      │
      └──→ Normalized copy
               ↓
            Matching
```

Don't permanently destroy information just because it makes matching easier.

---

# 9. Improve Skill Extraction

Our original implementation might do:

```python
if skill in normalized_text:
    found_skills.append(skill)
```

This can create unexpected matches.

For example, searching for:

```text
sql
```

could potentially match characters inside another word.

We can make matching more deliberate.

One approach is to use word boundaries:

```python
pattern = rf"\b{re.escape(skill)}\b"
```

Then:

```python
if re.search(
    pattern,
    normalized_text
):
    found_skills.append(skill)
```

This tells regex that we want the skill as a word rather than an arbitrary substring.

---

# 10. Why `re.escape()`?

Suppose our skill list contains:

```text
c++
```

or:

```text
.net
```

These characters have special meanings in regex.

Instead of manually escaping every skill, we can use:

```python
re.escape(skill)
```

For example:

```python
skill = "c++"

pattern = rf"\b{re.escape(skill)}\b"
```

This makes the skill safe to insert into a regex pattern.

---

# 11. Normalize Skill Names

Our output might currently be:

```python
[
    "python",
    "tensorflow",
    "opencv"
]
```

But our UI might prefer:

```text
Python
TensorFlow
OpenCV
```

So instead of storing only strings, we can store a mapping:

```python
KNOWN_SKILLS = {
    "python": "Python",
    "sql": "SQL",
    "tensorflow": "TensorFlow",
    "opencv": "OpenCV",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-learn"
}
```

Then:

```python
for skill, display_name in KNOWN_SKILLS.items():

    pattern = rf"\b{re.escape(skill)}\b"

    if re.search(
        pattern,
        normalized_text
    ):
        found_skills.append(
            display_name
        )
```

Now we separate:

```text
Matching representation
```

from:

```text
Display representation
```

---

# 12. Handling Comma-Separated Skills

A resume might contain:

```text
Python, Pandas, NumPy, SQL
```

instead of:

```text
Python
Pandas
NumPy
SQL
```

Our keyword approach can still detect them because we search the entire text.

This is a useful observation:

> **The parser does not always need to understand the exact formatting if the information can still be reliably extracted.**

---

# 13. Improve Email Extraction

Our original email extraction is already fairly useful.

We can wrap it in a function:

```python
def extract_email(text):

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@"
        r"[A-Za-z0-9.-]+"
        r"\."
        r"[A-Za-z]{2,}"
    )

    matches = re.findall(
        pattern,
        text
    )

    if matches:
        return matches[0]

    return None
```

Notice the return behavior:

```text
Found
 ↓
email

Not found
 ↓
None
```

This is better than returning an empty list when our application expects a single email.

---

# 14. Improve Phone Extraction

Phone numbers are harder.

Instead of assuming there is always one exact format, we can first extract candidates:

```python
def extract_phone(text):

    pattern = (
        r"(?:\+?\d[\d\s().-]{7,}\d)"
    )

    matches = re.findall(
        pattern,
        text
    )

    if matches:
        return matches[0].strip()

    return None
```

Again, this is a candidate extractor.

It is not a universal international phone-number parser.

That distinction matters.

---

# 15. Improve Name Extraction

Our first implementation:

```python
return lines[0]
```

is fragile.

Let's introduce a few simple filters.

We don't want:

```text
RESUME
CURRICULUM VITAE
CV
```

to become the name.

For example:

```python
IGNORED_HEADINGS = {
    "resume",
    "curriculum vitae",
    "cv"
}
```

Then:

```python
def extract_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines:

        if line.lower() in IGNORED_HEADINGS:
            continue

        if "@" in line:
            continue

        if re.search(r"\d", line):
            continue

        return line

    return None
```

This is still a heuristic.

It is just a better heuristic.

---

# 16. The Important Lesson About Heuristics

Our name parser now says:

```text
Find the first non-empty line
that doesn't look like:
- a heading
- an email
- a phone number
```

That sounds reasonable.

But consider:

```text
Software Engineer
John Smith
john@example.com
```

Our parser may return:

```text
Software Engineer
```

The rule failed.

We could add more rules.

But every new rule introduces another assumption.

This is exactly why we need to evaluate the parser rather than assuming that a clever-looking heuristic is reliable.

---

# 17. Build an Evaluation Function

Let's create:

```python
def evaluate_field(
    predicted,
    expected
):

    return predicted == expected
```

For lists:

```python
def evaluate_list(
    predicted,
    expected
):

    predicted = set(
        item.lower()
        for item in predicted
    )

    expected = set(
        item.lower()
        for item in expected
    )

    return predicted == expected
```

Now we can compare results.

---

# 18. Exact Matching Is Not Always Enough

Suppose the expected skills are:

```python
[
    "Python",
    "SQL",
    "TensorFlow"
]
```

and the parser finds:

```python
[
    "Python",
    "SQL"
]
```

Is that:

```text
Correct?
```

No.

But perhaps it is:

```text
Partially correct.
```

We need better metrics.

---

# 19. Precision and Recall

For information extraction, precision and recall are useful.

### Precision

Of everything we extracted:

> How much was actually correct?

```text
Precision =
Correct Predictions
-------------------
All Predictions
```

### Recall

Of everything that should have been extracted:

> How much did we find?

```text
Recall =
Correct Predictions
-------------------
All Expected Items
```

Suppose:

```text
Expected skills:

Python
SQL
TensorFlow
OpenCV
```

Our parser finds:

```text
Python
SQL
Docker
```

Then:

```text
Correct = Python, SQL
```

So:

```text
Precision = 2 / 3
Recall    = 2 / 4
```

This is much more informative than simply saying:

```text
"2 skills were correct."
```

---

# 20. F1 Score

We can combine precision and recall using F1:

```text
F1 =
2 × Precision × Recall
----------------------
Precision + Recall
```

In Python, we can eventually use:

```python
from sklearn.metrics import f1_score
```

But first understand the idea.

The metric is balancing:

```text
Precision
+
Recall
```

This is particularly useful when our parser can both:

```text
miss information
```

and:

```text
extract incorrect information
```

---

# 21. Evaluation Is Becoming More Serious

We now have a progression:

```text
Parser
  ↓
Expected Output
  ↓
Compare
  ↓
Precision
Recall
F1
```

This should feel familiar.

Earlier, in machine learning, we asked:

```text
How well does the model perform?
```

Now we are asking:

```text
How well does the information extraction system perform?
```

The same engineering mindset applies.

---

# 22. Build a Parser Evaluation Dataset

Create a simple Python file:

```text
evaluation_data.py
```

For example:

```python
TEST_CASES = [

    {
        "text": """
        John Smith

        john@example.com

        Skills
        Python
        SQL
        TensorFlow
        """,

        "expected": {
            "name": "John Smith",
            "email": "john@example.com",
            "skills": [
                "Python",
                "SQL",
                "TensorFlow"
            ]
        }
    },

    {
        "text": """
        Jane Doe

        jane@example.com

        Technical Expertise
        Python
        Pandas
        NumPy
        """,

        "expected": {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "skills": [
                "Python",
                "Pandas",
                "NumPy"
            ]
        }
    }
]
```

Now we have repeatable tests.

---

# 23. Run the Evaluation

We can create:

```text
evaluate_parser.py
```

Then:

```python
from evaluation_data import TEST_CASES
from resume_parser import parse_resume


for case in TEST_CASES:

    predicted = parse_resume(
        case["text"]
    )

    print(predicted)
    print(case["expected"])
```

Run:

```bash
python evaluate_parser.py
```

Now every time we modify the parser, we can run the same tests.

---

# 24. Regression Testing

Suppose we fix:

```text
Technical Expertise
```

but accidentally break:

```text
Skills
```

If we only test the new example, we may not notice.

Regression testing means:

> **After changing the program, rerun previous tests to make sure old behavior still works.**

Our workflow becomes:

```text
Change Parser
      ↓
Run Test Cases
      ↓
Did old cases still work?
      ↓
Yes → Continue
No  → Fix
```

This is a very important software engineering habit.

---

# 25. Challenge — Add Five More Resumes

Create at least five additional cases.

Try:

```text
Different capitalization
Different section names
Missing phone
Missing email
Multiple emails
Multiple phone numbers
Skills on one line
Skills on many lines
No explicit Skills heading
```

The goal is not to make the parser perfect.

The goal is to discover its failure modes.

---

# 26. Record the Failure Modes

Create a table:

```text
| Problem | Example | Current Result | Desired Result |
|---|---|---|---|
| Different heading | Technical Expertise | Missed | Skills |
| Name below title | Software Engineer / John Smith | Wrong | John Smith |
| Skill phrase | Deep Learning | Missed | Deep Learning |
| Multiple emails | two addresses | First only | Depends |
```

This is extremely valuable.

We are building a **map of the problem**.

---

# 27. Why Not Just Add More Rules?

At this point you may think:

> "Let's just keep adding rules."

Sometimes that is the correct answer.

But consider the direction we're heading:

```text
More resumes
      ↓
More exceptions
      ↓
More rules
      ↓
More interactions between rules
      ↓
Harder maintenance
```

Eventually we need to decide whether the problem is still suitable for a rule-based approach.

This is not an argument against rules.

It is an argument for choosing the right level of complexity.

---

# 28. Separate Deterministic and Semantic Tasks

Let's classify our extraction tasks.

### Strongly deterministic

```text
Email
Phone
URL
```

Rules are usually a reasonable first choice.

### Moderately structured

```text
Section headings
Dates
Education entries
```

Rules and heuristics can work.

### More semantic

```text
What skills does this person have?
What role does this experience represent?
Is this experience relevant to machine learning?
Is "predictive modeling" related to "machine learning"?
```

These problems depend more heavily on meaning.

This distinction will guide our next step.

---

# 29. The Architecture We Have Now

Our system is becoming:

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
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
 Deterministic     Structured      Semantic
   Patterns          Rules          Problems
       │               │               │
       ▼               ▼               ▼
   Regex          Heuristics       NLP / ML
```

We have not implemented the final column yet.

But now we have a reason to.

---

# 30. A Key Design Principle

We don't need to replace the entire rule-based parser with NLP.

We can combine approaches.

For example:

```text
Email
  ↓
Regex

Phone
  ↓
Regex

URLs
  ↓
Regex

Sections
  ↓
Rules

Skills
  ↓
NLP / Semantic Matching
```

This is often better than:

```text
Everything
  ↓
One giant model
```

Different problems can use different tools.

---

# 31. The Next Upgrade

Our next question is:

> **Can we make the skill matching more semantic?**

Currently:

```text
Resume:
"Built convolutional neural networks
for image classification."

Skill dictionary:
"computer vision"
```

Our rule-based parser may say:

```text
No match
```

A more semantic system could potentially recognize that the text is related to computer vision.

Before using modern language models, we can explore techniques we already encountered earlier:

```text
TF-IDF
Cosine Similarity
```

Then:

```text
Embeddings
```

This gives us another important progression:

```text
Exact Match
    ↓
Lexical Similarity
    ↓
Semantic Similarity
```

---

# 32. What Comes Next

We have now taken the resume parser through its first engineering cycle:

```text
Build
 ↓
Test
 ↓
Find failures
 ↓
Improve
 ↓
Evaluate again
```

The parser is now ready for its next challenge.

We will create:

# Project 2.2 — Semantic Skill Matching

Instead of asking:

```text
"Does the resume contain the exact phrase?"
```

we will ask:

```text
"How similar is this resume text
to the concept we are looking for?"
```

We will first implement this with techniques students already know:

```text
TF-IDF
+
Cosine Similarity
```

Then we will see why cosine similarity is still limited.

That limitation will lead naturally into:

```text
Embeddings
```

and eventually into the resume-to-job matching system.

The progression is now:

```text
Regex
  ↓
Rules
  ↓
TF-IDF
  ↓
Cosine Similarity
  ↓
Embeddings
  ↓
Resume ↔ Job Matching
```
