# Tutorial 01 — How the Web Works

## Why This Matters

Before Django, understand the simplest possible web mental model.

## The Flow

```text
Browser
   ↓ request
Web server / application
   ↓
Django
   ↓
Response
   ↓
Browser
```

A browser asks for a URL. The server/application decides what to return. The browser displays the response.

## HTML, CSS and JavaScript

```text
HTML       → structure
CSS        → appearance
JavaScript → browser behavior
```

Django runs on the server and can generate the HTML that the browser receives.

## Remember

You do not need networking theory yet.

> The browser asks. The server responds. Django helps the server produce the response.

## Try It

Open a website and identify what is probably HTML, CSS, JavaScript, and server-generated content.

## Using ChatGPT

Ask: **“I understand Python. Explain what happens when my browser requests a Django page, using Python concepts I already know.”**
