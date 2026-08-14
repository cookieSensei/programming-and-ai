# Tutorial 13 — JavaScript and the DOM

## Why this tutorial exists

The DOM can sound technical.

A beginner-friendly definition is:

> The DOM is the browser's representation of the HTML page.

JavaScript can use the DOM to find and change elements.

## 1. Start with HTML

```html
<p id="message">Hello</p>
```

JavaScript can find it:

```javascript
const message =
    document.getElementById("message");
```

Now `message` refers to the paragraph element.

## 2. Change the page

```javascript
message.textContent =
    "Hello from JavaScript";
```

The visible text changes.

The flow:

```text
HTML
 ↓
Browser creates DOM
 ↓
JavaScript finds element
 ↓
JavaScript changes element
 ↓
Browser updates page
```

## 3. Button example

HTML:

```html
<button id="hello-button">
    Say Hello
</button>

<p id="message"></p>
```

JavaScript:

```javascript
const button =
    document.getElementById("hello-button");

const message =
    document.getElementById("message");

button.addEventListener(
    "click",
    function () {
        message.textContent = "Hello!";
    }
);
```

The important idea:

```text
click
 ↓
event
 ↓
function
 ↓
DOM change
```

## 4. Why IDs matter

HTML:

```html
id="message"
```

JavaScript:

```javascript
getElementById("message")
```

The ID connects the two.

## 5. Other selectors

You may see:

```javascript
document.querySelector(".button");
```

or:

```javascript
document.querySelector("#message");
```

These are ways to find elements.

You do not need to memorize every selector.

## 6. Changing classes

JavaScript can modify CSS classes:

```javascript
message.classList.add("success");
```

or:

```javascript
message.classList.remove("hidden");
```

This is commonly used to show, hide, or style elements.

## 7. Reading input

HTML:

```html
<input id="name" type="text">
<button id="show">Show</button>
<p id="result"></p>
```

JavaScript:

```javascript
const nameInput =
    document.getElementById("name");

const result =
    document.getElementById("result");

const button =
    document.getElementById("show");

button.addEventListener(
    "click",
    function () {
        result.textContent =
            nameInput.value;
    }
);
```

The browser reads the input and updates the page.

## 8. DOM vs Django

Django primarily runs on the server.

The DOM exists in the browser.

```text
Server
 ↓
Django
 ↓
HTML
 ↓
Browser
 ↓
DOM
 ↓
JavaScript
```

So:

```text
Django     → server-side application
JavaScript → browser-side behavior
```

## 9. Debugging

If a button does nothing:

### Check HTML

Does the ID match?

```html
id="hello-button"
```

### Check JavaScript

Does it use:

```javascript
getElementById("hello-button")
```

### Check Console

Open:

```text
Developer Tools → Console
```

### Check Network

Did the JavaScript file actually load?

## 10. Exercise

Build:

```text
Name: [________]

[Say Hello]

Hello, ______!
```

Then build:

```text
Count: 0

[ + ]
[ - ]
```

## 11. Why this is enough

Later you may encounter:

- React
- Next.js
- browser APIs
- JavaScript libraries
- third-party widgets

You should not think:

> I have never seen this.

Instead:

> This is browser-side code selecting elements, responding to events, and changing the page.

That is the intended Phase 4 outcome.

## 12. Using ChatGPT

Ask:

> Here is my HTML and JavaScript. Explain which DOM elements are selected, which events are handled, and what changes when the user clicks. Do not rewrite the code.

## Remember

```text
HTML
 ↓
DOM
 ↓
JavaScript
 ↓
event
 ↓
function
 ↓
DOM changes
 ↓
browser updates
```
