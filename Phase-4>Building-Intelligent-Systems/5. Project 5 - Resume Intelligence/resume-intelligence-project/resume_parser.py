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
    "keras": "Keras",
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


SECTION_ALIASES = {
    "skills": {
        "skills",
        "technical skills",
        "core skills",
        "technical expertise",
        "core competencies",
        "technologies",
    },
    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "professional background",
    },
    "education": {
        "education",
        "academic background",
        "academic history",
    },
    "projects": {
        "projects",
        "personal projects",
        "selected projects",
    },
    "certifications": {
        "certifications",
        "certificates",
        "licenses and certifications",
    },
}


def normalize_line(line):
    return line.strip().lower().rstrip(":")


def extract_email(text):
    matches = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )
    return matches[0] if matches else None


def extract_phone(text):
    matches = re.findall(r"(?:\+?\d[\d\s().-]{7,}\d)", text)
    return matches[0].strip() if matches else None


def extract_urls(text):
    return re.findall(r"https?://[^\s]+", text)


def extract_name(text):
    ignored = {
        "resume",
        "curriculum vitae",
        "cv",
        "professional resume",
    }

    for line in (x.strip() for x in text.splitlines() if x.strip()):
        normalized = normalize_line(line)

        if normalized in ignored:
            continue

        if "@" in line or re.search(r"\d", line):
            continue

        if len(line.split()) > 6:
            continue

        return line

    return None


def extract_skills(text):
    normalized = text.lower()
    found = []

    # Longer phrases first to reduce partial-match confusion.
    skills = sorted(
        KNOWN_SKILLS.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    for skill, display_name in skills:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        if re.search(pattern, normalized):
            found.append(display_name)

    return found


def parse_sections(text):
    sections = {
        "skills": [],
        "education": [],
        "experience": [],
        "projects": [],
        "certifications": [],
    }

    current = None

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        normalized = normalize_line(line)

        matched = None
        for section, aliases in SECTION_ALIASES.items():
            if normalized in aliases:
                matched = section
                break

        if matched:
            current = matched
            continue

        if current:
            sections[current].append(line)

    return sections


def parse_resume(text):
    return {
        "contact": {
            "email": extract_email(text),
            "phone": extract_phone(text),
            "urls": extract_urls(text),
        },
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "urls": extract_urls(text),
        "skills": extract_skills(text),
        "sections": parse_sections(text),
    }
