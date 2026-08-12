import streamlit as st
from resume_parser import parse_resume

st.set_page_config(page_title="Resume Parser", page_icon="📄")
st.title("Resume Parser")
st.write("Turn resume text into structured information using rules and regular expressions.")

text = st.text_area("Paste resume text", height=350, placeholder="Paste a resume here...")

if st.button("Parse Resume", type="primary"):
    if not text.strip():
        st.warning("Please paste some resume text first.")
    else:
        resume = parse_resume(text)

        st.subheader("Contact")
        st.write("**Name:**", resume["name"] or "Not found")
        st.write("**Email:**", resume["email"] or "Not found")
        st.write("**Phone:**", resume["phone"] or "Not found")

        st.subheader("URLs")
        if resume["urls"]:
            for url in resume["urls"]:
                st.write(url)
        else:
            st.write("None found")

        st.subheader("Skills")
        if resume["skills"]:
            for skill in resume["skills"]:
                st.write(f"- {skill}")
        else:
            st.write("None found")

        st.subheader("Resume Sections")
        for section, items in resume["sections"].items():
            st.markdown(f"### {section.title()}")
            for item in items:
                st.write(f"- {item}")

        st.subheader("Structured Data")
        st.json(resume)
