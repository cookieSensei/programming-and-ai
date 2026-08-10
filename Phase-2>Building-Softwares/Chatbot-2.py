import re

import requests
import streamlit as st
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


WEBSITE_URL = "https://cookiesensei.com"


def get_webpage(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.text


def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove elements that don't contain useful page content.
    for element in soup(["script", "style", "nav", "footer"]):
        element.decompose()

    text = soup.get_text(" ", strip=True)

    return text


def build_memory():
    html = get_webpage(WEBSITE_URL)
    text = extract_text(html)

    # Split the webpage into sentences.
    sentences = re.split(r"(?<=[.!?])\s+", text)

    # Keep reasonably useful sentences as our chatbot's memory.
    memory = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) >= 5
    ]

    return memory


@st.cache_data
def load_memory():
    return build_memory()


def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


def retrieve(query, memory):
    documents = [
        " ".join(tokenize(text))
        for text in memory
    ]

    query = " ".join(tokenize(query))

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        documents + [query]
    )

    similarities = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )[0]

    best_index = similarities.argmax()

    return memory[best_index]


def chatbot(message, memory):
    return retrieve(message, memory)


st.title("🍪 CookieBot")

st.write(
    "Ask me something about CookieSensei."
)

with st.spinner("Reading CookieSensei..."):
    memory = load_memory()

st.caption(
    f"CookieBot currently remembers {len(memory)} pieces of information "
    f"from {WEBSITE_URL}"
)

message = st.text_input("You:")

if message:
    response = chatbot(message, memory)

    st.write("**CookieBot:**")
    st.write(response)