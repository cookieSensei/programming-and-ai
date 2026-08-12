import streamlit as st

from document_pipeline import process_resume_upload
from resume_parser import parse_resume
from job_matcher import (
    KNOWN_SKILLS,
    extract_job_skills,
    exact_skill_match,
    calculate_skill_score,
)
from similarity import (
    calculate_tfidf_similarity,
    load_embedding_model,
    calculate_embedding_similarity,
)
from resume_analysis import analyze_resume


st.set_page_config(
    page_title="Resume Intelligence",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Resume Intelligence")
st.caption(
    "An educational decision-support application combining document processing, "
    "information extraction, similarity, and ranking."
)

with st.sidebar:
    st.header("Matching Settings")
    semantic_weight = st.slider(
        "Semantic similarity weight",
        0.0,
        1.0,
        0.30,
        0.05,
    )
    tfidf_weight = st.slider(
        "TF-IDF similarity weight",
        0.0,
        1.0,
        0.20,
        0.05,
    )

    st.caption(
        "The remaining weight is used for exact skill matching. "
        "These weights are educational examples, not universal hiring rules."
    )

    use_embeddings = st.checkbox(
        "Use embeddings",
        value=True,
        help="Disable this if you want to inspect the exact + TF-IDF baseline.",
    )

resume_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "png", "jpg", "jpeg"],
)

job_text = st.text_area(
    "Job Description",
    height=260,
    placeholder="Paste the job description here...",
)

analyze_button = st.button(
    "Analyze",
    type="primary",
    use_container_width=True,
)

if analyze_button:
    if resume_file is None:
        st.error("Please upload a PDF, PNG, JPG, or JPEG resume.")
        st.stop()

    if not job_text.strip():
        st.error("Please provide a job description.")
        st.stop()

    with st.spinner("Processing resume..."):
        try:
            processed = process_resume_upload(resume_file)
        except Exception as exc:
            st.error(f"Document processing failed: {exc}")
            st.stop()

    raw_text = processed["raw_text"]
    clean_text = processed["clean_text"]

    if not clean_text.strip():
        st.error(
            "No usable text was extracted from the resume. "
            "Try a clearer scan or check OCR dependencies."
        )
        st.stop()

    resume = parse_resume(clean_text)
    analysis = analyze_resume(resume)

    job_skills = extract_job_skills(job_text, KNOWN_SKILLS)
    exact = exact_skill_match(resume["skills"], job_skills)
    skill_score = calculate_skill_score(exact, job_skills)

    tfidf_score = calculate_tfidf_similarity(clean_text, job_text)

    embedding_score = None
    if use_embeddings:
        with st.spinner("Calculating semantic similarity..."):
            try:
                model = load_embedding_model()
                embedding_score = calculate_embedding_similarity(
                    clean_text,
                    job_text,
                    model,
                )
            except Exception as exc:
                st.warning(
                    "Embedding similarity could not be calculated. "
                    f"Using the exact + TF-IDF baseline instead. Details: {exc}"
                )

    available_weights = [
        ("skill", 1.0 - tfidf_weight - semantic_weight),
        ("tfidf", tfidf_weight),
    ]

    if embedding_score is not None:
        available_weights.append(("semantic", semantic_weight))
    else:
        # Redistribute the semantic weight when embeddings are unavailable.
        available_weights = [
            ("skill", 1.0 - tfidf_weight),
            ("tfidf", tfidf_weight),
        ]

    final_score = 0.0
    for signal, weight in available_weights:
        if signal == "skill":
            final_score += weight * skill_score
        elif signal == "tfidf":
            final_score += weight * tfidf_score
        elif signal == "semantic":
            final_score += weight * embedding_score

    st.session_state["result"] = {
        "processed": processed,
        "raw_text": raw_text,
        "clean_text": clean_text,
        "resume": resume,
        "analysis": analysis,
        "job_skills": job_skills,
        "exact": exact,
        "skill_score": skill_score,
        "tfidf_score": tfidf_score,
        "embedding_score": embedding_score,
        "final_score": final_score,
    }

if "result" not in st.session_state:
    st.info("Upload a resume and add a job description, then click Analyze.")
    st.stop()

result = st.session_state["result"]

st.divider()

# ---------------- Resume Information ----------------

st.header("Resume Information")

resume = result["resume"]
analysis = result["analysis"]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Contact")
    st.write("**Name:**", resume["name"] or "Not found")
    st.write("**Email:**", resume["email"] or "Not found")
    st.write("**Phone:**", resume["phone"] or "Not found")

with col2:
    st.subheader("Resume Statistics")
    st.metric("Detected skills", analysis["skill_count"])
    st.metric("Projects", analysis["project_count"])
    st.metric("Experience entries", analysis["experience_count"])
    st.metric("Education entries", analysis["education_count"])

st.subheader("Skills")

if resume["skills"]:
    st.write(" · ".join(resume["skills"]))
else:
    st.write("No known skills detected.")

st.subheader("Resume Sections")

for section, items in resume["sections"].items():
    with st.expander(section.title()):
        if items:
            for item in items:
                st.write(f"- {item}")
        else:
            st.write("No entries detected.")

# ---------------- Job Match ----------------

st.divider()
st.header("Job Match")

score_col, skill_col, tfidf_col, semantic_col = st.columns(4)

with score_col:
    st.metric("Overall Match", f"{result['final_score']:.0%}")

with skill_col:
    st.metric("Skill Match", f"{result['skill_score']:.0%}")

with tfidf_col:
    st.metric("TF-IDF", f"{result['tfidf_score']:.2f}")

with semantic_col:
    if result["embedding_score"] is None:
        st.metric("Semantic", "Unavailable")
    else:
        st.metric("Semantic", f"{result['embedding_score']:.2f}")

matched = result["exact"]["matched"]
missing = result["exact"]["missing"]

left, right = st.columns(2)

with left:
    st.subheader("Matched Skills")
    if matched:
        for skill in matched:
            st.success(skill.title())
    else:
        st.write("No exact skill matches.")

with right:
    st.subheader("Missing Skills")
    if missing:
        for skill in missing:
            st.warning(skill.title())
    else:
        st.write("No missing skills from the known vocabulary.")

st.subheader("Job Skills Detected")

if result["job_skills"]:
    st.write(" · ".join(result["job_skills"]))
else:
    st.write("No known skills detected in the job description.")

st.info(
    "Interpretation: the score represents similarity according to the "
    "chosen matching formula. It is not a probability of candidate success "
    "and should not be treated as an automated hiring decision."
)

# ---------------- Debug / Pipeline ----------------

with st.expander("Document processing details"):
    st.write("**Detected input type:**", result["processed"]["input_type"])
    st.write("**Used OCR:**", result["processed"]["used_ocr"])
    st.write("**Raw text length:**", len(result["raw_text"]))
    st.write("**Clean text length:**", len(result["clean_text"]))

with st.expander("Raw extracted text"):
    st.text(result["raw_text"])

with st.expander("Clean text"):
    st.text(result["clean_text"])

with st.expander("Structured resume JSON"):
    st.json(result["resume"])

with st.expander("Matching formula"):
    st.code(
        "Final Score = exact skill signal + TF-IDF signal + semantic signal\n"
        "Weights are configurable in the sidebar."
    )
