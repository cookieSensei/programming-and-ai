import re

import cv2
import pytesseract


def preprocess_image(image):
    """
    Preprocess the uploaded document image before OCR.
    """

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Increase image size
    resized = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Reduce noise
    blurred = cv2.GaussianBlur(
        resized,
        (5, 5),
        0
    )

    # Convert to black and white
    _, thresholded = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresholded


def extract_text(image):
    """
    Extract text from an image using Tesseract OCR.
    """

    text = pytesseract.image_to_string(image)

    return text


def clean_text(text):
    """
    Clean unwanted OCR characters and whitespace.
    """

    # Remove unwanted characters
    text = re.sub(
        r"[^A-Za-z0-9\s.,@+-]",
        " ",
        text
    )

    # Collapse multiple spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def process_document(image):
    """
    Run the complete document processing pipeline.
    """

    # Preprocess image
    processed_image = preprocess_image(image)

    # Extract text
    text = extract_text(processed_image)

    # Clean text
    cleaned_text = clean_text(text)

    return cleaned_text