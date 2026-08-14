# Tutorial 03 — CSS Basics

## Why this matters

HTML gives a page structure. CSS controls how that structure looks.

The goal is not to become a professional frontend developer. The goal is to understand AI-generated CSS well enough to change and debug your website.

## 1. A CSS rule

```css
h1 {
    font-size: 48px;
    color: #222;
}
```

Think:

```text
h1          → selector
font-size   → property
48px        → value
```

## 2. Element selectors

```css
p {
    color: #444;
}
```

This applies to paragraphs.

## 3. Class selectors

HTML:

```html
<button class="primary-button">Book Now</button>
```

CSS:

```css
.primary-button {
    background: black;
    color: white;
}
```

The `.` means "element with this class."

## 4. IDs

```css
#hero {
    padding: 80px;
}
```

This targets the element with `id="hero"`.

Classes are generally more reusable.

## 5. Colors and typography

Common properties:

```css
color: #222;
background-color: #f5f5f5;
font-family: Arial, sans-serif;
font-size: 18px;
font-weight: 600;
line-height: 1.5;
```

You do not need to memorize every value. Learn to identify what the property controls.

## 6. Margin and padding

This is essential.

```css
.card {
    padding: 20px;
    margin: 30px;
}
```

Simplified:

```text
margin
  ↓
outside

border

padding
  ↓
inside

content
```

Remember:

```text
padding → inside
margin  → outside
```

## 7. Borders and radius

```css
.card {
    border: 1px solid #ddd;
    border-radius: 12px;
}
```

## 8. Flexbox

A very common layout:

```css
.navigation {
    display: flex;
    gap: 24px;
}
```

Other properties you may see:

```css
justify-content: center;
align-items: center;
flex-direction: column;
```

Think:

> `display: flex` means the element's children are being arranged with Flexbox.

## 9. Grid

Another layout system:

```css
.products {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
}
```

This can create a three-column layout.

## 10. Responsive design

A website may be viewed on phones, tablets, and laptops.

CSS can change based on screen width:

```css
@media (max-width: 768px) {
    .hero {
        padding: 40px 20px;
    }
}
```

Read this as:

> At 768px or less, use these styles.

## 11. The box model

Think of every element as a box:

```text
margin
border
padding
content
```

When spacing looks wrong, ask:

> Is the problem inside the element, around it, or between neighboring elements?

Then investigate:

```text
padding
margin
border
gap
```

## 12. Why CSS does not work

Common causes:

### Selector mismatch

HTML:

```html
<button class="primary">
```

CSS:

```css
.primary-button { ... }
```

These do not match.

### CSS file not loaded

The code may be correct but the browser may not have received the file.

### Rule overridden

Another rule may be more specific or loaded later.

### Typo

```css
font-szie: 20px;
```

The browser ignores the invalid property.

## 13. Developer tools

Right-click an element and choose **Inspect**.

Use:

- Elements
- Styles
- Network

The Styles panel shows which rules apply and which are crossed out.

This is one of the most useful skills you can learn.

## 14. Exercise

Take a Django page and change:

1. heading size
2. paragraph color
3. button appearance
4. button padding
5. card border
6. card spacing
7. navigation layout
8. mobile spacing

Try before asking AI.

## 15. Using ChatGPT

Ask:

> The cards on my Django page are too close together. Here is my HTML and CSS. Explain whether I should use margin, padding, or gap, and show the smallest change.

## Remember

Recognize:

```text
selector
class
property
value
margin
padding
border
flex
grid
gap
media query
```

Your goal is not to master CSS. Your goal is to make CSS feel understandable rather than mysterious.
