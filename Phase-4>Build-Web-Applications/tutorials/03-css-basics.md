# Tutorial 03 — CSS Basics

## Why This Matters

Students need enough CSS to make sensible changes without learning frontend development.

## CSS Rules

```css
h1 {
    font-size: 40px;
}
```

`h1` is the selector, `font-size` is the property, and `40px` is the value.

## Classes

```html
<button class="primary-button">Book Now</button>
```

```css
.primary-button {
    padding: 12px 20px;
}
```

## Spacing and Layout

Common properties include:

```css
margin: 20px;
padding: 20px;
display: flex;
gap: 20px;
```

Flexbox is a common way to arrange items in rows or columns.

## Responsive Design

You may encounter:

```css
@media (max-width: 768px) {
    .navigation {
        display: none;
    }
}
```

This means styles can change for smaller screens.

## Try It

Change a Django page's heading size, colors, spacing, button appearance, and layout.

## Using ChatGPT

Ask: **“Improve this page visually, but explain which CSS classes you changed and where I can adjust spacing and colors.”**
