import re

# Keep the vocabulary intentionally small and inspectable for the project.
KNOWN_SKILLS = {
    "python": "Python programming, scripting, software development",
    "sql": "SQL databases, relational databases, querying data",
    "machine learning": (
        "machine learning, predictive modeling, classification, "
        "regression, supervised learning"
    ),
    "deep learning": (
        "deep learning, neural networks, CNN, transformers, "
        "representation learning"
    ),
    "computer vision": (
        "computer vision, image processing, image classification, "
        "object detection, convolutional neural networks"
    ),
    "opencv": "OpenCV, image processing, computer vision",
    "tensorflow": "TensorFlow, neural networks, machine learning",
    "pytorch": "PyTorch, deep learning, neural networks",
    "docker": "Docker, containers, containerization, deployment",
    "kubernetes": "Kubernetes, container orchestration, deployment",
    "aws": "Amazon Web Services, AWS, cloud computing, cloud infrastructure",
    "azure": "Microsoft Azure, cloud computing, cloud infrastructure",
    "gcp": "Google Cloud Platform, GCP, cloud computing",
    "git": "Git, version control, source control",
    "linux": "Linux operating system, command line, servers",
}


def _contains_phrase(text, phrase):
    return bool(re.search(rf"\b{re.escape(phrase)}\b", text.lower()))


def extract_job_requirements(job_text, known_skills):
    normalized = job_text.lower()

    required_markers = [
        "required",
        "must have",
        "requirements",
        "required qualifications",
        "qualifications",
    ]
    preferred_markers = [
        "preferred",
        "nice to have",
        "bonus",
        "desired",
        "plus",
    ]

    required = []
    preferred = []

    # First find all vocabulary skills.
    found = [
        skill
        for skill in known_skills
        if _contains_phrase(normalized, skill)
    ]

    # Use section proximity as a simple heuristic.
    required_start = min(
        [normalized.find(marker) for marker in required_markers if normalized.find(marker) >= 0]
        or [10**9]
    )
    preferred_start = min(
        [normalized.find(marker) for marker in preferred_markers if normalized.find(marker) >= 0]
        or [10**9]
    )

    for skill in found:
        position = normalized.find(skill)

        if preferred_start < required_start and position >= preferred_start:
            preferred.append(skill)
        elif required_start < 10**9 and position >= required_start:
            # If preferred appears before this occurrence, classify preferred.
            if preferred_start < position and preferred_start < required_start:
                preferred.append(skill)
            else:
                required.append(skill)
        else:
            required.append(skill)

    # Remove duplicates while preserving order.
    required = list(dict.fromkeys(required))
    preferred = [x for x in dict.fromkeys(preferred) if x not in required]

    return required, preferred


def match_exact_skills(resume_skills, job_skills):
    resume = {skill.lower() for skill in resume_skills}
    job = {skill.lower() for skill in job_skills}

    matched = resume & job
    missing = job - resume

    return {
        "matched": matched,
        "missing": missing,
    }


def _semantic_skill_map(embedding_results, threshold):
    return {
        item["skill"].lower(): item
        for item in embedding_results
        if item["score"] >= threshold
    }


def calculate_match_score(
    required_skills,
    preferred_skills,
    exact_matches,
    embedding_results,
    embedding_threshold=0.55,
    required_weight=1.0,
    preferred_weight=0.5,
    document_similarity=None,
):
    required = {skill.lower() for skill in required_skills}
    preferred = {skill.lower() for skill in preferred_skills}

    exact = {skill.lower() for skill in exact_matches["matched"]}

    semantic = _semantic_skill_map(
        embedding_results,
        embedding_threshold,
    )

    total_weight = (
        len(required) * required_weight
        + len(preferred) * preferred_weight
    )

    if total_weight == 0:
        skill_coverage = 0.0
    else:
        covered = 0.0

        for skill in required:
            if skill in exact or skill in semantic:
                covered += required_weight

        for skill in preferred:
            if skill in exact or skill in semantic:
                covered += preferred_weight

        skill_coverage = covered / total_weight

    # The project specifies a composite of:
    # 60% skill coverage + 25% semantic coverage + 15% document similarity.
    # Here skill coverage already uses accepted semantic matches, while the
    # explicit semantic component rewards non-exact semantic matches.
    semantic_only = [
        skill
        for skill in semantic
        if skill not in exact
    ]

    denominator = len(required) + len(preferred)
    semantic_coverage = (
        len(semantic_only) / denominator
        if denominator
        else 0.0
    )

    document_score = document_similarity or 0.0

    final = (
        0.60 * skill_coverage
        + 0.25 * semantic_coverage
        + 0.15 * document_score
    )

    return {
        "score": final * 100,
        "skill_coverage": skill_coverage,
        "semantic_coverage": semantic_coverage,
        "document_similarity": document_score,
    }


def build_match_report(
    resume_text,
    job_text,
    required_skills,
    preferred_skills,
    exact_matches,
    embedding_results,
    document_similarity,
    embedding_threshold,
    required_weight=1.0,
    preferred_weight=0.5,
):
    score_parts = calculate_match_score(
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        exact_matches=exact_matches,
        embedding_results=embedding_results,
        embedding_threshold=embedding_threshold,
        required_weight=required_weight,
        preferred_weight=preferred_weight,
        document_similarity=document_similarity,
    )

    exact = {skill.lower() for skill in exact_matches["matched"]}
    semantic_candidates = _semantic_skill_map(
        embedding_results,
        embedding_threshold,
    )

    semantic_matches = []
    for skill, result in semantic_candidates.items():
        if skill in exact:
            continue

        semantic_matches.append(
            {
                "job_skill": skill,
                "resume_text": "semantic relationship",
                "score": result["score"],
            }
        )

    all_job_skills = {
        skill.lower()
        for skill in required_skills + preferred_skills
    }

    missing = [
        skill
        for skill in all_job_skills
        if skill not in exact and skill not in semantic_candidates
    ]

    score = score_parts["score"]

    if score >= 80:
        category = "Strong Match"
    elif score >= 60:
        category = "Moderate Match"
    else:
        category = "Weak Match"

    return {
        **score_parts,
        "category": category,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "exact_matches": sorted(exact),
        "semantic_matches": sorted(
            semantic_matches,
            key=lambda item: item["score"],
            reverse=True,
        ),
        "missing_skills": sorted(missing),
    }
