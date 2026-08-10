# Streamlit - Build a Web UI with Python

So far, we've been running Python programs from the terminal.

For example:

```bash
python app.py
```

But what if we want other people to interact with our Python program through a webpage?

This is where **Streamlit** comes in.

Streamlit lets us turn a normal Python script into an interactive web application.

The important idea is:

> **We write Python. Streamlit turns it into a web interface.**

---

# 1. Install Streamlit

Install Streamlit using `pip`:

```bash
pip install streamlit
```

We can check that it was installed:

```bash
streamlit --version
```

---

# 2. Our First Streamlit App

Create a file called:

```text
app.py
```

Put this inside:

```python
import streamlit as st

st.title("My First App")
```

Now instead of running:

```bash
python app.py
```

we run:

```bash
streamlit run app.py
```

Streamlit will start a local web server and open our application in the browser.

You should see:

```text
My First App
```

Congratulations - we just turned a Python file into a webpage.

---

# 3. Writing Text

We can display text using:

```python
st.write("Hello, world!")
```

For example:

```python
import streamlit as st

st.title("My First App")

st.write("Hello, world!")
st.write("I am learning Streamlit.")
```

Streamlit takes these Python instructions and displays the results in the browser.

---

# 4. Titles and Headings

We can create a title:

```python
st.title("CookieBot")
```

We can create a heading:

```python
st.header("About CookieBot")
```

And a smaller subheading:

```python
st.subheader("Ask a question")
```

For example:

```python
import streamlit as st

st.title("🍪 CookieBot")

st.header("About")

st.write(
    "CookieBot can answer questions about CookieSensei."
)
```

---

# 5. Markdown

Streamlit also understands Markdown.

We can use:

```python
st.markdown("## About CookieBot")
```

We can even write multiple lines:

```python
st.markdown("""
## CookieBot

CookieBot searches information from CookieSensei.

- It reads webpages
- It stores text as memory
- It searches that memory
""")
```

This is useful because Markdown gives us more control over how our text is displayed.

---

# 6. Getting Input from the User

Our chatbot needs to receive a question.

Streamlit provides:

```python
st.text_input()
```

For example:

```python
message = st.text_input("You:")

st.write(message)
```

Now the user can type something into the webpage.

If they enter:

```text
What is CookieSensei?
```

then:

```python
message
```

contains:

```text
What is CookieSensei?
```

We can think of this as:

```text
User types something
        ↓
text_input()
        ↓
Python variable
        ↓
Our program
```

---

# 7. Using the Input

We can use the input just like any other Python variable.

```python
import streamlit as st

st.title("CookieBot")

message = st.text_input("You:")

if message:
    st.write("You said:")
    st.write(message)
```

The `if message:` checks whether the user actually entered something.

If they did, we display it.

---

# 8. Connecting Streamlit to a Function

This is where Streamlit becomes useful for our chatbot.

Suppose we have:

```python
def chatbot(message):
    return "Hello! I am CookieBot."
```

We can connect it to our UI:

```python
import streamlit as st


def chatbot(message):
    return "Hello! I am CookieBot."


st.title("🍪 CookieBot")

message = st.text_input("You:")

if message:
    response = chatbot(message)

    st.write("**CookieBot:**")
    st.write(response)
```

Now the flow is:

```text
User
 ↓
text_input()
 ↓
message
 ↓
chatbot(message)
 ↓
response
 ↓
st.write()
 ↓
Browser
```

Notice that the chatbot function doesn't know anything about Streamlit.

It simply receives text and returns text.

This separation will become important as our application gets bigger.

---

# 9. Buttons

We can also create buttons:

```python
if st.button("Say Hello"):
    st.write("Hello!")
```

For example:

```python
import streamlit as st

st.title("My App")

if st.button("Click me"):
    st.write("You clicked the button!")
```

Buttons are useful when we want the user to explicitly trigger an action.

---

# 10. Text Areas

`st.text_input()` is useful for short pieces of text.

For longer text, we can use:

```python
st.text_area()
```

For example:

```python
question = st.text_area(
    "Ask a question:"
)
```

This gives the user a larger box for entering text.

For our chatbot, a normal `text_input()` is enough for now.

---

# 11. Showing Python Data

Streamlit can display Python objects too.

For example:

```python
memory = [
    "CookieSensei teaches Python.",
    "CookieSensei teaches through projects.",
    "CookieSensei has multiple curriculum phases."
]

st.write(memory)
```

We can also display a dictionary:

```python
page = {
    "title": "Curriculum",
    "url": "https://cookiesensei.com/curriculum"
}

st.write(page)
```

This is particularly useful while developing.

If we're not sure what our program contains, we can temporarily do:

```python
st.write(memory)
```

and inspect it directly in the browser.

---

# 12. Showing Code

