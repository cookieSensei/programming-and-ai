# Project 4 — Document Classifier

## From Understanding Images to Building an Intelligent Application

So far in Phase 4, we have worked with documents primarily as sources of text.

We built:

```text
Document
   ↓
Text
   ↓
Information
```

and then:

```text
Resume
   ↓
Skills
   ↓
Matching
```

Now we approach documents from a different direction.

Instead of asking:

> What text is inside this document?

we ask:

> **What kind of document is this?**

This introduces a different kind of intelligent application:

```text
Image
   ↓
Computer Vision Model
   ↓
Classification
   ↓
Prediction
```

---

# 1. The Problem

Imagine a system receives many documents:

```text
Resume
Invoice
Certificate
ID Card
Form
Other
```

A human can often recognize the document type immediately.

We want a computer to learn this task.

For example:

```text
Input:
[image of an invoice]

        ↓

Model

        ↓

Prediction:
Invoice
```

This is a **classification problem**.

---

# 2. Classification

In classification, we have a finite set of categories.

For example:

```text
Class 0 → Resume
Class 1 → Invoice
Class 2 → Certificate
Class 3 → ID
```

The model receives an image and predicts one of these classes.

Conceptually:

```text
Image
  ↓
Neural Network
  ↓
Class probabilities
  ↓
Highest score
  ↓
Predicted class
```

---

# 3. What We Already Know

This project should not re-teach CNN theory from the beginning.

That was already covered in the deep learning and computer vision material.

We already know that CNNs can learn visual patterns such as:

```text
Edges
 ↓
Shapes
 ↓
Textures
 ↓
Higher-level patterns
```

Now we use that knowledge inside an application.

---

# 4. The Application Pipeline

Our application follows:

```text
Training Dataset
       ↓
Preprocessing
       ↓
CNN / Transfer Learning
       ↓
Training
       ↓
Evaluation
       ↓
Saved Model
       ↓
Streamlit Application
       ↓
Uploaded Image
       ↓
Preprocessing
       ↓
Model Prediction
       ↓
Document Class
```

Notice the transition between:

```text
Training
```

and:

```text
Application inference
```

They are different stages.

---

# 5. Training vs Inference

During training:

```text
Image
 +
Correct Label
      ↓
    Model
      ↓
    Learn
```

During inference:

```text
New Image
      ↓
Trained Model
      ↓
Prediction
```

The user should not need to retrain the model every time they upload an image.

The model has already learned.

---

# 6. Dataset

We need examples of every document type.

For example:

```text
dataset/
│
├── resume/
│   ├── resume_01.png
│   ├── resume_02.png
│   └── ...
│
├── invoice/
│   ├── invoice_01.png
│   ├── invoice_02.png
│   └── ...
│
├── certificate/
│   ├── certificate_01.png
│   ├── certificate_02.png
│   └── ...
│
└── id/
    ├── id_01.png
    ├── id_02.png
    └── ...
```

The directory structure can represent the labels.

---

# 7. Image + Label

The model needs examples of:

```text
Image
+
Correct label
```

For example:

```text
invoice_01.png → invoice
resume_04.png  → resume
```

The model learns patterns from these examples.

---

# 8. Inspect the Dataset

Before training, inspect the data.

Ask:

```text
How many images?

How many classes?

How many examples per class?

Are the images readable?

Are there duplicates?

Are some classes much larger than others?
```

This is where our EDA habits continue into computer vision.

---

# 9. Visualize the Data

Display a few examples from every class.

For example:

```python
plt.imshow(image)
plt.title("Invoice")
plt.axis("off")
plt.show()
```

Always inspect the images before trusting the dataset.

---

# 10. Class Balance

Suppose:

```text
Resume       1000
Invoice       950
Certificate  100
ID             80
```

The dataset is imbalanced.

A model may become very good at predicting:

```text
Resume
Invoice
```

while performing poorly on:

```text
Certificate
ID
```

So we inspect the class distribution before training.

---

# 11. Train / Validation / Test

Split the dataset into:

```text
Training
Validation
Test
```

Conceptually:

```text
Dataset
   │
   ├── Training
   ├── Validation
   └── Test
```

