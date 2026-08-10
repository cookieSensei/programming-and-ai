# Phase 4 - Building Real AI Applications

## From Machine Learning Experiments to Real Software

By the end of the previous phases, we have learned how to:

- Write Python programs
- Work with data using Pandas and NumPy
- Perform exploratory data analysis
- Train and evaluate classical machine learning models
- Work with NLP and text
- Process images with OpenCV
- Build neural networks with TensorFlow/Keras
- Train CNNs
- Use transfer learning
- Save and load trained models
- Build interfaces with Streamlit

We have learned many individual tools.

Now it is time to put them together.

> **Phase 4 is about building real software using everything we have learned so far.**

Instead of asking:

> "How do I train this model?"

we start asking:

> **"How do I build an application around this model?"**

---

# Phase 4 Overview

The phase follows this progression:

```text
Notebook
   ↓
Python Application
   ↓
File & Document Processing
   ↓
OCR
   ↓
Computer Vision
   ↓
NLP
   ↓
Information Extraction
   ↓
Machine Learning
   ↓
Model Integration
   ↓
Streamlit
   ↓
Real AI Application
   ↓
Capstone Project
```

---

# Module 1 - From Notebook to Application

Before building larger projects, we need to understand how to turn experiments into software.

So far, much of our work has happened inside notebooks.

A notebook is excellent for:

- experimentation
- visualization
- EDA
- trying ideas
- inspecting data

But applications usually need a different structure.

We want to move toward:

```text
project/
│
├── app.py
├── requirements.txt
├── models/
├── data/
├── src/
└── README.md
```

## Topics

### Python project structure

Learn how to organize a project into:

- Python files
- folders
- modules
- functions
- configuration
- data
- models

### Requirements

Create:

```text
requirements.txt
```

and understand why a project should explicitly describe its dependencies.

### Virtual environments

Understand why projects use isolated Python environments.

### Separation of concerns

Instead of putting everything inside `app.py`:

```text
UI
+
Data processing
+
ML
+
Prediction
```

we begin separating responsibilities:

```text
UI
│
├── Input
│
└── Output

Processing
│
├── Cleaning
├── Feature extraction
└── Prediction
```

The goal is to make our applications easier to understand and maintain.

---

# Module 2 - Working with Real-World Documents

Our datasets so far have generally been clean.

Real-world applications are different.

A user might give us:

```text
resume.pdf
resume.jpg
invoice.png
scanned_document.jpg
```

The information we need may be buried inside an image or PDF.

This introduces a new problem:

> **How do we turn an unstructured document into data that Python can understand?**

This module introduces document processing.

---

# Project 1 - Build a Document Reader

We will build an application that allows a user to upload a document and extract its text.

The basic pipeline:

```text
Document
    ↓
Image / PDF
    ↓
Image Processing
    ↓
OCR
    ↓
Raw Text
    ↓
Text Cleaning
    ↓
Streamlit
```

---

# Module 3 - OCR

OCR stands for:

> **Optical Character Recognition**

OCR allows us to extract text from an image.

For example:

```text
Image:

┌─────────────────────┐
│ Name: John Smith    │
│ Email: john@x.com   │
│ Python Developer    │
└─────────────────────┘

          ↓ OCR

"Name: John Smith
 Email: john@x.com
 Python Developer"
```

## Topics

Students learn how OCR fits into a larger pipeline.

```text
Image
  ↓
Preprocessing
  ↓
OCR
  ↓
Text
```

They also learn that OCR is not magic.

Poor image quality can produce poor text.

This leads naturally into computer vision.

---

# Module 4 - Computer Vision for Document Processing

Before sending an image to OCR, we can improve it.

Using OpenCV, we can perform operations such as:

```text
Resize
Grayscale
Blur
Threshold
Crop
```

The pipeline becomes:

```text
Original Image
      ↓
Grayscale
      ↓
Noise Reduction
      ↓
Thresholding
      ↓
OCR
      ↓
Text
```

Students now see computer vision being used for a real purpose.

---

# Project 1 Final Version - Document Reader

The application should allow a user to:

1. Upload an image/document
2. Preview the document
3. Preprocess the image
4. Run OCR
5. Display extracted text
6. Clean the extracted text
7. Download or copy the result

Example:

