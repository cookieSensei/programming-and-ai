import re

KNOWN_SKILLS = {
    "python": "Python",
    "sql": "SQL",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "computer vision": "Computer Vision",
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
}

SECTION_ALIASES = {
    "skills": {
        "skills", "technical skills", "core skills",
        "technical expertise", "core competencies", "technologies",
    },
    "experience": {
        "experience", "work experience", "professional experience",
        "employment history", "professional background",
    },
    "education": {
        "education", "academic background", "academic history",
    },
    "projects": {
        "projects", "personal projects", "selected projects",
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
    for line in (x.strip() for x in text.splitlines() if x.strip()):
        if "@" in line or re.search(r"\d", line):
            continue
        if normalize_line(line) in {"resume", "curriculum vitae", "cv"}:
            continue
        return line
    return None


def extract_skills(text):
    normalized = text.lower()
    found = []

    for skill, display_name in KNOWN_SKILLS.items():
        if re.search(rf"\b{re.escape(skill)}\b", normalized):
            found.append(display_name)

    return found


def parse_sections(text):
    sections = {
        "skills": [],
        "education": [],
        "experience": [],
        "projects": [],
    }
    current = None

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        normalized = normalize_line(line)

        for section, aliases in SECTION_ALIASES.items():
            if normalized in aliases:
                current = section
                break
        else:
            if current:
                sections[current].append(line)

    return sections


def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "urls": extract_urls(text),
        "skills": extract_skills(text),
        "sections": parse_sections(text),
    }
