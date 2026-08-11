# Project 2 - Build a Resume Parser

## From Text to Structured Information

In Project 1, we built a document reader.

The application could take:

```text
resume.jpg
```

and turn it into:

```text
John Smith
Python Developer
john@example.com
Skills
Python
TensorFlow
SQL
```

We solved one problem:

> **How do we extract text from a document?**

Now we have a new problem:

> **How do we turn that text into useful information?**

A human can look at the text and immediately recognize:

```text
Name
Email
Phone
Skills
Education
Experience
```

Our Python program cannot automatically assume that.

So our new pipeline becomes:

```text
Resume
   ↓
Document Reader
   ↓
Raw Text
   ↓
Information Extraction
   ↓
Structured Data
```

We will initially solve this using **rules and regular expressions**.

That is deliberate.

Before reaching for machine learning, we should understand what can be solved with simple deterministic techniques.

---

# 1. What Is a Resume Parser?

A resume parser is a program that takes an unstructured resume and extracts useful information from it.

For example, given:

```text
John Smith

Email: john.smith@example.com
Phone: +1 555 123 4567

Python Developer

Skills:
Python
SQL
TensorFlow
OpenCV

Education:
BSc Computer Science

Experience:
Software Developer - 2022-2025
```

we want something closer to:

```python
{
    "name": "John Smith",
    "email": "john.smith@example.com",
    "phone": "+1 555 123 4567",
    "skills": [
        "Python",
        "SQL",
        "TensorFlow",
        "OpenCV"
    ],
    "education": [
        "BSc Computer Science"
    ],
    "experience": [
        "Software Developer - 2022-2025"
    ]
}
```

Notice what happened.

We transformed:

```text
Unstructured text
```

into:

```text
Structured data
```

This is the central problem of this project.

---

# 2. Our Pipeline

We can connect Project 1 directly to Project 2.

```text
                 RESUME
                    │
                    ▼
             Document Reader
                    │
                    ▼
                  Raw Text
                    │
                    ▼
             Text Cleaning
                    │
                    ▼
          Information Extraction
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
        Contact   Skills    Sections
          │         │         │
          └─────────┼─────────┘
                    ▼
             Structured Resume
```

The important thing is that we are **reusing Project 1**.

We don't want to build another OCR system.

Project 1 gives us text.

Project 2 gives that text meaning and structure.

---

# 3. Start Without Machine Learning

It might be tempting to immediately train a machine learning model.

Don't.

Our first parser will use:

```text
Python
+
String processing
+
Regex
+
Rules
```

Why?

Because some information has very predictable patterns.

For example:

```text
Email addresses
Phone numbers
Dates
URLs
```

These don't necessarily require machine learning.

This gives us an important engineering principle:

> **Use the simplest technique that solves the problem.**

---

# 4. Extracting an Email Address

Suppose our resume contains:

```text
Contact me at john.smith@example.com
```

We know that an email has a recognizable structure.

We can use regex.

```python
import re

pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

emails = re.findall(
    pattern,
    text
)
```

For example:

```python
text = """
John Smith
Email: john.smith@example.com
"""

emails = re.findall(
    pattern,
    text
)

print(emails)
```

We might get:

```text
['john.smith@example.com']
```

---

# 5. Extracting Phone Numbers

Phone numbers are more complicated because they can appear in many formats.

For example:

```text
+1 555 123 4567
```

or:

```text
+1-555-123-4567
```

or:

```text
555-123-4567
```

We can start with a simple pattern:

```python
phone_pattern = r"(?:\+?\d[\d\s().-]{7,}\d)"

phones = re.findall(
    phone_pattern,
    text
)
```

Then inspect the results.

Remember:

> Regex patterns are rules, not magic.

A pattern that works well for one country's phone numbers may not work perfectly for another.

---

# 6. Extracting URLs

A resume may contain:

```text
https://github.com/johnsmith
https://linkedin.com/in/johnsmith
```

We can extract URLs with another pattern.

```python
url_pattern = r"https?://[^\s]+"

urls = re.findall(
    url_pattern,
    text
)
```

Now:

```text
Resume
   ↓
Regex
   ↓
Emails
Phones
URLs
```

We are gradually building our parser.

---

# 7. Extracting Skills

Skills are different.

There isn't a universal regex for:

```text
Python
TensorFlow
SQL
Docker
```

