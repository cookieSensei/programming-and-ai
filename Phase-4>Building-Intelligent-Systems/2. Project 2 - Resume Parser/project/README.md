# Project 2 — Resume Parser

All helper functions/modules intentionally live in the same folder as `app.py`.

```text
resume-parser/
├── app.py
├── resume_parser.py
├── evaluation_data.py
├── evaluate_parser.py
└── README.md
```

Run the UI:

```bash
streamlit run app.py
```

Run the evaluation:

```bash
python evaluate_parser.py
```

The curriculum's intended pipeline is:

Resume → Document Reader → Raw Text → Resume Parser → Structured Data.

When Project 1's `document_reader.py` is available, keep it in this same folder and import its `process_document` function from `app.py`. The uploaded Project 2 materials do not contain the Project 1 implementation, so this starter does not invent it.
