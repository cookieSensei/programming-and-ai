import re
from urllib.parse import urljoin, urlparse

import requests
import streamlit as st
from bs4 import BeautifulSoup
# Install with: pip install rank-bm25
from rank_bm25 import BM25Okapi


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


def get_relative_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    links = []

    for link in soup.find_all("a", href=True):
        href = link["href"]

        # Convert relative links such as "/curriculum"
        # into complete URLs.
        full_url = urljoin(base_url, href)

        # Only keep links belonging to CookieSensei.
        if urlparse(full_url).netloc == urlparse(WEBSITE_URL).netloc:
            links.append(full_url)

    return links


def crawl_website(start_url, max_pages=10):
    visited = set()
    urls_to_visit = [start_url]
    pages = []

    while urls_to_visit and len(visited) < max_pages:
        url = urls_to_visit.pop(0)

        if url in visited:
            continue

        visited.add(url)

        try:
            html = get_webpage(url)
        except requests.RequestException:
            continue

        pages.append({
            "url": url,
            "text": extract_text(html)
        })

        links = get_relative_links(html, url)

        for link in set(links):
            if link not in visited and link not in urls_to_visit:
                urls_to_visit.append(link)

    return pages


def clean_text(text):
    # Replace anything that is not a word character or whitespace
    # with a space. This removes icons and other symbols while
    # keeping words separated.
    text = re.sub(r"[^\w\s]", " ", text)

    # Remove extra whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()


def build_memory():
    pages = crawl_website(
        WEBSITE_URL,
        max_pages=10
    )

    memory = []

    for page in pages:
        # Split each webpage into sentences.
        sentences = re.split(
            r"(?<=[.!?])\s+",
            page["text"]
        )

        for sentence in sentences:
            sentence = clean_text(sentence)

            if len(sentence.split()) >= 5:
                memory.append({
                    "text": sentence,
                    "url": page["url"]
                })

    return memory


@st.cache_data
def load_memory():
    return build_memory()


def tokenize(text):
    return clean_text(text).split()


def retrieve(query, memory):
    documents = [
        tokenize(item["text"])
        for item in memory
    ]

    query_tokens = tokenize(query)

    # BM25 is a ranking algorithm designed for information retrieval.
    # It considers term frequency, how rare a word is across documents,
    # and the length of each document.
    bm25 = BM25Okapi(documents)

    scores = bm25.get_scores(query_tokens)

    best_index = scores.argmax()

    return memory[best_index], scores[best_index]


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
    f"from CookieSensei and its internal pages."
)

message = st.text_input("You:")

if message:
    response, score = chatbot(message, memory)

    st.write("**CookieBot:**")
    st.write(response["text"])

    st.caption(
        f"Source: {response['url']} | Similarity: {score:.2f}"
    )
