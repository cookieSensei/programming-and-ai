# Tutorial 04 — HTML Forms

## Why This Matters

Forms are the bridge between a webpage and application logic.

## Basic Form

```html
<form method="post">
    <input type="text" name="name">
    <button type="submit">Submit</button>
</form>
```

## GET and POST

A simple mental model:

```text
GET  → request/read information
POST → submit/change information
```

## CSRF

Django forms that submit with POST commonly include:

```django
{% csrf_token %}
```

Django uses CSRF protection to help prevent unwanted requests from other sites. If Django tells you to include it, do not remove it just because you do not recognize it.

## Django Flow

```text
Form
 ↓
User input
 ↓
Request
 ↓
Django view
 ↓
Validation
 ↓
Save/process
 ↓
Response
```

## Try It

Build a form with name, email, and message. Submit it and identify where Django receives the data.

## Using ChatGPT

Ask: **“What does csrf_token do in this Django form, and why is it required?”**
