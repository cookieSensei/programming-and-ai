# Project 1.1 - Refactoring the Document Reader into an Application

## From Prototype to Real Project

We have already built a working OCR prototype:

```text
Upload Image
     ↓
OpenCV
     ↓
Preprocessing
     ↓
OCR
     ↓
Regex Cleaning
     ↓
Text
```

Now we will take that experiment and organize it as a proper Python application.

The goal is not to learn another library.

The goal is to practice what we learned in **Anatomy of an Intelligent Application**:

> Separate the user interface from the processing logic.

---

# 1. Why Refactor?

Our first version may have put everything into:

```text
app.py
```

That is perfectly reasonable while experimenting.

But as the project grows, we may want to:

- change the OCR engine
- test preprocessing independently
- try different cleaning strategies
- reuse OCR in another project
- change the Streamlit interface

If everything is inside one file, these changes become harder.

Instead, we will separate the responsibilities.

---

# 2. Project Structure

Create:

```text
document-reader/
│
├── app.py
├── document_reader.py
├── requirements.txt
└── README.md
```

The responsibilities are:

```text
app.py
    ↓
Streamlit interface

document_reader.py
    ↓
Image processing
OCR
Text cleaning
```

The important idea is:

> `app.py` describes what the user can do. `document_reader.py` describes how the document is processed.

---

# 3. Create the Processing Module

Open:

```text
document_reader.py
```

Add:

```python
import re

import cv2
import pytesseract


def preprocess_image(image):
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    resized = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    blurred = cv2.GaussianBlur(
        resized,
        (5, 5),
        0
    )

    _, thresholded = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresholded
```

Now OCR:

```python
def extract_text(image):
    processed = preprocess_image(image)

    text = pytesseract.image_to_string(
        processed
    )

    return text
```

And text cleaning:

```python
def clean_text(text):
    text = re.sub(
        r"[^A-Za-z0-9\s.,@+-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()
```

Finally:

```python
def process_document(image):
    text = extract_text(image)

    text = clean_text(text)

    return text
```

Our processing module now has one clear responsibility:

> **Take an image and return cleaned text.**

---

# 4. Import Our Module

In `app.py`:

```python
from document_reader import process_document
```

This is similar to importing a library:

```python
import cv2
```

The difference is that `document_reader.py` is our own module.

We can now write:

```python
text = process_document(image)
```

without exposing all of the OCR and preprocessing details to the UI.

---

# 5. Build the Streamlit Interface

Start `app.py` with:

```python
import cv2
import numpy as np
import streamlit as st

from document_reader import process_document


st.title("📄 Document Reader")

st.write(
    "Upload a document image and extract its text."
)
```

Add the uploader:

```python
uploaded_file = st.file_uploader(
    "Upload document",
    type=["png", "jpg", "jpeg"]
)
```

---

# 6. Convert the Uploaded File

When Streamlit gives us an uploaded file, we need to turn it into an image that OpenCV understands.

```python
if uploaded_file:

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )
```

The data changes representation:

```text
Uploaded File
      ↓
Bytes
      ↓
NumPy Array
      ↓
OpenCV Image
```

---

# 7. Display the Image

```python
st.image(
    image,
    channels="BGR",
    caption="Uploaded document"
)
```

Now the user can confirm that the correct document was uploaded.

---

# 8. Run the Pipeline

Add a button:

```python
if st.button("Extract Text"):

    with st.spinner(
        "Reading document..."
    ):

        text = process_document(
            image
        )
```

Notice that `app.py` does not need to know:

- how grayscale conversion works
- how thresholding works
- how Tesseract works
- how regex cleaning works

It simply calls:

```python
process_document(image)
```

This is separation of responsibilities in practice.

---

# 9. Display the Result

Add:

```python
st.subheader(
    "Extracted Text"
)

st.text_area(
    "OCR Result",
    text,
    height=300
)
```

---

# 10. Complete `app.py`

Our application can now look like:

```python
import cv2
import numpy as np
import streamlit as st

from document_reader import process_document


st.title("📄 Document Reader")

st.write(
    "Upload a document image and extract its text."
)

uploaded_file = st.file_uploader(
    "Upload document",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    st.image(
        image,
        channels="BGR",
        caption="Uploaded document"
    )

    if st.button("Extract Text"):

        with st.spinner(
            "Reading document..."
        ):

            text = process_document(
                image
            )

        st.subheader(
            "Extracted Text"
        )

        st.text_area(
            "OCR Result",
            text,
            height=300
        )
```

