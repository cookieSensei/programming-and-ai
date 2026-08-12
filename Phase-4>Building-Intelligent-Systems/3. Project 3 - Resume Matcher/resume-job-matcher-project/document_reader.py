def extract_text_from_upload(uploaded_file):
    """Extract text from supported uploaded files.

    TXT/MD are handled directly. PDFs use pypdf when installed.
    Image OCR belongs to the earlier Document Reader project and can
    be connected here without changing the matching engine.
    """
    filename = uploaded_file.name.lower()

    if filename.endswith((".txt", ".md")):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")

    if filename.endswith(".pdf"):
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError(
                "PDF support requires pypdf. Install the project requirements."
            ) from exc

        reader = PdfReader(uploaded_file)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    raise ValueError(f"Unsupported file type: {uploaded_file.name}")
