# Tutorial 07 - Django Templates

## Why this matters

Templates are the bridge between Django/Python data and HTML.

The basic idea is:

```text
Python data
 ↓
View
 ↓
Template
 ↓
HTML
 ↓
Browser
```

## 1. Static template

A template may contain ordinary HTML:

```html
<h1>Welcome</h1>
<p>We help entrepreneurs.</p>
```

The view can render it:

```python
return render(
    request,
    "main/home.html",
)
```

## 2. Variables

View:

```python
name = "CookieSensei"

return render(
    request,
    "main/home.html",
    {"name": name},
)
```

Template:

```django
<h1>Welcome to {{ name }}</h1>
```

The `{{ }}` syntax outputs a value.

## 3. Multiple values

```python
context = {
    "name": "CookieSensei",
    "city": "Bengaluru",
}
```

Template:

```django
<h1>{{ name }}</h1>
<p>{{ city }}</p>
```

## 4. Loops

```django
{% for product in products %}
    <article>
        <h2>{{ product.name }}</h2>
        <p>₹{{ product.price }}</p>
    </article>
{% endfor %}
```

The template syntax differs from Python, but the concept is familiar.

## 5. Conditions

```django
{% if product.available %}
    <p>Available</p>
{% else %}
    <p>Unavailable</p>
{% endif %}
```

## 6. Filters

You may see:

```django
{{ name|upper }}
```

or:

```django
{{ description|truncatewords:20 }}
```

Filters transform displayed values.

You do not need to memorize them.

## 7. Template inheritance

Suppose every page has the same navigation and footer.

Instead of copying them into every template, create:

```text
base.html
```

Example:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Website{% endblock %}</title>
</head>
<body>

<nav>
    <a href="/">Home</a>
    <a href="/about/">About</a>
</nav>

<main>
    {% block content %}{% endblock %}
</main>

<footer>
    <p>My Business</p>
</footer>

</body>
</html>
```

A child template:

```django
{% extends "base.html" %}

{% block title %}About{% endblock %}

{% block content %}
<h1>About Us</h1>
<p>We help entrepreneurs.</p>
{% endblock %}
```

## 8. Why inheritance is useful

Without it:

```text
home.html   → navigation + content + footer
about.html  → navigation + content + footer
contact.html → navigation + content + footer
```

With it:

```text
base.html
 ├── navigation
 └── footer

home.html
 └── content

about.html
 └── content

contact.html
 └── content
```

Change the navigation once.

## 9. URL tags

If a URL is named:

```python
path("about/", about, name="about")
```

a template can use:

```django
<a href="{% url 'about' %}">About</a>
```

This is often preferable to hard-coding paths throughout templates.

## 10. Static files

You may see:

```django
{% load static %}
```

and:

```django
<link
    rel="stylesheet"
    href="{% static 'main/css/style.css' %}"
>
```

This connects the template to Django's static-file system.

## 11. Be careful with `safe`

You may encounter:

```django
{{ content|safe }}
```

This tells Django not to escape the content in the usual way.

If AI introduces `safe`, ask why it is necessary.

Do not use it blindly for user-generated content.

## 12. Exercise

Create:

```text
base.html
home.html
about.html
contact.html
```

Put shared navigation/footer in `base.html`.

Use `{% extends %}` and `{% block %}`.

## 13. Using ChatGPT

Ask:

> Explain how template inheritance works in this project. Identify what belongs in `base.html` and what belongs in child templates. Do not rewrite the files.

## Remember

Templates connect application data to HTML.

```text
View
 ↓
data
 ↓
template
 ↓
HTML
```

Template inheritance prevents unnecessary duplication.