---

# 11. The New Architecture

We now have:

```text
                 app.py
                   │
             Streamlit UI
                   │
                   ▼
          process_document()
                   │
                   ▼
          document_reader.py
                   │
          ┌────────┼─────────┐
          ▼        ▼         ▼
     Preprocess   OCR     Cleaning
          │        │         │
          └────────┴─────────┘
                   │
                   ▼
                  Text
```

This is much easier to reason about than one large script.

---

# 12. Test the Processing Module Separately

One benefit of separating our processing code is that we can use it without Streamlit.

Create:

```text
test_document_reader.py
```

For a simple test:

```python
import cv2

from document_reader import process_document


image = cv2.imread(
    "document.jpg"
)

text = process_document(
    image
)

print(text)
```

Run:

```bash
python test_document_reader.py
```

Now the same processing logic can be used by:

```text
Streamlit
    ↓
process_document()

Terminal
    ↓
process_document()
```

This is why separating application logic from the UI is useful.

---

# 13. Handle Invalid Images

Real applications need failure paths.

OpenCV can fail to decode an invalid image.

Add:

```python
if image is None:

    st.error(
        "Could not read this image."
    )

    st.stop()
```

The application should detect the problem before sending invalid data further down the pipeline.

---

# 14. Handle Empty OCR Results

OCR may return:

```python
""
```

If that happens, show a useful message:

```python
if not text:

    st.warning(
        "No readable text was found."
    )

else:

    st.text_area(
        "OCR Result",
        text,
        height=300
    )
```

A real application should handle both:

```text
Happy path
```

and:

```text
Failure path
```

---

# 15. Inspect the Intermediate Image

During development, it is useful to see what we actually send to OCR.

We can expose the processed image temporarily.

For example, modify `process_document()`:

```python
def process_document(image):

    processed = preprocess_image(
        image
    )

    raw_text = pytesseract.image_to_string(
        processed
    )

    cleaned_text = clean_text(
        raw_text
    )

    return {
        "processed_image": processed,
        "raw_text": raw_text,
        "cleaned_text": cleaned_text
    }
```

Now the pipeline is visible:

```text
Original Image
      ↓
Processed Image
      ↓
Raw OCR
      ↓
Cleaned OCR
```

This is useful for debugging.

---

# 16. Why This Is Better

Suppose the final text is wrong.

Without intermediate results, we might think:

> "OCR doesn't work."

But perhaps the real problem is:

```text
Original image
      ↓
Good
      ↓
Thresholding
      ↓
Destroyed the text
      ↓
OCR
      ↓
Bad result
```

Inspecting intermediate stages lets us identify where the problem occurred.

---

# 17. Don't Over-Engineer

We could immediately create a huge architecture:

```text
src/
services/
controllers/
repositories/
config/
utils/
```

We don't need that.

Our current project is small.

This is enough:

```text
document-reader/
│
├── app.py
├── document_reader.py
├── requirements.txt
└── README.md
```

The lesson is not:

> "There is one correct folder structure."

The lesson is:

> **Separate code when there is a meaningful responsibility to separate.**

---

# 18. Requirements

Create:

```text
requirements.txt
```

Add:

```text
opencv-python
numpy
pytesseract
streamlit
```

Then another person can install the Python dependencies with:

```bash
pip install -r requirements.txt
```

Remember:

> Tesseract itself is a separate system dependency from the Python package.

---

# 19. Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The complete workflow is now:

```text
Terminal
   ↓
streamlit run app.py
   ↓
Browser
   ↓
Upload document
   ↓
OpenCV
   ↓
OCR
   ↓
Text cleaning
   ↓
Result
```

---

# 20. Git Checkpoint

Once everything works:

```bash
git status
```

Then:

```bash
git add .
```

Then:

```bash
git commit -m "Refactor document reader into application"
```

We now have a checkpoint:

```text
Experiment
    ↓
Working prototype
    ↓
Refactored application
    ↓
Git checkpoint
```

---

# 21. Challenge - Add a Second Preprocessing Method

Our current pipeline is:

