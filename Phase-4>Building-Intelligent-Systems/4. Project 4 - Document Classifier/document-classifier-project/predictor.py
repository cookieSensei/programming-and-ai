import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image


class DocumentPredictor:
    def __init__(self, model_dir="model"):
        model_dir = Path(model_dir)

        model_path = model_dir / "document_classifier.keras"
        metadata_path = model_dir / "metadata.json"

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Train the model first with train.py."
            )

        if not metadata_path.exists():
            raise FileNotFoundError(
                f"Metadata not found at {metadata_path}."
            )

        self.model = tf.keras.models.load_model(model_path)

        with open(metadata_path) as f:
            self.metadata = json.load(f)

        self.class_names = self.metadata["class_names"]
        self.image_size = tuple(self.metadata["image_size"])
        self.model_type = self.metadata["model_type"]

    def preprocess(self, image):
        image = image.convert("RGB")
        image = image.resize(self.image_size)
        array = np.asarray(image, dtype=np.float32)

        if self.model_type == "cnn":
            array = array / 255.0
        else:
            array = tf.keras.applications.vgg16.preprocess_input(array)

        return np.expand_dims(array, axis=0)

    def predict(self, image):
        processed = self.preprocess(image)
        scores = self.model.predict(processed, verbose=0)[0]

        predicted_index = int(np.argmax(scores))

        return {
            "class": self.class_names[predicted_index],
            "score": float(scores[predicted_index]),
            "scores": {
                name: float(score)
                for name, score in zip(self.class_names, scores)
            },
        }
