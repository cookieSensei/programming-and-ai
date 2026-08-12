import io
import re

import numpy as np
from PIL import Image


def clean_text(text):
    """Clean OCR/text-extraction noise while preserving useful content."""
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def preprocess_for_ocr(image):
    """Basic OpenCV preprocessing for scanned resumes."""
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError(
            "OpenCV is required for OCR preprocessing."
        ) from exc

    array = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)

    # Preserve enough resolution for OCR while avoiding extreme image sizes.
    height, width = gray.shape
    if width < 1600:
        scale = 1600 / width
        gray = cv2.resize(
            gray,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_CUBIC,
        )

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    thresholded = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )

    return Image.fromarray(thresholded)


def ocr_image(image):
    try:
        import pytesseract
    except ImportError as exc:
        raise RuntimeError(
            "pytesseract is required for OCR. Install it in the Cloud Lab."
        ) from exc

    processed = preprocess_for_ocr(image)
    return pytesseract.image_to_string(processed)


def extract_pdf_text(file_bytes):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("pypdf is required for PDF text extraction.") from exc

    reader = PdfReader(io.BytesIO(file_bytes))
    pages = []

    for page in reader.pages:
        pages.append(page.extract_text() or "")

    return "\n".join(pages)


def pdf_to_images(file_bytes):
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError(
            "PyMuPDF is required to OCR scanned PDFs."
        ) from exc

    document = fitz.open(stream=file_bytes, filetype="pdf")
    images = []

    for page in document:
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        image = Image.open(io.BytesIO(pixmap.tobytes("png"))).convert("RGB")
        images.append(image)

    return images


def process_resume_upload(uploaded_file):
    """Return raw/clean text and document-processing metadata."""
    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    if filename.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        raw_text = ocr_image(image)

        return {
            "input_type": "image",
            "used_ocr": True,
            "raw_text": raw_text,
            "clean_text": clean_text(raw_text),
        }

    if filename.endswith(".pdf"):
        extracted = extract_pdf_text(file_bytes)

        # Heuristic: a scanned PDF may technically contain a PDF object but
        # have little/no useful extracted text.
        if len(extracted.strip()) >= 80:
            return {
                "input_type": "text PDF",
                "used_ocr": False,
                "raw_text": extracted,
                "clean_text": clean_text(extracted),
            }

        pages = pdf_to_images(file_bytes)
        ocr_pages = [ocr_image(image) for image in pages]
        raw_text = "\n".join(ocr_pages)

        return {
            "input_type": "scanned PDF",
            "used_ocr": True,
            "raw_text": raw_text,
            "clean_text": clean_text(raw_text),
        }

    raise ValueError(
        "Unsupported file format. Use PDF, PNG, JPG, or JPEG."
    )