```text
Grayscale
 ↓
Resize
 ↓
Blur
 ↓
Threshold
```

Create another function:

```python
def preprocess_image_v2(image):
    ...
```

Try a different approach, such as adaptive thresholding.

Then allow the user to choose:

```text
Preprocessing Method

○ Standard Threshold
○ Adaptive Threshold
```

The application becomes:

```text
User
 ↓
Choose preprocessing
 ↓
Image
 ↓
Selected pipeline
 ↓
OCR
 ↓
Text
```

The goal is not to find a magical setting.

The goal is to understand how preprocessing changes the data sent to OCR.

---

# 22. Challenge - Preserve Document Structure

Our current cleaner collapses whitespace:

```python
text = re.sub(
    r"\s+",
    " ",
    text
)
```

Consider this:

```text
Skills

Python
TensorFlow
SQL

Education

BSc Computer Science
```

Collapsing all whitespace may produce:

```text
Skills Python TensorFlow SQL Education BSc Computer Science
```

That might be useful for search.

But it could be harmful for a resume parser because headings and sections contain useful structure.

Create another cleaning strategy that preserves line breaks.

Ask:

> **Which representation will be more useful for our next project?**

---

# 23. Challenge - Build a Small Evaluation Set

Create:

```text
test_documents/
│
├── clear_scan.jpg
├── blurry_photo.jpg
├── low_contrast.jpg
└── small_text.jpg
```

For each document, compare:

```text
OCR without preprocessing
```

against:

```text
OCR with preprocessing
```

Create a table:

```text
Document             Baseline       Preprocessed

clear_scan.jpg       ________       ________

blurry_photo.jpg     ________       ________

low_contrast.jpg     ________       ________

small_text.jpg       ________       ________
```

Ask:

1. Which documents work well?
2. Which documents fail?
3. Does preprocessing help?
4. Does image quality matter?
5. Does resizing help?
6. Does thresholding help?

We are beginning to evaluate an entire **pipeline**, not just a model.

---

# 24. Think Like an Engineer

A useful development cycle is:

```text
Baseline
   ↓
Change one thing
   ↓
Test
   ↓
Compare
   ↓
Keep / Reject
```

Avoid:

```text
Change ten things
   ↓
"It looks better"
```

If we change one component at a time, we can reason about why the result changed.

This is the same experimental mindset we used when learning machine learning.

---

# 25. What We Have Built

We started with:

```text
Image
```

and ended with:

```text
Image
 ↓
OpenCV
 ↓
Preprocessing
 ↓
OCR
 ↓
Regex
 ↓
Clean Text
 ↓
Streamlit
```

But the deeper lessons are:

### We separated UI from logic

```text
app.py
    ↓
document_reader.py
```

### We created a reusable processing function

```python
process_document(image)
```

### We created failure paths

```text
Invalid image
Empty OCR
```

### We evaluated a pipeline

```text
Baseline
vs
Preprocessed
```

### We created a Git checkpoint

```text
Experiment
 ↓
Application
 ↓
Checkpoint
```

These are all skills we will reuse throughout Phase 4.

---

# 26. The Limitation

Our application can answer:

> **"What text is inside this image?"**

But it cannot yet answer:

> "Who is this person?"

> "What skills do they have?"

> "Where did they study?"

> "How much experience do they have?"

We have converted:

```text
Pixels
 ↓
Text
```

but not:

```text
Text
 ↓
Meaning / Structure
```

That is the next problem.

---

# What Comes Next

The next project starts with the output of this one:

```text
Document Reader
      ↓
Raw Text
```

and asks:

> **Can we turn that text into structured information?**

For example:

```python
{
    "name": "John Smith",
    "email": "john@example.com",
    "skills": [
        "Python",
        "TensorFlow",
        "SQL"
    ],
    "education": [
        "BSc Computer Science"
    ]
}
```

That becomes:

# Project 2 - Build a Real Resume Parser

We will initially solve the problem using **Python, regex, and rules**.

Then we will discover where those rules begin to break down.

That failure will give us a reason to introduce more sophisticated NLP.

The progression is:

```text
Project 1
Pixels → Text

        ↓

Project 2
Text → Information

        ↓

Project 3
Information → Matching

        ↓

Final Project
Multiple systems → Intelligent Application
```