We can display code using:

```python
st.code("""
def hello():
    print("Hello!")
""")
```

This is useful when building educational applications or debugging our program.

---

# 13. Spinners

Some operations take time.

Our chatbot needs to crawl CookieSensei before it can answer questions.

We don't want the user staring at a blank screen.

Streamlit gives us:

```python
with st.spinner("Loading..."):
    # long-running operation
    ...
```

For example:

```python
with st.spinner("Reading CookieSensei..."):
    memory = load_memory()
```

While Python is working, Streamlit displays:

```text
Reading CookieSensei...
```

When the operation finishes, the spinner disappears.

---

# 14. Caching

There is an important problem with Streamlit.

Streamlit reruns our Python script whenever the user interacts with the application.

Imagine that our program does this:

```python
memory = crawl_website("https://cookiesensei.com")
```

Every time the user enters a question, we might crawl the website again.

We don't want that.

We can tell Streamlit to cache the result:

```python
@st.cache_data
def load_memory():
    return build_memory()
```

Then:

```python
memory = load_memory()
```

The first time `load_memory()` runs, Streamlit performs the work.

After that, Streamlit can reuse the cached result.

The basic idea is:

```text
First run:

load_memory()
     ↓
crawl website
     ↓
build memory
     ↓
cache result


Later runs:

load_memory()
     ↓
use cached result
```

This is especially useful for our chatbot.

---

# 15. A Small Example

Let's combine what we've learned.

```python
import streamlit as st


def chatbot(message):
    if message.lower() == "hello":
        return "Hello!"

    return "I don't understand that yet."


st.title("🍪 CookieBot")

st.write(
    "Ask CookieBot a question."
)

message = st.text_input("You:")

if message:

    response = chatbot(message)

    st.write("**CookieBot:**")

    st.write(response)
```

We now have a complete interactive web application.

---

# 16. Connecting Our Real Chatbot

Our actual chatbot already has a retrieval function:

```python
def retrieve(query, memory):
    ...
```

And a chatbot function:

```python
def chatbot(message, memory):
    return retrieve(message, memory)
```

Streamlit becomes the interface around those functions.

Conceptually:

```text
                 STREAMLIT
                     │
          ┌──────────┴──────────┐
          │                     │
       User Input           Display Output
          │                     ▲
          ▼                     │
       message                  │
          │                     │
          ▼                     │
       chatbot() ───────────────┘
          │
          ▼
      retrieve()
          │
          ▼
       MEMORY
```

The Streamlit UI is therefore **not the chatbot itself**.

It is the interface through which the user interacts with the chatbot.

---

# 17. Our CookieBot Application

Our current application follows this structure:

```python
import streamlit as st


st.title("🍪 CookieBot")

st.write(
    "Ask me something about CookieSensei."
)

with st.spinner("Reading CookieSensei..."):
    memory = load_memory()

message = st.text_input("You:")

if message:

    response, score = chatbot(
        message,
        memory
    )

    st.write("**CookieBot:**")

    st.write(response["text"])

    st.caption(
        f"Source: {response['url']} | "
        f"Similarity: {score:.2f}"
    )
```

The important thing is that the UI code is relatively small.

Most of the interesting work happens elsewhere:

```text
             CookieSensei
                  ↓
             Web Crawler
                  ↓
                Memory
                  ↓
               Search
                  ↓
              Chatbot
                  ↓
             Streamlit UI
```

---

# 18. The Streamlit Mental Model

You don't need to memorize every Streamlit function.

For now, remember these:

| Streamlit         | Purpose                            |
| ----------------- | ---------------------------------- |
| `st.title()`      | Page title                         |
| `st.header()`     | Heading                            |
| `st.write()`      | Display content                    |
| `st.markdown()`   | Display Markdown                   |
| `st.text_input()` | Get text from user                 |
| `st.text_area()`  | Get longer text                    |
| `st.button()`     | Create a button                    |
| `st.code()`       | Display code                       |
| `st.spinner()`    | Show progress while something runs |
| `st.cache_data`   | Cache expensive results            |

The core pattern is:

```text
Python
  ↓
Streamlit functions
  ↓
Web interface
```

---

# 19. Your Challenge

Create a Streamlit application called:

```text
app.py
```

It should:

1. Display the title **CookieBot**
2. Explain what the chatbot does
3. Have a text input for the user's question
4. Pass the question to a Python function
5. Display the response
6. Display the source URL
7. Display a loading spinner while the memory is being loaded

Once that works, try changing the interface.

Add:

* a subtitle
* a description
* an emoji
* a button
* Markdown
* a section showing how many pieces of information are in memory

The goal isn't to memorize Streamlit.

The goal is to understand:

> **Streamlit lets us take the Python programs we build and give them an interface that other people can use.**