Instead, we can start with a known vocabulary.

For example:

```python
KNOWN_SKILLS = [
    "python",
    "sql",
    "pandas",
    "numpy",
    "tensorflow",
    "keras",
    "pytorch",
    "opencv",
    "docker",
    "git",
    "linux",
    "aws"
]
```

Now normalize the resume:

```python
normalized_text = text.lower()
```

Then:

```python
found_skills = []

for skill in KNOWN_SKILLS:

    if skill in normalized_text:

        found_skills.append(skill)
```

For example:

```text
Resume:

Python Developer
Experience with TensorFlow and SQL
```

might produce:

```python
[
    "python",
    "sql",
    "tensorflow"
]
```

---

# 8. Why This Approach Is Useful

This is a very simple system.

But it has an advantage:

> **We know exactly why it produced its result.**

If the parser says:

```text
Python
```

we know why:

```text
"python" was found in the resume.
```

This is a rule-based system.

There is no hidden model.

---

# 9. The Problem With Keyword Matching

Now consider:

```text
I have experience building
Python-based machine learning systems.
```

Our system can detect:

```text
Python
```

But suppose the resume says:

```text
Developed predictive models using
the Python ecosystem.
```

It might still work.

But consider:

```text
Built convolutional neural networks
for image classification.
```

There may be no literal:

```text
"computer vision"
```

even though the experience is clearly related.

Our dictionary cannot infer that.

This is the first important limitation.

---

# 10. Extracting Sections

Resumes often contain headings such as:

```text
Skills
Education
Experience
Projects
Certifications
```

We can use those headings as clues.

Suppose we have:

```text
Skills
Python
SQL
TensorFlow

Education
BSc Computer Science

Experience
Software Developer
```

We can think of the document as:

```text
Skills
   ↓
Everything until the next section

Education
   ↓
Everything until the next section

Experience
   ↓
Everything until the next section
```

This gives us a simple rule-based section parser.

---

# 11. Normalize Section Names

Different resumes may use:

```text
Skills
Technical Skills
Core Skills
Technologies
```

Similarly:

```text
Experience
Work Experience
Professional Experience
Employment History
```

We can define aliases.

```python
SECTION_ALIASES = {
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "technologies"
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history"
    ],
    "education": [
        "education",
        "academic background"
    ],
    "projects": [
        "projects",
        "personal projects"
    ]
}
```

This is still rule-based.

We are simply making our rules more flexible.

---

# 12. Split the Resume Into Lines

Instead of treating the entire resume as one string:

```python
lines = text.splitlines()
```

Now:

```python
for line in lines:
    print(line)
```

A resume such as:

```text
John Smith
john@example.com

Skills
Python
SQL
TensorFlow

Education
BSc Computer Science
```

becomes roughly:

```python
[
    "John Smith",
    "john@example.com",
    "",
    "Skills",
    "Python",
    "SQL",
    "TensorFlow",
    "",
    "Education",
    "BSc Computer Science"
]
```

This structure is useful for section detection.

---

# 13. Detect a Section

We can normalize each line:

```python
line = line.strip().lower()
```

Then compare it with our known headings.

For example:

```python
if line in SECTION_ALIASES["skills"]:
    current_section = "skills"
```

Then:

```python
if line in SECTION_ALIASES["education"]:
    current_section = "education"
```

We can continue this pattern.

---

# 14. A Simple Section Parser

A basic implementation could look like:

```python
def parse_sections(text):

    sections = {
        "skills": [],
        "education": [],
        "experience": [],
        "projects": []
    }

    current_section = None

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        normalized = line.lower()

        if normalized in [
            "skills",
            "technical skills",
            "core skills"
        ]:
            current_section = "skills"
            continue

        if normalized in [
            "education",
            "academic background"
        ]:
            current_section = "education"
            continue

        if normalized in [
            "experience",
            "work experience",
            "professional experience"
        ]:
            current_section = "experience"
            continue

        if normalized in [
            "projects",
            "personal projects"
        ]:
            current_section = "projects"
            continue

        if current_section:
            sections[current_section].append(line)

    return sections
```

This is not a perfect resume parser.

That's the point.

We are building the first version so that we can understand its limitations.

---

# 15. Extract the Name

Names are surprisingly difficult.

We might be tempted to say:

```text
"The first line is the name."
```

For a simple resume, that might work:

```text
John Smith
Email: ...
```

