
"""
IMDB Sentiment Analysis Training Script

This script performs the full pipeline:

1. Load IMDB dataset from TensorFlow
2. Preprocess sequences (padding)
3. Build neural network model
4. Train the model
5. Evaluate performance
6. Save the trained model

The script runs independently and does NOT require the notebook.
"""
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, GlobalAveragePooling1D

# -------------------------------
# 1. Load Dataset
# -------------------------------

vocab_size = 10000

(train_data, train_labels), (test_data, test_labels) = tf.keras.datasets.imdb.load_data(
    num_words=vocab_size
)

print("Training samples:", len(train_data))
print("Test samples:", len(test_data))

# -------------------------------
# 2. Preprocessing
# -------------------------------

max_length = 256

train_data = pad_sequences(
    train_data,
    value=0,
    padding="post",
    maxlen=max_length
)

test_data = pad_sequences(
    test_data,
    value=0,
    padding="post",
    maxlen=max_length
)

# -------------------------------
# 3. Build Model
# -------------------------------

model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=16),
    GlobalAveragePooling1D(),
    Dense(16, activation="relu"),
    Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# -------------------------------
# 4. Train Model
# -------------------------------

history = model.fit(
    train_data,
    train_labels,
    epochs=10,
    batch_size=512,
    validation_split=0.2
)

# -------------------------------
# 5. Evaluate Model
# -------------------------------

loss, accuracy = model.evaluate(test_data, test_labels)

print("Test Accuracy:", accuracy)

# -------------------------------
# 6. Save Model
# -------------------------------


# -------------------------------
# 6. Save Model
# -------------------------------

os.makedirs("models", exist_ok=True)

model.save("models/imdb_sentiment_model.keras")

print("Model saved successfully.")