def analyze_resume(resume):
    sections = resume.get("sections", {})

    return {
        "skill_count": len(resume.get("skills", [])),
        "project_count": len(sections.get("projects", [])),
        "experience_count": len(sections.get("experience", [])),
        "education_count": len(sections.get("education", [])),
        "certification_count": len(sections.get("certifications", [])),
    }