### Training

Used to learn model parameters.

### Validation

Used while developing the model.

### Test

Used for final evaluation.

---

# 12. Why Not Train on Everything?

Suppose we train on:

```text
100% of the images
```

and evaluate on:

```text
the same images
```

A high score does not tell us whether the model can recognize new documents.

We want to know:

> Can the model generalize?

That is why we keep unseen data.

---

# 13. Image Preprocessing

Neural networks expect consistent input.

For example:

```text
160 × 160 × 3
```

An image can be resized:

```python
image = tf.image.resize(
    image,
    (160, 160)
)
```

We may also normalize pixel values:

```python
image = image / 255.0
```

The exact preprocessing must match the model being used.

---

# 14. CNN Baseline

We can begin with a simple CNN.

Conceptually:

```text
Input
 ↓
Conv2D
 ↓
MaxPooling
 ↓
Conv2D
 ↓
MaxPooling
 ↓
Conv2D
 ↓
Flatten
 ↓
Dense
 ↓
Output
```

The final layer depends on the number of classes.

For four classes, we need four output scores.

---

# 15. Multi-Class Classification

Suppose:

```text
0 → Resume
1 → Invoice
2 → Certificate
3 → ID
```

The model might output:

```text
[
    0.02,
    0.91,
    0.04,
    0.03
]
```

The largest value is:

```text
0.91
```

which corresponds to:

```text
Invoice
```

---

# 16. Softmax

For multi-class classification, we commonly use:

```python
activation="softmax"
```

The output represents a distribution across classes.

For example:

```text
Resume       0.02
Invoice      0.91
Certificate  0.04
ID           0.03
```

The values sum approximately to:

```text
1.0
```

---

# 17. Train the CNN

A basic model can be compiled with:

```python
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)
```

Then:

```python
history = model.fit(
    train_data,
    validation_data=validation_data,
    epochs=...
)
```

The important concept is:

```text
Training data
      ↓
Model
      ↓
Loss
      ↓
Backpropagation
      ↓
Updated weights
```

---

# 18. Watch Training and Validation

Suppose we see:

```text
Training accuracy:   99%
Validation accuracy: 72%
```

This may indicate:

```text
Overfitting
```

The model has learned the training data much better than unseen examples.

Training and validation curves help us notice this.

---

# 19. Training Curves

Plot:

```text
Training accuracy
Validation accuracy
```

and:

```text
Training loss
Validation loss
```

For example:

```python
plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])
plt.show()
```

The visualization helps us understand how training progressed.

---

# 20. Transfer Learning

Our CNN is a useful baseline.

Now we can experiment with a pretrained model such as:

```text
VGG16
```

Instead of learning all visual features from random initialization, we start with a model that already learned general visual patterns.

This is:

> **Transfer learning.**

---

# 21. Transfer Learning Concept

Instead of:

```text
Random weights
      ↓
Learn everything
```

we start with:

```text
Pretrained model
      ↓
Existing visual features
      ↓
Adapt to our document classes
```

The pretrained model was not trained specifically on our document dataset.

We are transferring useful knowledge.

---

# 22. Freeze the Base Model

Initially:

```python
base_model.trainable = False
```

Then add our classifier:

```text
VGG16
  ↓
Feature representation
  ↓
GlobalAveragePooling
  ↓
Dense
  ↓
Output classes
```

We train the new classifier first.

---

# 23. Why Freeze the Base?

If we immediately update every pretrained layer:

```text
Many parameters
      ↓
More difficult training
      ↓
Potentially damaging useful pretrained features
```

Freezing the base allows us to first learn how our document classes map onto the existing visual representation.

---

# 24. Fine-Tuning

After the classifier works, we can optionally unfreeze some later layers.

Conceptually:

```text
Pretrained model
       ↓
Freeze
       ↓
Train classifier
       ↓
Unfreeze selected layers
       ↓
Fine-tune
```

Fine-tuning should normally use a small learning rate.

This connects directly to the transfer-learning material already covered earlier.

---

# 25. Compare the Models

Now we have an experiment:

```text
Model A:
CNN from scratch

Model B:
VGG16 transfer learning
```

Compare:

```text
Validation accuracy
Test accuracy
Training time
Prediction speed
```

Do not assume that the larger model is automatically better.

Measure it.

---

# 26. Test Set Evaluation

After choosing an approach:

```python
test_loss, test_accuracy = model.evaluate(
    test_data
)
```

This gives a final estimate on unseen examples.

---

# 27. Accuracy Is Not the Whole Story

Suppose:

```text
Accuracy = 95%
```

That sounds good.

But perhaps:

```text
Resume       98%
Invoice      97%
Certificate  80%
ID           70%
```

Overall accuracy hides the weakness of some classes.

So inspect per-class metrics.

---

# 28. Confusion Matrix

A confusion matrix shows which classes are being confused.

For example:

```text
              Predicted
             R   I   C   ID

Actual R     90  5   3   2
       I      2 92   4   2
       C      8  5  80   7
       ID     3  4   6  87
```

This can reveal that:

```text
Certificate
```

is frequently mistaken for:

```text
Resume
```

---

# 29. Classification Report

Use:

```python
from sklearn.metrics import classification_report

print(
    classification_report(
        y_true,
        y_pred,
        target_names=class_names
    )
)
```

This gives:

```text
Precision
Recall
F1-score
Support
```

for each class.

---

# 30. Look at Wrong Predictions

Metrics tell us:

```text
How often?
```

Images can help us understand:

```text
Why?
```

Display incorrect predictions:

```text
Actual:
Certificate

Predicted:
Resume
```

Then inspect the image.

Maybe:

```text
The document was blurry.
```

Maybe:

```text
The layout resembles a resume.
```

Maybe:

```text
The dataset contains confusing examples.
```

This is error analysis.

---

# 31. Save the Model

Once training is finished:

```python
model.save(
    "document_classifier.keras"
)
```

Now the application can load the trained model without retraining it.

---

# 32. Separate Training From Inference

Use two conceptual programs:

```text
train.py
```

and:

```text
app.py
```

### `train.py`

```text
Dataset
 ↓
Preprocessing
 ↓
Training
 ↓
Evaluation
 ↓
Save model
```

### `app.py`

```text
Load model
 ↓
Upload image
 ↓
Preprocess
 ↓
Predict
 ↓
Display result
```

This separation is an important application concept.

---

# 33. Build the Streamlit App

Start simply:

```python
import streamlit as st

st.title(
    "Document Classifier"
)
```

Then:

```python
uploaded_file = st.file_uploader(
    "Upload a document image",
    type=["jpg", "jpeg", "png"]
)
```

---

# 34. Display the Uploaded Image

```python
from PIL import Image

image = Image.open(
    uploaded_file
)

st.image(
    image,
    caption="Uploaded document"
)
```

The user should be able to see what the model is processing.

---

# 35. Preprocess for Inference

The model needs the same relevant preprocessing used during training.

Conceptually:

```text
Uploaded Image
      ↓
Resize
      ↓
Normalize / Model preprocessing
      ↓
Batch dimension
      ↓
Model
```

A common mistake is training with one preprocessing pipeline and predicting with another.

---

# 36. Prediction

Conceptually:

```python
prediction = model.predict(
    processed_image
)

predicted_index = prediction.argmax()

predicted_class = class_names[
    predicted_index
]
```

The application can display:

```text
Prediction: Invoice
```

---

# 37. Display the Prediction Score

We can display the largest model output:

```text
Prediction:
Invoice

Score:
91%
```

For this introductory application, call this a:

```text
Prediction score
```

rather than automatically treating it as a calibrated probability.

---

# 38. Show All Class Scores

A better interface can display:

```text
Invoice       91%
Resume         4%
Certificate    3%
ID             2%
```

This gives us a more informative result and helps us inspect ambiguous predictions.

---

# 39. Handle Basic Errors

The application should handle:

```text
No file
Unsupported format
Corrupt image
Model loading failure
```

For example:

```python
if uploaded_file is None:
    st.info(
        "Upload a document image to begin."
    )
```

The application should fail gracefully.

---