```text
┌─────────────────────────────────────┐
│         📄 Document Reader           │
├─────────────────────────────────────┤
│                                     │
│ Upload document                     │
│ [ Choose File ]                     │
│                                     │
│ Original Image                      │
│                                     │
│ ┌───────────────────────────────┐   │
│ │                               │   │
│ │          DOCUMENT             │   │
│ │                               │   │
│ └───────────────────────────────┘   │
│                                     │
│ Extracted Text                      │
│ ┌───────────────────────────────┐   │
│ │ Name: John Smith              │   │
│ │ Email: john@example.com       │   │
│ │ Python Developer              │   │
│ └───────────────────────────────┘   │
└─────────────────────────────────────┘
```

This becomes the foundation for the next project.

---

# Module 5 - NLP Information Extraction

OCR gives us text.

But raw text isn't enough.

Suppose we extract:

```text
John Smith
john@example.com
+1 555 123 4567

Python Developer

Skills:
Python
TensorFlow
SQL
OpenCV
```

We want our program to turn this into structured information:

```python
{
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "+1 555 123 4567",
    "skills": [
        "Python",
        "TensorFlow",
        "SQL",
        "OpenCV"
    ]
}
```

This is **information extraction**.

---

# Module 6 - Resume Parser

## Project 2 - Build a Real Resume Parser

The first major Phase 4 project will be a resume parser.

Input:

```text
resume.pdf
```

Output:

```text
Name
Email
Phone
Skills
Education
Experience
Projects
```

---

# Resume Parser Version 1 - Rule-Based Extraction

We begin without machine learning.

This is intentional.

We already know Python and regex.

For example, an email address can be detected using a regular expression.

```text
Resume
  ↓
Extract text
  ↓
Regex
  ↓
Email / Phone / Dates
```

We can also maintain a skill dictionary:

```python
skills = [
    "python",
    "tensorflow",
    "pytorch",
    "sql",
    "docker",
    "opencv",
    "pandas"
]
```

Then search the resume for known skills.

The important lesson:

> **Not every intelligent-looking problem requires machine learning.**

Sometimes a simple rule is the correct solution.

---

# Resume Parser Version 2 - NLP

Now we improve our parser.

Instead of treating the resume as one giant string, we begin working with language.

Topics can include:

- tokenization
- normalization
- sentence splitting
- word frequencies
- text cleaning
- phrases
- basic entity extraction
- section detection

The pipeline becomes:

```text
Resume
  ↓
Text
  ↓
Cleaning
  ↓
Tokenization
  ↓
NLP
  ↓
Structured Information
```

---

# Module 7 - Resume ↔ Job Matching

A resume parser extracts information.

Now we make the application useful.

We give the application two inputs:

```text
Resume
+
Job Description
```

For example:

```text
Job Description:

We are looking for a Python developer
with experience in machine learning,
TensorFlow, SQL and computer vision.
```

The application compares this with the candidate's resume.

---

# First Matching System

We can use concepts already introduced earlier in the curriculum:

```text
TF-IDF
   ↓
Vector representation
   ↓
Cosine Similarity
   ↓
Resume ↔ Job Description
```

The result could be:

```text
Match Score: 82%
```

We can also show:

```text
Matched Skills

✓ Python
✓ TensorFlow
✓ SQL
✓ Computer Vision

Missing Skills

✗ Docker
✗ AWS
```

This creates a practical reason to revisit text representation and similarity.

---

# Module 8 - Machine Learning Inside Applications

At this point we move from:

```text
Training a model
```

to:

```text
Using a trained model
```

The workflow becomes:

```text
Training
   ↓
Evaluation
   ↓
Save Model
   ↓
Application
   ↓
Load Model
   ↓
User Input
   ↓
Prediction
```

Students should understand that model training and model usage are two different stages.

---

# Model Integration

We have already learned how to save models.

Now we build applications that load them.

For example:

```python
model = load_model("models/model.h5")
```

Then:

```python
prediction = model.predict(input_data)
```

The user doesn't need to know anything about the model.

They simply interact with the application.

---

# Module 9 - Bringing Computer Vision into Applications

We have already trained CNNs and used transfer learning.

Now we use those models inside software.

For example:

```text
Image
  ↓
Preprocessing
  ↓
CNN
  ↓
Prediction
  ↓
Streamlit
```

The application could classify:

```text
Cat
Dog
```

or:

```text
Resume
Invoice
Other Document
```

The important lesson is:

> **A trained model becomes useful when an application can actually use it.**

---

# Optional Project - Document Classifier