But another resume might begin with:

```text
RESUME
John Smith
```

or:

```text
Curriculum Vitae
John Smith
```

or:

```text
JOHN SMITH
Software Engineer
```

So name extraction requires assumptions.

For our first version, we can use a simple heuristic:

```python
def extract_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    return lines[0]
```

This is intentionally simple.

We will later discover why it isn't reliable enough.

---

# 16. Build the Parser Functions

Create:

```text
resume_parser.py
```

We can define:

```python
def extract_email(text):
    ...


def extract_phone(text):
    ...


def extract_urls(text):
    ...


def extract_name(text):
    ...


def extract_skills(text):
    ...


def parse_sections(text):
    ...
```

Now the resume parser becomes a collection of smaller components.

---

# 17. Build One Main Function

We can expose a single function to the rest of the application:

```python
def parse_resume(text):

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "urls": extract_urls(text),
        "skills": extract_skills(text),
        "sections": parse_sections(text)
    }
```

Now another part of our application only needs:

```python
resume = parse_resume(text)
```

This is another example of separation of responsibilities.

---

# 18. Connect Project 1 and Project 2

We now have two components:

```text
Document Reader
        ↓
Raw Text
        ↓
Resume Parser
        ↓
Structured Resume
```

The document reader doesn't need to know anything about resumes.

The resume parser doesn't need to know anything about OCR.

That separation is extremely useful.

---

# 19. Connect the Parser to Streamlit

Our Streamlit application can use:

```python
from document_reader import process_document
from resume_parser import parse_resume
```

Then:

```python
text = process_document(image)

resume = parse_resume(text)
```

We can display the result.

For example:

```python
st.subheader("Contact")

st.write(
    "Name:",
    resume["name"]
)

st.write(
    "Email:",
    resume["email"]
)

st.write(
    "Phone:",
    resume["phone"]
)
```

---

# 20. Display Skills

```python
st.subheader("Skills")

for skill in resume["skills"]:

    st.write(
        f"- {skill}"
    )
```

Now the application is beginning to look like a real resume parser.

---

# 21. Display Sections

```python
st.subheader("Resume Sections")

for section, items in resume["sections"].items():

    st.markdown(
        f"### {section.title()}"
    )

    for item in items:

        st.write(
            f"- {item}"
        )
```

The raw document has now become structured UI.

---

# 22. The Full Pipeline

We now have:

```text
                 RESUME
                    │
                    ▼
             Image / PDF
                    │
                    ▼
            Document Reader
                    │
                    ▼
                  OCR
                    │
                    ▼
              Raw Text
                    │
                    ▼
             Resume Parser
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
        Contact   Skills    Sections
          │         │         │
          └─────────┼─────────┘
                    ▼
             Structured Data
                    │
                    ▼
              Streamlit UI
```

This is the first genuinely multi-stage intelligent system we have built.

---

# 23. The Limitations of Rules

At this point, our parser will fail on real resumes.

That's expected.

For example:

```text
Resume A
```

might work perfectly.

But:

```text
Resume B
```

might have:

```text
Technical Expertise
```

instead of:

```text
Skills
```

Our section parser may miss it.

Another resume may write:

```text
Professional Background
```

instead of:

```text
Experience
```

Our rules won't understand the relationship automatically.

This gives us an important observation:

> **Rules are powerful when the problem is predictable, but brittle when language becomes variable.**

---

# 24. Where Regex Starts Breaking

Regex is excellent for:

```text
Email
Phone
URLs
Dates
```

But consider:

```text
Worked extensively with
machine learning and predictive analytics.
```

What exactly is the skill?

Maybe:

```text
Machine Learning
Predictive Analytics
```

But perhaps the person also has experience with:

```text
scikit-learn
classification
regression
feature engineering
```

There is no single regex that understands all of these relationships.

We are starting to reach the boundary of rule-based extraction.

---

# 25. Where Keyword Lists Start Breaking

Suppose our skill list contains:

```python
"computer vision"
```

but the resume says:

```text
Developed image classification systems
using convolutional neural networks.
```

A simple keyword matcher may not detect:

```text
Computer Vision
```

But a human can understand the relationship.

Similarly:

```text
PostgreSQL
```

is related to:

```text
SQL
```

but they are not the same literal word.

Our dictionary cannot automatically reason about these relationships.

---

# 26. This Failure Is Useful

