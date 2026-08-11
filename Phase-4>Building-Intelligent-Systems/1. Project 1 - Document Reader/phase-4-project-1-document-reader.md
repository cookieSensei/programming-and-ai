# Project 1 - Build a Document Reader

## Phase 4 - Building Intelligent Systems

In the previous module, we learned how to think about an intelligent application as a pipeline.

Now we are going to build our first real Phase 4 application.

Our problem is simple:

> **Can we take a real-world document and turn it into usable text?**

A user should be able to upload an image of a document and our application should:

```text
Upload Image
     ↓
Read Image
     ↓
Preprocess Image
     ↓
OCR
     ↓
Extract Text
     ↓
Clean Text
     ↓
Display Result
```

We will build this application incrementally.

---

# 1. Why Documents Are Different

So far, most of our data has been relatively convenient.

We have worked with things such as:

```text
CSV files
DataFrames
NumPy arrays
Images
Text files
```

A document image is different.

Suppose a user gives us:

```text
resume.jpg
```

Python does not automatically know that the image contains:

```text
John Smith
Python Developer
john@example.com
```

As far as a computer vision program is concerned, the image is primarily a collection of pixels.

We need a process that converts:

```text
Pixels
   ↓
Characters
   ↓
Words
   ↓
Text
```

This is where **OCR** comes in.

---

# 2. What Is OCR?

OCR stands for:

> **Optical Character Recognition**

OCR is the process of extracting written or printed text from an image.

Conceptually:

```text
             IMAGE

┌────────────────────────┐
│                        │
│  John Smith             │
│  Python Developer       │
│  john@example.com       │
│                        │
└────────────────────────┘
            │
            │ OCR
            ▼
"John Smith
 Python Developer
 john@example.com"
```

The important thing is that OCR gives us **text**.

Once we have text, we can use techniques we already know:

```text
Regex
NLP
String processing
TF-IDF
Embeddings
Machine Learning
```

This makes OCR a bridge between:

```text
Computer Vision
        ↓
       Text
        ↓
       NLP
```

That bridge will become extremely important in the next projects.

---

# 3. The Technology Stack

For this project, our pipeline will use:

```text
Python
   ↓
OpenCV
   ↓
OCR
   ↓
Regex / Text Processing
   ↓
Streamlit
```

Each component has a different responsibility.

### Python

Controls the application.

### OpenCV

Reads and preprocesses images.

### OCR

Extracts text from images.

### Regex

Cleans predictable unwanted characters and patterns.

### Streamlit

Provides the user interface.

Notice that we are not learning these technologies from scratch.

We are **combining technologies we have already learned**.

---

# 4. The First Version

Before adding preprocessing, let's build the smallest possible OCR program.

Our first goal is:

```text
Image
 ↓
OCR
 ↓
Text
```

This gives us a baseline.

Later, we can compare:

```text
OCR without preprocessing

vs.

OCR with preprocessing
```

This is an important engineering habit.

> **Build a simple baseline before trying to improve it.**

---

# 5. Install the Python Libraries

We will use:

```bash
pip install opencv-python
pip install pytesseract
pip install pillow
```

Or:

```bash
pip install opencv-python pytesseract pillow
```

There is one additional component.

`pytesseract` is a Python interface to the **Tesseract OCR engine**.

Installing the Python package alone does not necessarily install the OCR engine itself.

Make sure Tesseract is installed on your computer and that Python can find it.

After installation, we can test the setup.

```python
import pytesseract

print(pytesseract.get_tesseract_version())
```

If this prints a Tesseract version, the OCR engine is available.

If it doesn't, fix the Tesseract installation before continuing.

---

# 6. Read an Image with OpenCV

Let's start with OpenCV.

```python
import cv2

image = cv2.imread("document.jpg")
```

We can inspect the image:

```python
print(image.shape)
```

For a color image, this might look something like:

```text
(1200, 800, 3)
```

The three values represent:

```text
height
width
channels
```

The three channels generally correspond to the color channels represented by OpenCV.