Students can build a small image classification application.

For example:

```text
Upload Document
      ↓
CNN / Transfer Learning
      ↓
┌───────────────┐
│ Resume        │
│ Invoice       │
│ Other         │
└───────────────┘
```

This provides a practical use for the CNN and transfer-learning concepts from earlier phases.

---

# Module 10 - Building the Streamlit Application

Now we bring everything together through Streamlit.

The UI becomes the front door to our system.

Instead of:

```text
python script.py
```

the user gets:

```text
Web Application
```

---

# Streamlit Application Architecture

We should begin separating the application into layers.

```text
                 STREAMLIT
                     │
             User Interface
                     │
                     ▼
             Application Logic
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   Document       NLP            ML
   Processing                  Models
        │            │            │
        └────────────┼────────────┘
                     ▼
                  Result
                     │
                     ▼
                Streamlit
```

The UI should not contain all of the application's logic.

---

# Module 11 - EDA Inside Real Applications

EDA doesn't disappear just because we are building software.

We can use EDA to understand:

- resume datasets
- skill frequencies
- document lengths
- experience distributions
- classification results
- model performance
- extracted information

For example:

```text
Most common skills

Python       ███████████████
SQL          ███████████
TensorFlow   ████████
Docker       █████
AWS          ████
```

Students now see EDA as a tool for understanding real data rather than merely a notebook exercise.

---

# Module 12 - The Complete Resume Intelligence Platform

## Capstone Project

The major Phase 4 project is:

# Resume Intelligence Platform

The application accepts:

```text
Resume
+
Job Description
```

and produces useful information.

---

# Complete Pipeline

```text
                     RESUME
                        │
                        ▼
                PDF / Image Reader
                        │
                        ▼
                       OCR
                        │
                        ▼
                OpenCV Processing
                        │
                        ▼
                  Text Cleaning
                        │
                        ▼
                       NLP
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
         Skills     Education    Experience
            │           │           │
            └───────────┼───────────┘
                        ▼
                Feature Extraction
                        │
                        ▼
                Resume Representation
                        │
                        │
              JOB DESCRIPTION
                        │
                        ▼
                Text Processing
                        │
                        ▼
                  Representation
                        │
                        ▼
                  Similarity / ML
                        │
                        ▼
                   Match Score
                        │
                        ▼
                  Streamlit UI
```

---

# Capstone UI

The final application can contain multiple sections or tabs.

```text
┌───────────────────────────────────────────┐
│        🧠 Resume Intelligence              │
├───────────────────────────────────────────┤
│                                           │
│ [ Resume ] [ Job Match ] [ Analytics ]    │
│                                           │
└───────────────────────────────────────────┘
```

---

# Resume Tab

The user uploads a resume.

The application displays:

```text
Name
Email
Phone

Skills
────────────
Python
TensorFlow
SQL
OpenCV

Education
────────────
BSc Computer Science

Experience
────────────
3 years
```

---

# Job Match Tab

The user provides a job description.

The application calculates:

```text
Resume ↔ Job Description

Match Score
      82%
```

Then:

```text
Matched Skills
───────────────
✓ Python
✓ TensorFlow
✓ SQL
✓ Computer Vision

Missing Skills
───────────────
✗ Docker
✗ AWS
```

---

# Analytics Tab

Now we bring EDA into the product.

Possible visualizations:

- Most common skills
- Experience distribution
- Education distribution
- Resume length
- Skill frequency
- Match score distribution
- Model performance

This demonstrates that data analysis is useful beyond the classroom notebook.

---

# Module 13 - Making the Application Robust

Real software doesn't assume everything goes perfectly.

We need to handle:

```text
No file uploaded
Wrong file type
Corrupted file
Empty document
OCR failure
No text extracted
Unexpected text format
Model failure
```

Students should learn to think about:

```python
try:
    ...
except Exception:
    ...
```

and, more importantly, how to provide useful feedback to users.

For example:

```text
❌ We couldn't extract text from this document.

Please upload a clearer image or PDF.
```

rather than exposing a Python traceback to the user.

---

# Module 14 - Project Documentation

A real project should be understandable by someone who didn't build it.

Students should create:

```text
README.md
```

containing:

- Project description
- Features
- Installation instructions
- Requirements
- How to run the application
- Example usage
- Project architecture
- Model information
- Limitations

Example:

```text
# Resume Intelligence

A document-processing application that extracts
information from resumes and compares them
against job descriptions.
```

