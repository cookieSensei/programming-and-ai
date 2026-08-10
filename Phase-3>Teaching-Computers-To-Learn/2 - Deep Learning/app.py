import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from PIL import Image

# =========================
# CONFIG
# =========================
MODEL_PATH = "saved_models/vgg16_model.h5"   # change if needed
IMG_SIZE = (160, 160)

# =========================
# LOAD MODEL (cached)
# =========================
@st.cache_resource
def load_my_model():
    model = load_model(MODEL_PATH)
    return model

model = load_my_model()

# =========================
# PREPROCESS FUNCTION
# =========================
def preprocess_image(img):
    img = img.resize(IMG_SIZE)
    img_array = np.array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# =========================
# UI
# =========================
st.title("🐶🐱 Dog vs Cat Classifier")
st.write("Upload an image and the model will predict whether it's a cat or a dog.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# =========================
# PREDICTION
# =========================
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Predict"):
        with st.spinner("Analyzing image..."):

            img_array = preprocess_image(image)
            prediction = model.predict(img_array)[0][0]

            if prediction > 0.5:
                label = "Dog 🐶"
            else:
                label = "Cat 🐱"

            st.success(f"Prediction: {label}")
            st.write(f"Confidence: {float(prediction):.4f}")