# 40. Complete Application Architecture

We now have:

```text
                     DATASET
                        │
                        ▼
                 PREPROCESSING
                        │
                        ▼
              TRAIN / VALIDATE
                        │
                        ▼
                 CNN / VGG16
                        │
                        ▼
                    EVALUATE
                        │
                        ▼
                  SAVE MODEL
                        │
                        ▼
              ┌──────────────────┐
              │   STREAMLIT APP  │
              └────────┬─────────┘
                       │
                 Upload Image
                       │
                       ▼
                  PREPROCESS
                       │
                       ▼
                    MODEL
                       │
                       ▼
                  PREDICTION
                       │
                       ▼
                CLASS + SCORE
                       │
                       ▼
                      USER
```

This is our first complete computer-vision intelligent application.

---

# 41. What Makes This Different From Phase 3?

In Phase 3, we focused primarily on:

```text
How does a CNN learn?
How does transfer learning work?
How do we evaluate a classifier?
```

Now we focus on:

```text
How do we turn that model into a usable program?
```

The model is only one component.

```text
Model
+
Preprocessing
+
Inference
+
Interface
```

creates the application.

---

# 42. Project Structure

A simple project can look like:

```text
document-classifier/
│
├── dataset/
│
├── train.py
├── app.py
├── model/
│   └── document_classifier.keras
│
├── requirements.txt
└── README.md
```

We do not need a complicated architecture.

This is an introductory project.

---

# 43. Optional Refactoring

Once the basic version works, inference can be separated:

```text
document-classifier/
│
├── train.py
├── predictor.py
├── app.py
└── model/
```

Then:

```python
from predictor import predict_document
```

The Streamlit application becomes cleaner.

But first:

> Make the simple version work.

Then refactor.

---

# 44. Suggested Experiment

Compare:

```text
CNN from scratch
```

against:

```text
VGG16 transfer learning
```

Record:

```text
Model
Validation Accuracy
Test Accuracy
Training Time
```

For example:

```text
| Model | Validation | Test | Training Time |
|---|---:|---:|---:|
| CNN | ... | ... | ... |
| VGG16 | ... | ... | ... |
```

The actual values should come from your experiment.

---

# 45. Student Challenge

Once the basic classifier works, try:

```text
1. Better preprocessing
2. Data augmentation
3. Transfer learning
4. Fine-tuning
5. Confusion matrix
6. Incorrect prediction visualization
7. Better Streamlit interface
```

Each meaningful change should be evaluated.

---

# 46. Don't Add Complexity Without a Reason

Instead of:

```text
"Let's use VGG16 because it is bigger."
```

think:

> "Our CNN is overfitting and validation performance is poor, so let's experiment with transfer learning."

The engineering decision should come from an observed problem.

---

# 47. Final Exercise

At the end of this project, you should be able to:

```text
Train a document classifier
        ↓
Evaluate it
        ↓
Save the model
        ↓
Load the model
        ↓
Accept a new image
        ↓
Run inference
        ↓
Display the prediction
```

You should understand every step.

---

# 48. Questions Before Moving On

Answer these:

```text
1. What is classification?

2. Why do we need separate training and test data?

3. What does a CNN learn from images?

4. What is transfer learning?

5. Why might VGG16 perform better than a small CNN?

6. What is the difference between training and inference?

7. Why must preprocessing be consistent?

8. What does a confusion matrix tell us?

9. Why isn't accuracy always enough?

10. How does Streamlit turn the model into an application?
```

If you can answer these questions and run the application, you are ready for Project 5.

---

# 49. Takeaway

We have moved from:

```text
IMAGE
```

to:

```text
IMAGE
 ↓
NEURAL NETWORK
 ↓
PREDICTION
```

and finally to:

```text
USER
 ↓
UPLOAD IMAGE
 ↓
STREAMLIT
 ↓
PREPROCESSING
 ↓
TRAINED MODEL
 ↓
PREDICTION
 ↓
RESULT
```

That is the important transition.

> **A trained model becomes useful when we put it inside an application that accepts real input and produces a useful result.**

Next:

# Project 5 — Resume Intelligence
