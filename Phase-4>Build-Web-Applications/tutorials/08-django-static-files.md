# Tutorial 08 — Django Static Files

## Why This Matters

Students need to understand where CSS, JavaScript, and images live in Django.

## What Are Static Files?

Static files include CSS, JavaScript, images, and fonts.

## Typical Structure

```text
main/
└── static/
    └── main/
        ├── css/style.css
        ├── js/app.js
        └── images/
```

## Using Static Files

```django
{% load static %}
<link rel="stylesheet" href="{% static 'main/css/style.css' %}">
<script src="{% static 'main/js/app.js' %}"></script>
```

For an image:

```django
<img src="{% static 'main/images/logo.png' %}" alt="Logo">
```

## Try It

Add one CSS file, one JavaScript file, and one image to a Django project.

## Debugging

If HTML works but CSS does not, check the file path, `{% load static %}`, browser developer tools, and Django static-file configuration.

## Using ChatGPT

Give ChatGPT your folder structure, template, CSS location, and exact browser error rather than simply saying “CSS doesn't work.”
