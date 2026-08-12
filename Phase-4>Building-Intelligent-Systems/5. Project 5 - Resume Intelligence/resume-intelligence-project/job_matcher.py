import re


KNOWN_SKILLS = {
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "sql": "SQL",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-learn",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "computer vision": "Computer Vision",
    "natural language processing": "Natural Language Processing",
    "opencv": "OpenCV",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "git": "Git",
    "linux": "Linux",
    "streamlit": "Streamlit",
    "next.js": "Next.js",
}


def extract_job_skills(job_text, known_skills):
    normalized = job_text.lower()
    found = []

    for skill, display_name in sorted(
        known_skills.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if re.search(
            rf"(?<!\w){re.escape(skill)}(?!\w)",
            normalized,
        ):
            found.append(display_name)

    return found


def exact_skill_match(resume_skills, job_skills):
    resume = {skill.lower() for skill in resume_skills}
    job = {skill.lower() for skill in job_skills}

    matched = sorted(resume & job)
    missing = sorted(job - resume)

    return {
        "matched": matched,
        "missing": missing,
    }


def calculate_skill_score(exact_result, job_skills):
    if not job_skills:
        return 0.0

    return len(exact_result["matched"]) / len(job_skills)