---

# Phase 4 Capstone Requirements

The final project should demonstrate the student's ability to combine multiple parts of the curriculum.

## Required

### Python

- Functions
- Modules
- File handling
- Error handling
- Project structure

### EDA

- Load data
- Explore data
- Create useful visualizations
- Interpret findings

### Machine Learning

- Prepare data
- Train or use a model
- Evaluate it
- Understand the metric
- Save/load the model

### Deep Learning

Where appropriate:

- Load a trained neural network
- Preprocess input
- Run inference

### Computer Vision

- Image loading
- Image preprocessing
- OCR and/or image classification

### NLP

- Text cleaning
- Tokenization
- Information extraction
- Text representation
- Similarity/matching

### Streamlit

- File upload
- User input
- Results
- Progress indicators
- Application layout

---

# Optional Advanced Extensions

Once the basic system works, students can improve it.

## Extension 1 - Better Resume Section Detection

Automatically identify:

```text
Education
Experience
Projects
Skills
Certifications
```

---

## Extension 2 - Better Matching

Compare:

```text
TF-IDF + Cosine Similarity
```

with another representation.

Students can investigate whether semantic representations improve matching.

---

## Extension 3 - Resume Classification

Train a model to classify resumes into categories such as:

```text
Data Science
Web Development
Computer Vision
DevOps
Finance
Marketing
```

---

## Extension 4 - Document Classification

Classify uploaded documents:

```text
Resume
Invoice
Report
Other
```

Then route the document to the appropriate processing pipeline.

---

## Extension 5 - Analytics Dashboard

Allow users to upload multiple resumes and analyze the entire collection.

For example:

```text
100 Resumes

Python mentioned: 78%
SQL mentioned: 61%
TensorFlow mentioned: 23%
Docker mentioned: 17%
```

Now the application becomes a small data-analysis platform.

---

# Alternative Capstone Projects

Students who don't want to build the resume system can choose another document-intelligence project.

## Track A - Resume Intelligence

```text
OCR
+
NLP
+
ML
+
Streamlit
```

Extract and analyze resumes.

## Track B - Invoice Intelligence

```text
Image/PDF
    ↓
OCR
    ↓
Text Cleaning
    ↓
Information Extraction
    ↓
Structured Invoice
```

Extract:

```text
Invoice Number
Date
Vendor
Items
Quantity
Tax
Total
```

## Track C - Document Intelligence

Build a general document-processing application.

```text
Upload Document
      ↓
Classify Document
      ↓
Extract Text
      ↓
Extract Relevant Fields
      ↓
Display Structured Information
```

---

# The Final Learning Progression

The entire curriculum has now moved from small experiments to a complete application.

```text
PHASE 0
Python & Developer Workflow
        ↓
PHASE 1
Programming Fundamentals
        ↓
PHASE 2
Building Python Applications
        ↓
PHASE 3
Teaching Computers to Learn
        ↓
PHASE 4
Building Real AI Applications
```

And inside Phase 4:

```text
Python
  ↓
Project Structure
  ↓
Real-world Files
  ↓
OpenCV
  ↓
OCR
  ↓
Regex
  ↓
NLP
  ↓
Information Extraction
  ↓
EDA
  ↓
Machine Learning
  ↓
Deep Learning
  ↓
Model Inference
  ↓
Streamlit
  ↓
Real Application
  ↓
Capstone
```

---

# The Big Idea of Phase 4

The goal of Phase 4 is not to teach another collection of libraries.

The goal is to change how students think about their work.

Earlier, we asked:

> **"Can I write this code?"**

Then:

> **"Can I analyze this data?"**

Then:

> **"Can I train this model?"**

Now we ask:

> **"Can I build something that another person can actually use?"**

A machine learning model is only one part of an AI application.

A real application looks more like:

```text
                    USER
                     │
                     ▼
               STREAMLIT UI
                     │
                     ▼
              INPUT HANDLING
                     │
                     ▼
             DATA PROCESSING
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        OpenCV      NLP         ML
          │          │          │
          └──────────┼──────────┘
                     ▼
                  MODEL
                     │
                     ▼
                PREDICTION
                     │
                     ▼
             POST-PROCESSING
                     │
                     ▼
                USER RESULT
```

This is the transition from:

> **learning machine learning**

to:

> **building software with machine learning.**

And that is what Phase 4 is about.
