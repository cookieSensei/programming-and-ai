# Project 4 — Document Classifier

This project turns the computer-vision material from Phase 3 into a usable
document-classification application.

The progression is:

```text
Dataset
  ↓
Preprocessing
  ↓
CNN / Transfer Learning
  ↓
Training
  ↓
Validation
  ↓
Test Evaluation
  ↓
Saved Model
  ↓
Streamlit Application
  ↓
Uploaded Image
  ↓
Prediction
  ↓
Document Class + Scores
```

## Folder structure

All application helper code is kept beside `app.py`.

```text
document-classifier/
├── app.py
├── predictor.py
├── train.py
├── dataset/
│   ├── resume/
│   ├── invoice/
│   ├── certificate/
│   └── id/
├── model/
├── results/
├── requirements.txt
└── README.md
```

The class folders are the labels. Add your own images to them.

## 1. Inspect your dataset

Before training, ask:

- How many images do I have?
- How many classes?
- How many images per class?
- Are there duplicates?
- Are images readable?
- Is one class much larger than another?

The project is intentionally structured so students inspect the data before
training rather than treating the dataset as a black box.

## 2. Train the baseline CNN

From this project directory:

```bash
python train.py --model cnn --epochs 10
```

The script:

- loads images from `dataset/`
- creates training/validation/test splits
- resizes images to 224×224
- trains a small CNN
- saves the model
- plots training/validation curves
- evaluates the test set
- writes a confusion matrix and classification report

The saved files go into:

```text
model/
├── document_classifier.keras
├── class_names.json
└── metadata.json
```

and evaluation artifacts go into:

```text
results/
├── accuracy.png
├── loss.png
├── confusion_matrix.csv
└── classification_report.json
```

## 3. Experiment with VGG16 transfer learning

Run:

```bash
python train.py --model vgg16 --epochs 10
```

The VGG16 base is frozen initially. A new classifier is trained on top of the
pretrained visual representation.

Compare the two models using:

- validation accuracy
- test accuracy
- training time
- confusion matrix
- per-class precision/recall/F1

Do not assume VGG16 is better just because it is larger. Measure it.

## 4. Run the application

After training:

```bash
streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.enableXsrfProtection false \
  --server.enableCORS false
```

The application does NOT retrain the model.

It:

```text
Load saved model
      ↓
Upload image
      ↓
Preprocess image
      ↓
Model inference
      ↓
Display class + score
```

This separation between training and inference is intentional.

## 5. Optional fine-tuning experiment

The baseline VGG16 implementation freezes the pretrained base.

A useful next student experiment is:

```text
Train classifier
    ↓
Evaluate
    ↓
Unfreeze selected later VGG16 layers
    ↓
Use a smaller learning rate
    ↓
Fine-tune
    ↓
Evaluate again
```

Only make this change after the baseline works.

## 6. Important preprocessing rule

The preprocessing used during inference must match the preprocessing used
during training.

The baseline CNN uses:

```python
image / 255.0
```

The VGG16 model uses:

```python
tf.keras.applications.vgg16.preprocess_input(...)
```

Do not mix these pipelines.

## 7. Teaching flow

Recommended classroom sequence:

1. Inspect the dataset.
2. Visualize examples.
3. Check class balance.
4. Train the small CNN.
5. Inspect training/validation curves.
6. Evaluate on the unseen test set.
7. Inspect the confusion matrix.
8. Look at incorrect predictions.
9. Try VGG16 transfer learning.
10. Compare both models.
11. Save the chosen model.
12. Build/run the Streamlit inference app.
13. Upload a new document and inspect the prediction.

The central lesson is:

> A trained model becomes useful when we put it inside an application that
> accepts real input and produces a useful result.

## Dataset note

No training images are included in this starter project. The directory
structure is ready for the actual document dataset.

For a classroom experiment, start with the four curriculum classes:

```text
resume
invoice
certificate
id
```

and add an `other` class later if your dataset contains enough representative
examples.
