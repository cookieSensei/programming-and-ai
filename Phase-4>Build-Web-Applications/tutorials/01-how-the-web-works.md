# Tutorial 01 - How the Web Works

## Why this matters

You are learning to build websites, not become a networking engineer. You only need a useful mental model for what happens when someone opens a website.

The most important idea is:

> A browser sends a request. A server receives it and sends back a response.

## 1. The basic flow

When someone visits:

```text
https://example.com/about/
```

a simplified flow is:

```text
Browser
   ↓ request
Internet
   ↓
Web server / application
   ↓
Response
   ↓
Browser
```

The browser asks for a resource. The server processes the request and sends something back.

## 2. What is a URL?

A URL is an address.

```text
https://example.com/about/
│       │           │
│       │           └── route/resource
│       └────────────── website
└────────────────────── protocol
```

In Django, a route such as `/about/` can be connected to a Python view.

```python
path("about/", about)
```

This means:

> When this URL is requested, call the `about` view.

## 3. HTML

HTML describes page structure.

```html
<h1>Welcome</h1>
<p>We help entrepreneurs build websites.</p>
```

The browser interprets the elements and displays them.

## 4. CSS

CSS controls appearance.

```css
h1 {
    font-size: 48px;
}
```

Think:

```text
HTML → structure
CSS  → appearance
```

## 5. JavaScript

JavaScript adds browser-side behavior.

```text
User clicks button
        ↓
JavaScript runs
        ↓
Page changes
```

You will learn only enough JavaScript to recognize and make small interactive changes.

## 6. Where Django fits

Django is a Python web framework that normally runs on the server.

A simplified Django request looks like:

```text
Browser
   ↓
GET /about/
   ↓
Django URL configuration
   ↓
View
   ↓
Application logic / database
   ↓
Template
   ↓
HTML response
   ↓
Browser
```

Django is not HTML. Python/Django runs on the server; HTML is ultimately delivered to the browser.

## 7. Static vs dynamic pages

A static page may always contain:

```html
<h1>Welcome</h1>
```

A Django page can be dynamic:

```python
return render(
    request,
    "products.html",
    {"products": products},
)
```

The template can display current application data.

```text
Database
   ↓
Django
   ↓
Template
   ↓
HTML
   ↓
Browser
```

## 8. What you do not need yet

You do not need to memorize DNS, TCP/IP, HTTP headers, TLS, browser rendering engines, or reverse proxies.

When you encounter these later, learn what role they play.

## 9. Exercise

Open a Phase 4 Django project and choose one URL.

Find:

1. its URL pattern
2. its view
3. its template
4. any data passed to the template
5. the HTML shown by the browser

Write:

```text
URL
 ↓
URL pattern
 ↓
View
 ↓
Template
 ↓
Browser
```

## 10. Using ChatGPT

Ask:

> I understand Python but am new to web development. Trace what happens when a user visits `/bookings/` in this Django project. Explain the URL, view, model/database if relevant, template, and browser. Do not rewrite my code.

## Remember

```text
Browser → request
Django  → processing
View    → application logic
Template → HTML
CSS     → appearance
JavaScript → browser behavior
```
