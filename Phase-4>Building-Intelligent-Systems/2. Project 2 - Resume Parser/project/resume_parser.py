import re

KNOWN_SKILLS = {
    "python": "Python",
    "sql": "SQL",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "tensorflow": "TensorFlow",
    "keras": "Keras",
    "pytorch": "PyTorch",
    "opencv": "OpenCV",
    "docker": "Docker",
    "git": "Git",
    "linux": "Linux",
    "aws": "AWS",
    "scikit-learn": "Scikit-learn",
}

SECTION_ALIASES = {
    "skills": {"skills", "technical skills", "core skills", "technical expertise", "core competencies", "technologies"},
    "experience": {"experience", "work experience", "professional experience", "employment history", "professional background"},
    "education": {"education", "academic background", "academic history"},
    "projects": {"projects", "personal projects", "selected projects"},
}

IGNORED_HEADINGS = {"resume", "curriculum vitae", "cv"}


def normalize_line(line):
    return line.strip().lower().rstrip(":")


def extract_email(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    matches = re.findall(pattern, text)
    return matches[0] if matches else None


def extract_phone(text):
    pattern = r"(?:\+?\d[\d\s().-]{7,}\d)"
    matches = re.findall(pattern, text)
    return matches[0].strip() if matches else None


def extract_urls(text):
    return re.findall(r"https?://[^\s]+", text)


def extract_name(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        normalized = normalize_line(line)
        if normalized in IGNORED_HEADINGS or "@" in line or re.search(r"\d", line):
            continue
        return line
    return None


def extract_skills(text):
    normalized_text = text.lower()
    found_skills = []
    for skill, display_name in KNOWN_SKILLS.items():
        pattern = rf"\b{re.escape(skill)}\b"
        if re.search(pattern, normalized_text):
            found_skills.append(display_name)
    return found_skills


def parse_sections(text):
    sections = {"skills": [], "education": [], "experience": [], "projects": []}
    current_section = None

    for line in text.splitlines():
        original_line = line.strip()
        if not original_line:
            continue

        normalized = normalize_line(original_line)
        matched_section = next(
            (section for section, aliases in SECTION_ALIASES.items() if normalized in aliases),
            None,
        )

        if matched_section:
            current_section = matched_section
            continue

        if current_section:
            sections[current_section].append(original_line)

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
