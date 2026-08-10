"""
IMDB Sentiment Model Analysis Script

This script:
1. Loads the trained sentiment model
2. Loads the IMDB dataset
3. Applies the same preprocessing
4. Generates predictions
5. Evaluates performance
6. Analyzes misclassified reviews
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.preprocessing.sequence import pad_sequences


# -------------------------------
# 1. Load Model
# -------------------------------

print("Loading model...")

model = tf.keras.models.load_model(
    "./models/imdb_sentiment_model.keras",
    compile=False,
    safe_mode=False
)

model.summary()


# -------------------------------
# 2. Load Dataset
# -------------------------------

print("\nLoading IMDB dataset...")

vocab_size = 10000

(train_data, train_labels), (test_data, test_labels) = tf.keras.datasets.imdb.load_data(
    num_words=vocab_size
)

print("Test samples:", len(test_data))


# -------------------------------
# 3. Apply Same Preprocessing
# -------------------------------

max_length = 256

test_data = pad_sequences(
    test_data,
    value=0,
    padding="post",
    maxlen=max_length
)


# -------------------------------
# 4. Generate Predictions
# -------------------------------

print("\nGenerating predictions...")

predictions = model.predict(test_data)

pred_labels = (predictions > 0.5).astype(int).flatten()


# -------------------------------
# 5. Evaluation Metrics
# -------------------------------

print("\nClassification Report:\n")

print(classification_report(test_labels, pred_labels))


# -------------------------------
# 6. Confusion Matrix
# -------------------------------

cm = confusion_matrix(test_labels, pred_labels)

plt.figure(figsize=(6,5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Negative", "Positive"],
    yticklabels=["Negative", "Positive"]
)

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.show()


# -------------------------------
# 7. Prediction Confidence
# -------------------------------

plt.hist(predictions, bins=50)

plt.title("Prediction Confidence Distribution")
plt.xlabel("Probability of Positive Review")
plt.ylabel("Frequency")

plt.show()


# -------------------------------
# 8. Decode Reviews
# -------------------------------

word_index = tf.keras.datasets.imdb.get_word_index()

reverse_word_index = {value + 3: key for key, value in word_index.items()}

reverse_word_index[0] = "<PAD>"
reverse_word_index[1] = "<START>"
reverse_word_index[2] = "<UNK>"
reverse_word_index[3] = "<UNUSED>"


def decode_review(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])


# -------------------------------
# 9. Misclassified Reviews
# -------------------------------

misclassified = np.where(pred_labels != test_labels)[0]

print("\nTotal misclassified:", len(misclassified))


print("\nShowing 5 misclassified reviews:\n")

for i in misclassified[:5]:

    print("Actual:", test_labels[i])
    print("Predicted:", pred_labels[i])
    print("Confidence:", predictions[i][0])

    print("\nReview text:\n")

    print(decode_review(test_data[i]))

    print("\n" + "-"*80 + "\n")