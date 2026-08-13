# Tutorial 02 — HTML Basics

## Why This Matters

Students need enough HTML to understand and modify AI-generated pages.

## Common Elements

```html
<h1>Heading</h1>
<p>Paragraph</p>
<a href="/about/">About</a>
<img src="/static/logo.png" alt="Logo">

<ul>
    <li>Item</li>
</ul>
```

## Page Structure

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
</head>
<body>
    <h1>Hello</h1>
</body>
</html>
```

## Attributes

Attributes add information to elements:

```html
<a href="/contact/" class="button">Contact</a>
```

Here `href` controls the destination and `class` gives CSS/JavaScript something to target.

## Forms

```html
<form method="post">
    <input type="text" name="name">
    <button type="submit">Submit</button>
</form>
```

The `name` identifies submitted data.

## Try It

Create a page with a heading, paragraph, link, image, list, and form.

## Using ChatGPT

Ask: **“Explain the HTML structure in this page and tell me which elements I should change to modify the heading, navigation, and button.”**
