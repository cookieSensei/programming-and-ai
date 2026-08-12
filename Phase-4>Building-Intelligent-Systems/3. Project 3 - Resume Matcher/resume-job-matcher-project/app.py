import streamlit as st

from document_reader import extract_text_from_upload
from resume_parser import parse_resume
from semantic_matcher import (
    DEFAULT_MODEL_NAME,
    load_embedding_model,
    calculate_embedding_skill_scores,
)
from tfidf_matcher import calculate_tfidf_skill_scores
from job_matcher import (
    KNOWN_SKILLS,
    extract_job_requirements,
    match_exact_skills,
    calculate_match_score,
    build_match_report,
)

st.set_page_config(page_title="Resume ↔ Job Matcher", page_icon="🎯", layout="wide")

st.title("Resume ↔ Job Matching")
st.caption("Decision-support signal — not an automated hiring decision.")

st.sidebar.header("Matching Settings")
embedding_threshold = st.sidebar.slider(
    "Embedding similarity threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.55,
    step=0.01,
)
required_weight = st.sidebar.number_input(
    "Required skill weight",
    min_value=0.1,
    value=1.0,
    step=0.1,
)
preferred_weight = st.sidebar.number_input(
    "Preferred skill weight",
    min_value=0.1,
    value=0.5,
    step=0.1,
)

resume_file = st.file_uploader(
    "Upload resume",
    type=["txt", "md", "pdf"],
)

resume_text_input = st.text_area(
    "Or paste resume text",
    height=250,
    placeholder="Paste resume text here...",
)

job_text = st.text_area(
    "Job description",
    height=300,
    placeholder="Paste the job description here...",
)

run = st.button("Analyze Match", type="primary", use_container_width=True)

if run:
    if resume_file is not None:
        resume_text = extract_text_from_upload(resume_file)
    else:
        resume_text = resume_text_input

    if not resume_text.strip():
        st.error("Please upload a resume or paste resume text.")
        st.stop()

    if not job_text.strip():
        st.error("Please provide a job description.")
        st.stop()

    # 1. Existing rule-based parser
    resume = parse_resume(resume_text)
    resume_skills = {skill.lower() for skill in resume["skills"]}

    # 2. Extract job requirements using the same vocabulary
    required_skills, preferred_skills = extract_job_requirements(
        job_text,
        KNOWN_SKILLS,
    )

    job_skills = required_skills + preferred_skills

    # 3. Exact matching
    exact = match_exact_skills(resume_skills, job_skills)

    # 4. TF-IDF semantic-ish matching
    tfidf_results = calculate_tfidf_skill_scores(
        resume_text,
        job_skills,
    )

    # 5. Embedding matching
    with st.spinner("Loading embedding model and calculating semantic matches..."):
        model = load_embedding_model(DEFAULT_MODEL_NAME)
        skill_descriptions = {
        skill: KNOWN_SKILLS[skill]
        for skill in job_skills
    }

    embedding_results = calculate_embedding_skill_scores(
        resume_text,
        skill_descriptions,
        model,
    )

    # 6. Final score/report
    from semantic_matcher import calculate_pair_similarity

    document_similarity = calculate_pair_similarity(
        resume_text,
        job_text,
        model,
    )

    report = build_match_report(
        resume_text=resume_text,
        job_text=job_text,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        exact_matches=exact,
        embedding_results=embedding_results,
        document_similarity=document_similarity,
        embedding_threshold=embedding_threshold,
        required_weight=float(required_weight),
        preferred_weight=float(preferred_weight),
    )

    # 7. UI
    st.divider()

    score_col, category_col = st.columns(2)
    with score_col:
        st.metric("Match Score", f"{report['score']:.0f}%")
    with category_col:
        st.metric("Match Category", report["category"])

    st.subheader("Skill Analysis")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Exact Matches")
        if exact["matched"]:
            for skill in exact["matched"]:
                st.success(skill.title())
        else:
            st.write("None")

    with c2:
        st.markdown("### Semantic Matches")
        semantic_matches = report["semantic_matches"]
        if semantic_matches:
            for item in semantic_matches:
                st.write(
                    f"**{item['job_skill'].title()}** ← "
                    f"{item['resume_text']} "
                    f"({item['score']:.2f})"
                )
        else:
            st.write("None above threshold")

    with c3:
        st.markdown("### Potential Gaps")
        if report["missing_skills"]:
            for skill in report["missing_skills"]:
                st.warning(skill.title())
        else:
            st.write("No obvious gaps")

    st.subheader("TF-IDF vs Embeddings")

    comparison = []
    tfidf_by_skill = {
        item["skill"].lower(): item["score"]
        for item in tfidf_results
    }
    embedding_by_skill = {
        item["skill"].lower(): item["score"]
        for item in embedding_results
    }

    for skill in job_skills:
        key = skill.lower()
        comparison.append(
            {
                "Skill": skill.title(),
                "Exact": "✓" if key in exact["matched"] else "",
                "TF-IDF": round(tfidf_by_skill.get(key, 0.0), 3),
                "Embedding": round(embedding_by_skill.get(key, 0.0), 3),
            }
        )

    st.dataframe(comparison, use_container_width=True, hide_index=True)

    with st.expander("Structured resume data"):
        st.json(resume)

    with st.expander("Raw match report"):
        st.json(report)
