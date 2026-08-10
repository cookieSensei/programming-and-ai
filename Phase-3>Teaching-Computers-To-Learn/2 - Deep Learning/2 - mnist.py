import os
import matplotlib
matplotlib.use("Agg")  # needed for headless environments like Coder

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns

# ======================================================
# Create directories
# ======================================================

os.makedirs("models", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# ======================================================
# Load dataset
# ======================================================

(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()

# ======================================================
# Normalize pixel values
# ======================================================

X_train = X_train / 255.0
X_test = X_test / 255.0

# ======================================================
# One-hot encode labels
# ======================================================

y_train = tf.keras.utils.to_categorical(y_train)
y_test = tf.keras.utils.to_categorical(y_test)

# ======================================================
# Build model
# ======================================================

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(256, activation="relu"),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(256, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax")
])

# ======================================================
# Compile model
# ======================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.005),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ======================================================
# Train model
# ======================================================

history = model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    epochs=20,
    batch_size=32
)

# ======================================================
# Save model (.h5 format)
# ======================================================

model_path = "models/mnist_model.h5"
model.save(model_path)

print(f"\nModel saved at: {model_path}")

# ======================================================
# Load saved model
# ======================================================

loaded_model = tf.keras.models.load_model(model_path)

print("Model loaded successfully\n")

# ======================================================
# Predictions
# ======================================================

y_pred = np.argmax(loaded_model.predict(X_test), axis=1)
y_true = np.argmax(y_test, axis=1)

# ======================================================
# Metrics
# ======================================================

accuracy = accuracy_score(y_true, y_pred)

print("Test Accuracy:", accuracy)
print("\nClassification Report:\n")
print(classification_report(y_true, y_pred))

# ======================================================
# Confusion Matrix
# ======================================================

cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")

plt.savefig("plots/confusion_matrix.png")
plt.close()

print("Confusion matrix saved to plots/confusion_matrix.png")

# ======================================================
# Training Accuracy Plot
# ======================================================

plt.figure()

plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")

plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Training vs Validation Accuracy")
plt.legend()

plt.savefig("plots/accuracy_curve.png")
plt.close()

print("Accuracy plot saved to plots/accuracy_curve.png")

# ======================================================
# Training Loss Plot
# ======================================================

plt.figure()

plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training vs Validation Loss")
plt.legend()

plt.savefig("plots/loss_curve.png")
plt.close()

print("Loss plot saved to plots/loss_curve.png")

print("\nTraining pipeline finished successfully.")