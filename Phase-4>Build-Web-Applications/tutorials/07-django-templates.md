# Tutorial 07 — Django Templates

## Why This Matters

Templates connect Django data with HTML.

## Variables

```django
<h1>Welcome, {{ name }}</h1>
```

If the view supplies `name`, Django inserts its value.

## Loops

```django
{% for product in products %}
    <h2>{{ product.name }}</h2>
    <p>{{ product.price }}</p>
{% endfor %}
```

This should feel similar to Python's `for` loop.

## Conditions

```django
{% if product.available %}
    <p>Available</p>
{% else %}
    <p>Unavailable</p>
{% endif %}
```

## Template Inheritance

A common structure is:

```text
base.html
   ↓
home.html
about.html
contact.html
```

A child can use:

```django
{% extends "base.html" %}
{% block content %}
...
{% endblock %}
```

## Remember

```text
Python data → Django view → Template → HTML
```

## Using ChatGPT

Ask: **“Explain the Django template tags in this file using Python concepts where possible.”**