---

# 7. Display the Image

We can use OpenCV:

```python
cv2.imshow("Document", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

However, because we will eventually use Streamlit, we can also use:

```python
import streamlit as st

st.image(image)
```

For now, the important concept is:

```text
File
 ↓
cv2.imread()
 ↓
Image array
```

The image is now data that Python can manipulate.

---

# 8. Send the Image to OCR

Now import:

```python
import pytesseract
```

Then:

```python
text = pytesseract.image_to_string(image)
```

And:

```python
print(text)
```

If the document contains:

```text
John Smith
Python Developer
```

we may get:

```text
John Smith

Python Developer
```

The exact output depends on the image quality and OCR engine.

---

# 9. Our First Complete OCR Program

Let's put the pieces together.

```python
import cv2
import pytesseract


image = cv2.imread("document.jpg")

text = pytesseract.image_to_string(image)

print(text)
```

That's our first document reader.

It is small.

It may not be very accurate.

That's okay.

We now have a working baseline.

---

# 10. Why OCR Sometimes Performs Poorly

Try giving the program different images.

For example:

```text
Clear scanned document
```

versus:

```text
Blurry photograph
```

You may notice that the OCR quality changes dramatically.

Why?

Because OCR is receiving an image.

If the image contains:

- noise
- shadows
- poor contrast
- skew
- blur
- strange lighting
- tiny text

then recognizing characters becomes harder.

This gives us our next question:

> **Can we improve the image before giving it to OCR?**

Yes.

This is where OpenCV becomes useful.

---

# 11. Image Preprocessing

Our new pipeline becomes:

```text
Original Image
      ↓
Preprocessing
      ↓
OCR
      ↓
Text
```

We can perform several operations.

For example:

```text
Resize
Grayscale
Blur
Threshold
```

We don't necessarily need all of them for every document.

The correct preprocessing depends on the input.

---

# 12. Convert to Grayscale

A document usually does not require all the color information in an RGB image.

We can convert it to grayscale:

```python
gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)
```

Now instead of three color channels, we have a single intensity value per pixel.

Conceptually:

```text
Color Image
     ↓
Grayscale Image
```

This can simplify later processing.

---

# 13. Why Grayscale Helps

Imagine a black document on a white background.

The information we care about is primarily:

```text
Dark pixels
vs.
Light pixels
```

Color may not be important.

Grayscale lets us focus on brightness.

For OCR preprocessing, this can make later operations easier.

---

# 14. Resize the Image

Small text can be difficult for OCR.

We can increase the image size:

```python
scale = 2

resized = cv2.resize(
    gray,
    None,
    fx=scale,
    fy=scale,
    interpolation=cv2.INTER_CUBIC
)
```

Now:

```text
Small text
   ↓
Larger image
   ↓
OCR
```

But remember:

> Bigger does not automatically mean better.

If the original image is extremely blurry, resizing cannot magically recreate missing information.

---

# 15. Reduce Noise

Images may contain small random variations called noise.

We can use a blur operation.

For example:

```python
blurred = cv2.GaussianBlur(
    resized,
    (5, 5),
    0
)
```

The purpose is not to make the document visually beautiful.

The purpose is to make the input easier for the next processing stage.

---

# 16. Thresholding

One particularly useful operation for document images is thresholding.

The idea is to convert an image into something closer to:

```text
BLACK
and
WHITE
```

For example:

```python
_, thresholded = cv2.threshold(
    blurred,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)
```

The result might conceptually look like:

```text
Original:

gray shades
████████████████


Thresholded:

black / white
████████████████
```

This can make text boundaries easier for OCR to detect.

---

# 17. Our Preprocessing Pipeline

We now have:

```python
image = cv2.imread("document.jpg")

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
```

Then:

```python
text = pytesseract.image_to_string(
    thresholded
)
```

The complete pipeline is:

```text
Image
  ↓
Grayscale
  ↓
Resize
  ↓
Blur
  ↓
