import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"


@st.cache_resource
def load_embedding_model(model_name=DEFAULT_MODEL_NAME):
    return SentenceTransformer(model_name)


def calculate_embedding_skill_scores(
    resume_text,
    skill_descriptions,
    model,
):
    """Compare the resume with each skill description using embeddings."""
    if not skill_descriptions:
        return []

    skills = list(skill_descriptions.keys())
    descriptions = list(skill_descriptions.values())

    resume_embedding = model.encode(resume_text)
    skill_embeddings = model.encode(descriptions)

    scores = cosine_similarity(
        [resume_embedding],
        skill_embeddings,
    )[0]

    results = [
        {
            "skill": skill,
            "score": float(score),
        }
        for skill, score in zip(skills, scores)
    ]

    return sorted(results, key=lambda item: item["score"], reverse=True)


def calculate_pair_similarity(text_a, text_b, model):
    embeddings = model.encode([text_a, text_b])
    return float(
        cosine_similarity(
            [embeddings[0]],
            [embeddings[1]],
        )[0][0]
    )
