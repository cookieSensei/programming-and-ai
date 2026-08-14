# Tutorial 02 - HTML Basics

## Why this matters

You will often ask ChatGPT to create web pages. That is encouraged.

But you should be able to look at generated HTML and answer:

- Where is the heading?
- Where is navigation?
- Where is the button?
- Where is the form?
- Which class controls styling?
- Where should I make my change?

## 1. A basic HTML document

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
</head>
<body>
    <h1>Welcome</h1>
    <p>This is my website.</p>
</body>
</html>
```

The `head` contains document information. The `body` contains the visible page.

## 2. Headings

```html
<h1>Main heading</h1>
<h2>Section heading</h2>
<h3>Subsection</h3>
```

Use headings to describe structure. Do not choose them only because they look large; CSS controls appearance.

## 3. Paragraphs

```html
<p>We help entrepreneurs build minimum working products.</p>
```

## 4. Links

```html
<a href="/about/">About us</a>
```

`href` tells the browser where the link goes.

## 5. Images

```html
<img
    src="/static/images/logo.png"
    alt="Company logo"
>
```

`src` identifies the image. `alt` describes it.

## 6. Lists

```html
<ul>
    <li>Consulting</li>
    <li>Training</li>
    <li>Support</li>
</ul>
```

Ordered lists use `ol`.

## 7. Containers

You will frequently see:

```html
<div>...</div>
```

You will also see semantic containers:

```html
<header>...</header>
<nav>...</nav>
<main>...</main>
<section>...</section>
<article>...</article>
<footer>...</footer>
```

You do not need to memorize every element. Recognize that they structure content.

## 8. Classes and IDs

```html
<button class="primary-button" id="book-button">
    Book Now
</button>
```

A `class` is commonly used by CSS and JavaScript. An `id` identifies a particular element.

## 9. Forms

```html
<form method="post">
    <label for="name">Name</label>

    <input
        type="text"
        id="name"
        name="name"
    >

    <button type="submit">Submit</button>
</form>
```

The `name` attribute is especially important because submitted data is associated with that name.

## 10. Common inputs

```html
<input type="text">
<input type="email">
<input type="password">
<input type="date">
<input type="number">
```

You can also use:

```html
<textarea name="message"></textarea>
<select name="service">
    <option value="consulting">Consulting</option>
</select>
```

## 11. Django templates

A Django template can contain normal HTML plus Django syntax:

```django
<h1>{{ business.name }}</h1>
```

`{{ business.name }}` means "insert this value."

You may also see:

```django
{% if user.is_authenticated %}
    <p>Welcome!</p>
{% endif %}
```

## 12. Template loops

```django
{% for product in products %}
    <h2>{{ product.name }}</h2>
{% endfor %}
```

The syntax differs from Python, but the programming idea is familiar.

## 13. Exercise

Create a page with:

- header
- navigation
- main heading
- two paragraphs
- image
- list
- call-to-action
- contact form

Then identify each HTML element.

## 14. Reading AI-generated HTML

If ChatGPT gives you:

```html
<section class="hero">
    <h1>Build Your Business</h1>
    <p>Launch your idea online.</p>
    <a href="/contact/" class="button">Get Started</a>
</section>
```

you should be able to identify:

```text
section
 ↓
heading
 ↓
paragraph
 ↓
link styled as a button
```

## 15. Using ChatGPT

Ask:

> Here is my Django template. Explain its HTML structure and tell me which elements I should change to modify the heading, navigation, and button. Do not rewrite unrelated parts.

## Remember

Know how to recognize:

```text
h1 h2 h3
p
a
img
ul ol li
div
section
nav
form
label
input
textarea
select
button
class
id
```

You do not need to memorize HTML. You need to be able to read and modify it.
