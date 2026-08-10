import re

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


memory = [
    "CookieSensei teaches programming through practical projects.",
    "CookieSensei teaches Python and software development.",
    "CookieSensei has a curriculum divided into different phases.",
    "CookieSensei helps students learn by building real software.",
]


def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


def retrieve(query):
    documents = [" ".join(tokenize(text)) for text in memory]
    query = " ".join(tokenize(query))

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents + [query])

    similarities = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )[0]

    best_index = similarities.argmax()

    return memory[best_index]


def chatbot(message):
    return retrieve(message)


st.title("🍪 CookieBot")

st.write(
    "Ask me something about CookieSensei."
)

message = st.text_input("You:")

if message:
    response = chatbot(message)

    st.write("**CookieBot:**")
    st.write(response)