We deliberately built a simple system first.

Why?

Because now we have a concrete problem.

```text
Rule-based parser
       ↓
Works on predictable patterns
       ↓
Fails on language variation
```

That gives us a reason to ask:

> **Can NLP help us understand text beyond exact keyword matching?**

Now concepts such as:

```text
Tokenization
N-grams
TF-IDF
Embeddings
Semantic similarity
Named entities
```

have a real purpose.

They are not just techniques in a textbook.

They are potential solutions to a problem we just encountered.

---

# 27. Exercise - Break Your Parser

Create several artificial resumes.

### Resume A

```text
John Smith

Email: john@example.com

Skills
Python
SQL
TensorFlow

Education
BSc Computer Science

Experience
Software Developer
```

### Resume B

```text
Jane Doe

Contact
jane@example.com

Technical Expertise
Python, Pandas, NumPy

Academic Background
MSc Data Science

Professional Experience
Data Analyst
```

### Resume C

```text
Alex Johnson

alex@example.com

Core Competencies
Python
Machine Learning
Computer Vision

Employment History
ML Engineer
```

Run all three through your parser.

Record what works and what fails.

---

# 28. Create an Evaluation Table

Create:

```text
| Field      | Resume A | Resume B | Resume C |
|------------|----------|----------|----------|
| Name       | ✓        | ✓        | ✓        |
| Email      | ✓        | ✓        | ✓        |
| Skills     | ✓        | ?        | ?        |
| Education  | ✓        | ?        | ?        |
| Experience | ✓        | ?        | ?        |
```

The exact results depend on your implementation.

The important part is to **measure the failures**.

---

# 29. Challenge - Improve the Rules

Before introducing NLP, try improving the rule-based system.

Add more section aliases:

```python
"technical expertise"
"core competencies"
"professional background"
"employment history"
```

Add more skills.

Add more phone formats.

Improve the name heuristic.

Then run the same evaluation set again.

Ask:

> Did adding rules improve the parser?

Probably.

Then ask:

> Can we keep adding rules forever?

This is the beginning of an engineering trade-off we want students to understand.

---

# 30. Rule Explosion

Imagine trying to support every possible resume.

We might eventually have:

```text
50 skill aliases
100 section aliases
20 phone formats
30 education formats
50 date formats
```

Then more exceptions appear.

The program becomes:

```text
if this
    ...
elif that
    ...
elif another thing
    ...
elif special case
    ...
```

This is sometimes called **rule explosion**.

The problem isn't that rules are bad.

The problem is that the underlying problem is no longer completely deterministic.

Language is variable.

---

# 31. The Next Question

We have now reached an important point.

We started with:

```text
Regex
+
Rules
```

and discovered:

```text
Predictable patterns
        ↓
Rules work well

Variable language
        ↓
Rules become brittle
```

This is exactly where we want to introduce more advanced NLP.

We can now revisit techniques from earlier phases:

```text
Text
 ↓
Tokens
 ↓
Representation
 ↓
Similarity / Model
```

and ask:

> **Can we represent text in a way that captures more than exact word matching?**

That will become the next stage of our resume parser.

---

# 32. What We Have Learned

We didn't start with a sophisticated AI model.

We started with:

```text
Regex
Rules
Dictionaries
```

Then we tested the system.

Then we found its limitations.

This is a realistic development process:

```text
Understand problem
      ↓
Build simplest solution
      ↓
Test
      ↓
Find limitations
      ↓
Improve
```

A good engineer does not automatically reach for the most complicated model.

---

# 33. The Evolution of Our System

We now have:

```text
Project 1
Document Reader

Image
 ↓
OCR
 ↓
Text
```

and:

```text
Project 2
Resume Parser

Text
 ↓
Regex
 ↓
Rules
 ↓
Structured Information
```

The next problem is:

```text
Resume
     +
Job Description
     ↓
How well do they match?
```

That takes us to:

# Project 3 - Resume ↔ Job Matching

We will start with techniques students have already encountered:

```text
TF-IDF
+
Cosine Similarity
```

Then revisit:

```text
BM25
```

from the chatbot project.

Finally, we will explore why lexical similarity has limitations and where embeddings can help.

The progression is becoming:

```text
Pixels
  ↓
Text
  ↓
Information
  ↓
Similarity
  ↓
Decision
```

That is the foundation for our final intelligent application.
