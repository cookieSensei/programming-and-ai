from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_tfidf_skill_scores(resume_text, job_skills):
    """Rank job skills by TF-IDF similarity to the resume."""
    if not job_skills:
        return []

    documents = [resume_text] + list(job_skills)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)

    scores = cosine_similarity(vectors[0], vectors[1:])[0]

    results = [
        {
            "skill": skill,
            "score": float(score),
        }
        for skill, score in zip(job_skills, scores)
    ]

    return sorted(results, key=lambda item: item["score"], reverse=True)
