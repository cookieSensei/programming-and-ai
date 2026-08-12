import streamlit as st

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_tfidf_similarity(resume_text, job_text):
    """Calculate cosine similarity between the resume and job description."""
    documents = [resume_text, job_text]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
    )

    matrix = vectorizer.fit_transform(documents)

    return float(
        cosine_similarity(
            matrix[0:1],
            matrix[1:2],
        )[0][0]
    )


@st.cache_resource
def load_embedding_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")


def calculate_embedding_similarity(resume_text, job_text, model):
    embeddings = model.encode(
        [resume_text, job_text],
        normalize_embeddings=True,
    )

    return float(
        cosine_similarity(
            embeddings[0:1],
            embeddings[1:2],
        )[0][0]
    )
