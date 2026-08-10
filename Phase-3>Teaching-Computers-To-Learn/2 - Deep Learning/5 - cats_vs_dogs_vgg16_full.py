#Install if required
# pip install tensorflow-datasets

# =========================================================
# 1. IMPORT LIBRARIES
# =========================================================
# Core Python + ML libraries
import os
import json

# TensorFlow + datasets
import tensorflow as tf
import tensorflow_datasets as tfds

# Visualization
import matplotlib.pyplot as plt

# Keras modules
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input



# =========================================================
# 2. GPU MEMORY SAFETY (VERY IMPORTANT 🔥)
# =========================================================
# Prevent TensorFlow from grabbing all GPU memory at once
# This avoids OOM (Out Of Memory) issues

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)



# =========================================================
# 3. CONFIGURATION
# =========================================================
# Image size for models
IMG_SIZE = (160, 160)   # smaller than 224 → saves memory

# Batch size (reduce if OOM occurs)
BATCH_SIZE = 16

# Performance optimization
AUTOTUNE = tf.data.AUTOTUNE

# Directory structure
DATA_DIR = "./datasets"
MODEL_DIR = "./saved_models"
PLOT_DIR = "./plots"

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)



# =========================================================
# 4. LOAD DATASET (TFDS handles download automatically)
# =========================================================
(train_ds, val_ds), info = tfds.load(
    'cats_vs_dogs',
    split=['train[:75%]', 'train[75%:]'],  # 75/25 split
    as_supervised=True,                   # returns (image, label)
    with_info=True,
    data_dir=DATA_DIR
)



# =========================================================
# 5. DATA AUGMENTATION (helps generalization)
# =========================================================
# Applied only during training

data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])



# =========================================================
# 6. PREPROCESSING FUNCTIONS
# =========================================================

# For CNN (simple normalization)
def preprocess_cnn(image, label):
    image = tf.image.resize(image, IMG_SIZE)
    image = image / 255.0  # normalize to [0,1]
    return image, label

# For VGG16 (special preprocessing required)
def preprocess_vgg(image, label):
    image = tf.image.resize(image, IMG_SIZE)
    image = preprocess_input(image)  # required for pretrained models
    return image, label



# =========================================================
# 7. CREATE DATA PIPELINES
# =========================================================

# CNN pipeline
train_cnn = train_ds.map(preprocess_cnn, num_parallel_calls=AUTOTUNE)
val_cnn = val_ds.map(preprocess_cnn, num_parallel_calls=AUTOTUNE)

train_cnn = train_cnn.shuffle(1000).batch(BATCH_SIZE).prefetch(AUTOTUNE)
val_cnn = val_cnn.batch(BATCH_SIZE).prefetch(AUTOTUNE)

# VGG16 pipeline
train_vgg = train_ds.map(preprocess_vgg, num_parallel_calls=AUTOTUNE)
val_vgg = val_ds.map(preprocess_vgg, num_parallel_calls=AUTOTUNE)

train_vgg = train_vgg.shuffle(1000).batch(BATCH_SIZE).prefetch(AUTOTUNE)
val_vgg = val_vgg.batch(BATCH_SIZE).prefetch(AUTOTUNE)



# =========================================================
# 8. BUILD CNN MODEL (FROM SCRATCH)
# =========================================================
def build_cnn():
    model = keras.Sequential([
        data_augmentation,

        layers.Conv2D(32, (3,3), activation='relu', input_shape=(160,160,3)),
        layers.MaxPooling2D(),

        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D(),

        layers.Conv2D(128, (3,3), activation='relu'),
        layers.MaxPooling2D(),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')  # binary classification
    ])

    return model



# =========================================================
# 9. BUILD VGG16 MODEL (TRANSFER LEARNING)
# =========================================================
def build_vgg16():

    # Load pretrained model
    base_model = VGG16(
        weights='imagenet',
        include_top=False,
        input_shape=(160,160,3)
    )

    # Freeze base model initially
    base_model.trainable = False

    # Custom classifier on top
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(1, activation='sigmoid')(x)

    model = keras.Model(inputs=base_model.input, outputs=outputs)

    return model, base_model



# =========================================================
# 10. TRAINING FUNCTION
# =========================================================
def train_model(model, train_data, val_data, name, base_model=None):

    # Compile model
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    # Initial training
    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=5
    )

    # Fine-tuning (only for VGG16)
    if base_model is not None:

        print("🔧 Fine-tuning...")

        # Unfreeze last layers
        for layer in base_model.layers[-4:]:
            layer.trainable = True

        model.compile(
            optimizer=tf.keras.optimizers.Adam(1e-5),  # lower LR
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        history_fine = model.fit(
            train_data,
            validation_data=val_data,
            epochs=5
        )

        # Merge histories
        for key in history.history:
            history.history[key] += history_fine.history[key]

    # =========================
    # SAVE MODEL + METRICS
    # =========================
    # model.save(os.path.join(MODEL_DIR, name))
    model.save(os.path.join(MODEL_DIR, name + ".h5"))

    with open(os.path.join(MODEL_DIR, name + "_history.json"), "w") as f:
        json.dump(history.history, f)

    return history

    
    
# =========================================================
# 11. TRAIN CNN MODEL
# =========================================================
print("🚀 Training CNN...")
cnn_model = build_cnn()
cnn_history = train_model(cnn_model, train_cnn, val_cnn, "cnn_model")

# Free memory before next model (VERY IMPORTANT 🔥)
del cnn_model
tf.keras.backend.clear_session()


# =========================================================
# 12. TRAIN VGG16 MODEL
# =========================================================
print("\n🚀 Training VGG16...")
vgg_model, base_model = build_vgg16()
vgg_history = train_model(vgg_model, train_vgg, val_vgg, "vgg16_model", base_model)



# =========================================================
# 13. PLOT COMPARISON
# =========================================================
def plot_comparison(cnn_hist, vgg_hist):

    plt.figure(figsize=(12,5))

    # Accuracy comparison
    plt.subplot(1,2,1)
    plt.plot(cnn_hist.history['val_accuracy'], label='CNN')
    plt.plot(vgg_hist.history['val_accuracy'], label='VGG16')
    plt.title("Validation Accuracy")
    plt.legend()

    # Loss comparison
    plt.subplot(1,2,2)
    plt.plot(cnn_hist.history['val_loss'], label='CNN')
    plt.plot(vgg_hist.history['val_loss'], label='VGG16')
    plt.title("Validation Loss")
    plt.legend()

    plt.savefig(os.path.join(PLOT_DIR, "comparison.png"))
    plt.show()

plot_comparison(cnn_history, vgg_history)