Threshold
  ↓
OCR
  ↓
Text
```

---

# 18. Compare Before and After

This is a good experiment.

Run OCR on the original image:

```python
original_text = pytesseract.image_to_string(
    image
)
```

Then run OCR on the processed image:

```python
processed_text = pytesseract.image_to_string(
    thresholded
)
```

Print both:

```python
print("ORIGINAL")
print(original_text)

print("\nPROCESSED")
print(processed_text)
```

Ask:

> Did preprocessing improve the result?

Sometimes yes.

Sometimes no.

This is important.

There is no universal preprocessing pipeline that works perfectly for every image.

---

# 19. Inspect the Intermediate Images

We should not blindly apply transformations.

Let's display:

```python
cv2.imshow("Original", image)
cv2.imshow("Grayscale", gray)
cv2.imshow("Thresholded", thresholded)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

Now we can visually inspect what each operation actually did.

This is a recurring machine learning and computer vision habit:

> **Look at your data.**

Don't assume the transformation improved it.

---

# 20. Clean the OCR Output

OCR output can contain:

```text
extra spaces
blank lines
weird symbols
```

We already learned regex.

Let's use it.

Import:

```python
import re
```

Suppose OCR gives us:

```text
Hello!!!
Name: John Smith
@@@###
Python Developer
```

We can clean unwanted characters.

For example:

```python
cleaned = re.sub(
    r"[^A-Za-z0-9\s.,@+-]",
    " ",
    text
)
```

This replaces characters outside our allowed set with spaces.

Then:

```python
cleaned = re.sub(
    r"\s+",
    " ",
    cleaned
).strip()
```

Now multiple spaces are collapsed.

The pipeline becomes:

```text
OCR
 ↓
Raw Text
 ↓
Regex Cleaning
 ↓
Cleaner Text
```

---

# 21. Why Use `re.sub()` Here?

We have previously used regex to **find** patterns.

For example:

```python
re.findall(...)
```

But now we want to **replace** unwanted characters.

That's exactly what:

```python
re.sub(...)
```

is designed for.

The pattern:

```python
r"[^A-Za-z0-9\s.,@+-]"
```

means roughly:

> Find characters that are not letters, numbers, whitespace, or the selected punctuation.

Then:

```python
re.sub(pattern, " ", text)
```

replaces those characters with a space.

This is a good example of reusing a tool we learned earlier for a new application.

---

# 22. Build the Document Reader Function

Let's now separate our processing logic into functions.

```python
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

Then:

```python
def extract_text(image):
    processed = preprocess_image(image)

    text = pytesseract.image_to_string(
        processed
    )

    return text
```

Now our application logic is easier to understand:

```text
image
 ↓
extract_text()
 ↓
text
```

---

# 23. Add Text Cleaning

We can make another function:

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

Now our complete processing pipeline becomes:

```python
def process_document(image):
    text = extract_text(image)

    text = clean_text(text)

    return text
```

This is already starting to look like an actual application component.

---

# 24. Why Functions Matter Here

Notice what we have achieved.

Instead of one large script, we now have:

```text
preprocess_image()
        ↓
extract_text()
        ↓
clean_text()
        ↓
process_document()
```

Each function has a responsibility.

If OCR doesn't work, we can investigate:

```text
extract_text()
```

If the image looks bad:

```text
preprocess_image()
```

If the text contains unwanted symbols:

```text
clean_text()
```

This is exactly the kind of separation we discussed in the previous module.

---

# 25. Build the Streamlit Interface

Now let's give the system a user interface.

Create:

```text
app.py
```

Start with:

```python
import streamlit as st

st.title("📄 Document Reader")
st.write(
    "Upload an image and extract its text."
)
```

---

# 26. Upload an Image

Streamlit provides:

```python
st.file_uploader()
```

For example:

```python
uploaded_file = st.file_uploader(
    "Upload a document image",
    type=["png", "jpg", "jpeg"]
)
```

Now the user can select an image.

---

# 27. Read the Uploaded File

We can use OpenCV and NumPy to convert the uploaded file into an image.

```python
import numpy as np
import cv2

