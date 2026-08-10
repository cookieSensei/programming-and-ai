
import os
import matplotlib
matplotlib.use("Agg")


import tensorflow as tf

print("TensorFlow version:", tf.__version__)
print("GPUs:", tf.config.list_physical_devices('GPU'))


import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

os.makedirs("models", exist_ok=True)
os.makedirs("plots", exist_ok=True)

tf.keras.backend.clear_session()

from tensorflow.keras.datasets import cifar10

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

x_train = x_train / 255.0
x_test = x_test / 255.0

model = tf.keras.models.Sequential([

    tf.keras.layers.Conv2D(32,(3,3),activation="relu",input_shape=(32,32,3)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D((2,2)),

    tf.keras.layers.Conv2D(64,(3,3),activation="relu"),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D((2,2)),

    tf.keras.layers.Conv2D(128,(3,3),activation="relu"),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D((2,2)),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(128,activation="relu"),
    tf.keras.layers.Dropout(0.5),

    tf.keras.layers.Dense(10,activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    x_train,
    y_train,
    validation_split=0.2,
    epochs=10,
    batch_size=8
)

model.save("models/cifar10_cnn_model.h5")

y_pred = np.argmax(model.predict(x_test),axis=1)
y_true = y_test.flatten()

print(classification_report(y_true,y_pred))

cm = confusion_matrix(y_true,y_pred)

plt.figure(figsize=(8,6))
sns.heatmap(cm,annot=True,fmt="d")
plt.title("Confusion Matrix")
plt.savefig("plots/confusion_matrix.png")
plt.close()

plt.figure()
plt.plot(history.history["accuracy"],label="train")
plt.plot(history.history["val_accuracy"],label="val")
plt.legend()
plt.title("Accuracy Curve")
plt.savefig("plots/accuracy_curve.png")
plt.close()

print("Training complete. Model saved to models/cifar10_cnn_model.h5")
