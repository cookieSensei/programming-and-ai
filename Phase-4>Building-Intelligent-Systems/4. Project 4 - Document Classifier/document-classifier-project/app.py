import streamlit as st
from PIL import Image

from predictor import DocumentPredictor


st.set_page_config(
    page_title="Document Classifier",
    page_icon="📄",
)

st.title("Document Classifier")
st.write(
    "Upload a document image and let the trained computer-vision model "
    "predict its document type."
)

uploaded_file = st.file_uploader(
    "Upload a document image",
    type=["jpg", "jpeg", "png"],
)

@st.cache_resource
def load_predictor():
    return DocumentPredictor("model")


if uploaded_file is None:
    st.info("Upload a document image to begin.")
    st.stop()

try:
    image = Image.open(uploaded_file)
except Exception:
    st.error("The uploaded file could not be read as an image.")
    st.stop()

st.image(image, caption="Uploaded document", use_container_width=True)

try:
    predictor = load_predictor()
    result = predictor.predict(image)
except FileNotFoundError as exc:
    st.error(str(exc))
    st.info("Run train.py first to create the model.")
    st.stop()
except Exception as exc:
    st.error(f"Prediction failed: {exc}")
    st.stop()

st.divider()

st.subheader("Prediction")
st.metric(
    "Document Class",
    result["class"].title(),
)

st.metric(
    "Prediction Score",
    f"{result['score']:.1%}",
)

st.subheader("All Class Scores")

for class_name, score in sorted(
    result["scores"].items(),
    key=lambda item: item[1],
    reverse=True,
):
    st.write(f"**{class_name.title()}** — {score:.1%}")
    st.progress(score)

st.caption(
    "The prediction score is the model output for the predicted class. "
    "It should not automatically be interpreted as a calibrated probability."
)
