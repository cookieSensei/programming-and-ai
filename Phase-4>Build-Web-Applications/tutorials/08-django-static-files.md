# Tutorial 08 — Django Static Files

## Why this matters

A web application contains more than Python and HTML.

You will use:

```text
CSS
JavaScript
Images
Fonts
```

Django calls these static files.

## 1. What is a static file?

Examples:

```text
style.css
app.js
logo.png
hero.jpg
favicon.ico
```

They are generally served as files rather than generated dynamically for every request.

## 2. A common structure

A Django app may contain:

```text
main/
├── static/
│   └── main/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── app.js
│       └── images/
│           └── logo.png
├── templates/
│   └── main/
│       └── home.html
├── views.py
└── models.py
```

The exact organization can vary.

## 3. Loading CSS

At the top of a template:

```django
{% load static %}
```

Then:

```django
<link
    rel="stylesheet"
    href="{% static 'main/css/style.css' %}"
>
```

## 4. Loading JavaScript

```django
<script
    src="{% static 'main/js/app.js' %}">
</script>
```

## 5. Loading images

```django
<img
    src="{% static 'main/images/logo.png' %}"
    alt="Company logo"
>
```

## 6. Why use `{% static %}`?

You could write a URL manually, but Django's static system provides a consistent way to locate these assets across environments.

The important habit is:

> Use Django's static-file mechanism instead of guessing file URLs.

## 7. When CSS does not load

If:

```text
HTML works
CSS does not
```

check:

1. Does the CSS file exist?
2. Is `{% load static %}` present?
3. Is the path correct?
4. Does the browser request the file?
5. Is the response successful?

Open:

```text
Developer Tools → Network
```

Reload the page and find the CSS request.

## 8. When JavaScript does not work

Check:

- file exists
- path is correct
- script is included
- browser console
- JavaScript execution order
- element IDs/selectors

## 9. Images

If an image is missing:

```text
image exists
 ↓
correct static location
 ↓
correct template path
 ↓
browser request succeeds
```

Do not immediately replace the image.

First check the path.

## 10. Development vs production

During development, Django can serve static files in a development setup.

Production requires deliberate static-file configuration.

You will later encounter:

```bash
python manage.py collectstatic
```

This gathers static files for deployment.

## 11. Browser developer tools

Learn these three areas:

```text
Elements
Network
Console
```

You do not need the entire browser toolkit.

You need to answer:

> Did the browser actually receive the file?

## 12. Exercise

Add all three to a Django project:

```text
style.css
app.js
logo.png
```

Load each from a template.

Then intentionally break one path and use developer tools to diagnose it.

## 13. Using ChatGPT

Instead of:

> CSS doesn't work.

Give:

- project structure
- template
- static-file path
- browser error

Ask:

> Trace the static-file path from my template to the CSS file and identify where it breaks.

## Remember

```text
HTML
 ↓
references CSS / JS / images
 ↓
Django static system
 ↓
browser
```

When a file is missing, inspect the path before rewriting the code.