file_bytes = np.asarray(
    bytearray(uploaded_file.read()),
    dtype=np.uint8
)

image = cv2.imdecode(
    file_bytes,
    cv2.IMREAD_COLOR
)
```

Now:

```text
Browser
  ↓
Uploaded File
  ↓
Bytes
  ↓
NumPy Array
  ↓
OpenCV Image
```

This is another example of data changing representation.

---

# 28. Display the Uploaded Image

We can show it:

```python
st.image(
    image,
    channels="BGR",
    caption="Uploaded document"
)
```

Now the user can see what they uploaded.

---

# 29. Run OCR

We can add a button:

```python
if st.button("Extract Text"):

    text = process_document(image)

    st.subheader("Extracted Text")

    st.write(text)
```

Now our application flow is:

```text
User
 ↓
Upload Image
 ↓
Click Extract Text
 ↓
OpenCV
 ↓
OCR
 ↓
Regex
 ↓
Text
 ↓
Streamlit
```

We have built our first Phase 4 application.

---

# 30. Add a Loading Indicator

OCR can take some time.

We can give the user feedback:

```python
if st.button("Extract Text"):

    with st.spinner("Reading document..."):

        text = process_document(image)

    st.subheader("Extracted Text")

    st.write(text)
```

This is a small detail, but it makes the application feel much more like software.

---

# 31. Complete Version

Our first complete `app.py` can look like this:

```python
import re

import cv2
import numpy as np
import pytesseract
import streamlit as st


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


def extract_text(image):

    processed = preprocess_image(image)

    text = pytesseract.image_to_string(
        processed
    )

    return text


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


def process_document(image):

    text = extract_text(image)

    text = clean_text(text)

    return text


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

Run it with:

```bash
streamlit run app.py
```

---

# 32. Notice the Architecture

Even though everything is currently in one file, we can already see the architecture:

```text
                STREAMLIT
                    │
                    ▼
              File Upload
                    │
                    ▼
                OpenCV
                    │
                    ▼
            Image Preprocessing
                    │
                    ▼
                  OCR
                    │
                    ▼
             Regex Cleaning
                    │
                    ▼
                  Text
```

This is exactly the pipeline we designed before writing the code.

---

# 33. Exercise - Break the Application

A good way to understand the pipeline is to deliberately change it.

Try removing preprocessing:

```python
text = pytesseract.image_to_string(
    image
)
```

Compare the result.

Then try:

```python
text = pytesseract.image_to_string(
    gray
)
```

Then:

```python
text = pytesseract.image_to_string(
    thresholded
)
```

Compare the results.

Create a small table:

```text
Input                  OCR Result

Original image         ________

Grayscale              ________

Thresholded            ________
```

Ask:

> Which preprocessing approach worked best for this document?

---

# 34. Exercise - Add a Preview

Add a section that displays the processed image.

For example:

```python
processed = preprocess_image(image)

st.subheader(
    "Processed Image"
)

st.image(
    processed,
    caption="Image sent to OCR"
)
```

Now the user can see:

```text
Original
   ↓
Processed
   ↓
OCR
```

This makes the pipeline visible.

---

# 35. Exercise - Preserve Line Structure

Our cleaning function currently collapses whitespace.

That can be useful for search, but it may destroy document structure.

For example:

```text
Skills

Python
SQL
TensorFlow
```

could become:

```text
Skills Python SQL TensorFlow
```

Experiment with a second cleaning function that preserves line breaks.

This is an important lesson:

> **Cleaning data always involves a trade-off.**

The correct representation depends on what we want to do next.

For a search engine, normalized text might be useful.

For a resume parser, preserving sections and line breaks might be extremely important.

---

# 36. Exercise - Add File Validation

What happens if the user uploads an unsupported file?

Our UI currently limits the uploader, but real applications should still validate inputs.

Think about:

