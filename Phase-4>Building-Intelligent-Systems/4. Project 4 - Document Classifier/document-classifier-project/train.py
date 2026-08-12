import argparse
import json
import os
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

SEED = 42
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32


def parse_args():
    parser = argparse.ArgumentParser(description="Train a document classifier.")
    parser.add_argument("--dataset", default="dataset")
    parser.add_argument("--model", choices=["cnn", "vgg16"], default="cnn")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--output", default="model")
    return parser.parse_args()


def load_datasets(dataset_dir):
    dataset_dir = Path(dataset_dir)

    train_val = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.30,
        subset="training",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int",
    )

    holdout = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.30,
        subset="validation",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int",
    )

    class_names = train_val.class_names

    # Split the 30% holdout equally into validation and test.
    holdout_batches = tf.data.experimental.cardinality(holdout).numpy()
    test_batches = max(1, holdout_batches // 2)

    test_ds = holdout.take(test_batches)
    val_ds = holdout.skip(test_batches)

    return train_val, val_ds, test_ds, class_names


def build_cnn(num_classes):
    inputs = tf.keras.Input(shape=(*IMAGE_SIZE, 3))

    x = tf.keras.layers.Rescaling(1.0 / 255)(inputs)
    x = tf.keras.layers.Conv2D(32, 3, activation="relu")(x)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(64, 3, activation="relu")(x)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(128, 3, activation="relu")(x)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)

    return tf.keras.Model(inputs, outputs, name="document_cnn")


def build_vgg16(num_classes):
    base_model = tf.keras.applications.VGG16(
        include_top=False,
        weights="imagenet",
        input_shape=(*IMAGE_SIZE, 3),
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(*IMAGE_SIZE, 3))
    x = tf.keras.applications.vgg16.preprocess_input(inputs)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)

    return tf.keras.Model(inputs, outputs, name="document_vgg16")


def configure_datasets(train_ds, val_ds, test_ds):
    autotune = tf.data.AUTOTUNE
    return (
        train_ds.prefetch(autotune),
        val_ds.prefetch(autotune),
        test_ds.prefetch(autotune),
    )


def plot_history(history, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.plot(history.history["accuracy"], label="Training")
    plt.plot(history.history["val_accuracy"], label="Validation")
    plt.title("Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "accuracy.png")
    plt.close()

    plt.figure()
    plt.plot(history.history["loss"], label="Training")
    plt.plot(history.history["val_loss"], label="Validation")
    plt.title("Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "loss.png")
    plt.close()


def evaluate_model(model, test_ds, class_names, output_dir):
    y_true = []
    y_pred = []

    for images, labels in test_ds:
        predictions = model.predict(images, verbose=0)
        y_true.extend(labels.numpy().tolist())
        y_pred.extend(np.argmax(predictions, axis=1).tolist())

    print("\nClassification report:\n")
    print(
        classification_report(
            y_true,
            y_pred,
            target_names=class_names,
            zero_division=0,
        )
    )

    matrix = confusion_matrix(y_true, y_pred)

    print("Confusion matrix:")
    print(matrix)

    output_dir = Path(output_dir)
    np.savetxt(output_dir / "confusion_matrix.csv", matrix, delimiter=",", fmt="%d")

    report = classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )

    with open(output_dir / "classification_report.json", "w") as f:
        json.dump(report, f, indent=2)

    return y_true, y_pred


def main():
    args = parse_args()
    tf.random.set_seed(SEED)
    np.random.seed(SEED)

    print("Loading dataset...")
    train_ds, val_ds, test_ds, class_names = load_datasets(args.dataset)

    print("Classes:", class_names)
    print("Training model:", args.model)

    if args.model == "cnn":
        model = build_cnn(len(class_names))
    else:
        model = build_vgg16(len(class_names))

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True,
        )
    ]

    start = time.time()

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
        callbacks=callbacks,
    )

    training_seconds = time.time() - start

    Path(args.output).mkdir(parents=True, exist_ok=True)
    Path("results").mkdir(parents=True, exist_ok=True)

    model_path = Path(args.output) / "document_classifier.keras"
    model.save(model_path)

    with open(Path(args.output) / "class_names.json", "w") as f:
        json.dump(class_names, f, indent=2)

    metadata = {
        "model_type": args.model,
        "image_size": list(IMAGE_SIZE),
        "class_names": class_names,
        "training_seconds": training_seconds,
        "epochs_requested": args.epochs,
    }

    with open(Path(args.output) / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    plot_history(history, "results")

    _, test_accuracy = model.evaluate(test_ds, verbose=1)
    print(f"\nTest accuracy: {test_accuracy:.4f}")
    print(f"Training time: {training_seconds:.1f} seconds")

    evaluate_model(model, test_ds, class_names, "results")
    print(f"\nSaved model to: {model_path}")


if __name__ == "__main__":
    main()
