import cv2
import numpy as np
import streamlit as st

from document_reader import (
    clean_text,
    extract_text,
    preprocess_image,
)


# -----------------------------
# Streamlit Page
# -----------------------------

st.set_page_config(
    page_title="Document Reader",
    page_icon="📄"
)

st.title("📄 Document Reader")

st.write(
    "Upload a document image and extract its text."
)


# -----------------------------
# File Upload
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload document",
    type=["png", "jpg", "jpeg"]
)


# -----------------------------
# Process Uploaded Image
# -----------------------------

if uploaded_file is not None:

    # Convert uploaded file to bytes
    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    # Convert bytes into OpenCV image
    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    # Validate image
    if image is None:

        st.error(
            "Could not read the uploaded image."
        )

        st.stop()

    # Display original image
    st.subheader("Original Image")

    st.image(
        image,
        channels="BGR",
        caption="Uploaded document"
    )


    # -----------------------------
    # Extract Text Button
    # -----------------------------

    if st.button("Extract Text"):

        with st.spinner(
            "Reading document..."
        ):

            # Preprocess image
            processed_image = preprocess_image(
                image
            )

            # Extract raw OCR text
            raw_text = extract_text(
                processed_image
            )

            # Clean OCR text
            cleaned_text = clean_text(
                raw_text
            )


        # -----------------------------
        # Show Processed Image
        # -----------------------------

        st.subheader(
            "Processed Image"
        )

        st.image(
            processed_image,
            caption="Image sent to OCR"
        )


        # -----------------------------
        # Show Extracted Text
        # -----------------------------

        st.subheader(
            "Extracted Text"
        )

        st.text_area(
            "OCR Result",
            cleaned_text,
            height=300
        )


        # -----------------------------
        # Show Raw OCR
        # -----------------------------

        with st.expander(
            "Show Raw OCR Output"
        ):

            st.text(
                raw_text
            )