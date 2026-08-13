# Tutorial 13 — JavaScript and the DOM

## Why This Matters

Students should understand the basic idea behind browser-side JavaScript.

## Finding Elements

HTML:

```html
<p id="message">Hello</p>
```

JavaScript:

```javascript
const message = document.getElementById("message");
```

## Changing the Page

```javascript
message.textContent = "Hello from JavaScript";
```

## Events

```javascript
button.addEventListener("click", function () {
    message.textContent = "Hello!";
});
```

The flow is:

```text
Click → event → function → DOM change → updated page
```

## Django Connection

Django can generate the initial HTML. JavaScript can make that page interactive after it reaches the browser.

## Try It

Build a tiny counter with a `+` button.

## Using ChatGPT

If it fails, provide the HTML, JavaScript, and browser console error. Ask for diagnosis rather than asking ChatGPT to rewrite everything.