```text
Is a file present?
Is the image readable?
Does OpenCV return None?
Does OCR return anything?
```

For example:

```python
if image is None:

    st.error(
        "Could not read the uploaded image."
    )
```

This is our first practical example of handling failure paths.

---

# 37. Exercise - Measure OCR Quality

Create a small set of test documents.

For each document, write the expected text manually.

Then compare:

```text
Expected Text
      vs.
OCR Text
```

Ask:

- Which documents work well?
- Which fail?
- Does preprocessing help?
- Does image resolution matter?
- Does handwriting work?
- Does a photograph work as well as a scan?

We are beginning to think about **evaluation**.

---

# 38. Exercise - Experiment With the Pipeline

Try changing:

### Resize

```python
fx=2
```

to:

```python
fx=3
```

or:

```python
fx=1.5
```

### Blur

Try different kernel sizes.

### Thresholding

Compare:

```python
cv2.THRESH_BINARY
```

with:

```python
cv2.THRESH_BINARY + cv2.THRESH_OTSU
```

Don't just change parameters randomly.

Ask:

> **What effect does this transformation have on the image?**

---

# 39. A Useful Debugging Technique

When a pipeline doesn't work, don't stare at the final output and guess.

Inspect every stage.

```text
Input
 ↓
Inspect
 ↓
Preprocessing
 ↓
Inspect
 ↓
OCR
 ↓
Inspect
 ↓
Cleaning
 ↓
Inspect
```

For example:

```python
st.image(image)

st.image(gray)

st.image(thresholded)

st.write(raw_text)

st.write(cleaned_text)
```

This lets us identify **where** the problem occurred.

Maybe:

```text
Image is fine
     ↓
Preprocessing destroyed the text
     ↓
OCR fails
```

Without inspecting the intermediate result, we might incorrectly blame OCR.

---

# 40. Git Checkpoint

Once the basic application works, create a Git checkpoint.

For example:

```bash
git status
```

Then:

```bash
git add .
```

Then:

```bash
git commit -m "Build basic document reader"
```

This gives us a checkpoint:

```text
Experiment
    ↓
Build
    ↓
Git Checkpoint
    ↓
Improve
```

This connects directly back to the developer workflow introduced earlier in the curriculum.

---

# 41. Project Structure

At this point, a simple project can look like:

```text
Document-Reader/
│
├── app.py
├── requirements.txt
└── README.md
```

Our `requirements.txt` might contain:

```text
opencv-python
pytesseract
numpy
streamlit
```

Remember that Tesseract itself is a separate system dependency from the Python package.

---

# 42. What We Have Built

We started with:

```text
Image
```

and built:

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

This is already an intelligent application.

It is not intelligent because every step uses AI.

It is intelligent because it transforms unstructured real-world input into useful information.

---

# 43. The Important Limitation

Our application currently knows how to extract text.

It doesn't really **understand** the document.

Suppose it extracts:

```text
John Smith
Python Developer
john@example.com
Skills
Python
TensorFlow
SQL
```

Our application gives us text.

But we still need to answer:

> Which part is the person's name?

> Which part is the email?

> Which words are skills?

> Where does education begin?

> Where does work experience begin?

This is the next problem.

And this leads directly to our next project.

---

# What Comes Next

Our first Phase 4 project taught us:

```text
Real-world Document
       ↓
Image Processing
       ↓
OCR
       ↓
Text
```

Now we will ask a harder question:

> **Can we turn that text into structured information?**

For example:

```text
Raw Text
   ↓
NLP / Regex
   ↓
{
    name: ...,
    email: ...,
    skills: [...],
    education: [...],
    experience: [...]
}
```

That will become:

# Project 2 - Build a Real Resume Parser

We will start with rules and regex.

Then we will progressively introduce NLP and more sophisticated information extraction.

The important progression is:

```text
Project 1

Pixels
  ↓
Text


Project 2

Text
  ↓
Information


Project 3

Information
  ↓
Matching


Final Project

Information
  ↓
Intelligent Application
```
