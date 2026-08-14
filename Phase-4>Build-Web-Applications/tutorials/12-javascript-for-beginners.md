# Tutorial 12 - JavaScript for Beginners

## Why this tutorial exists

This is **not a JavaScript course**.

The purpose is to make JavaScript familiar enough that students do not become uncomfortable when they encounter it later.

You already know Python. Many programming ideas remain the same across languages.

## 1. Variables

Python:

```python
name = "Ashish"
```

JavaScript:

```javascript
const name = "Ashish";
```

Both create a named value.

You may also see:

```javascript
let count = 0;
```

For this course, understand the concept before worrying about every distinction between `let`, `const`, and `var`.

## 2. Strings

```javascript
const name = "Ashish";
const message = "Hello " + name;
```

You may also see:

```javascript
const message = `Hello ${name}`;
```

## 3. Numbers

```javascript
let count = 0;
count = count + 1;
```

This should feel familiar from Python.

## 4. Functions

Python:

```python
def greet(name):
    return "Hello " + name
```

JavaScript:

```javascript
function greet(name) {
    return "Hello " + name;
}
```

The syntax differs, but the concept is:

```text
input
 ↓
function
 ↓
result
```

## 5. Conditions

Python:

```python
if age >= 18:
    print("Adult")
```

JavaScript:

```javascript
if (age >= 18) {
    console.log("Adult");
}
```

Again, the programming concept is familiar.

## 6. Arrays

Python:

```python
products = ["Laptop", "Mouse"]
```

JavaScript:

```javascript
const products = ["Laptop", "Mouse"];
```

Both represent collections.

## 7. Objects

JavaScript:

```javascript
const product = {
    name: "Laptop",
    price: 50000
};
```

This is similar in spirit to a Python dictionary:

```python
product = {
    "name": "Laptop",
    "price": 50000,
}
```

## 8. Console

JavaScript developers often inspect values using:

```javascript
console.log(product);
```

Open browser developer tools → Console.

This is the browser equivalent of having a quick place to inspect values while debugging.

## 9. Events

The browser generates events:

```text
click
submit
change
input
```

JavaScript can respond.

Conceptually:

```text
User clicks
 ↓
Browser event
 ↓
JavaScript function
 ↓
Page changes
```

## 10. A small example

HTML:

```html
<button id="hello-button">
    Say Hello
</button>
```

JavaScript:

```javascript
const button =
    document.getElementById("hello-button");

button.addEventListener(
    "click",
    function () {
        console.log("Hello!");
    }
);
```

You do not need to memorize this.

Recognize:

```text
document
 ↓
find an element

addEventListener
 ↓
wait for event

function
 ↓
perform action
```

## 11. JavaScript and Django

Django can generate the initial page:

```text
Django
 ↓
HTML
 ↓
Browser
```

JavaScript can then add browser-side behavior:

```text
Browser
 ↓
JavaScript
 ↓
interaction
```

For example, Django might render a booking form while JavaScript provides instant UI feedback.

## 12. JavaScript errors

You may see:

```text
ReferenceError
TypeError
SyntaxError
```

Do not panic.

Open:

```text
Developer Tools → Console
```

Read the message and line number.

## 13. Small project

Build:

```text
Count: 0

[ + ]
```

Clicking the button should increment the count.

This introduces:

- variable
- function
- event
- DOM element
- browser console

That is enough for the program's purpose.

## 14. Python comparison

| Concept | Python | JavaScript |
|---|---|---|
| Variable | `name = "A"` | `const name = "A"` |
| Function | `def greet():` | `function greet() {}` |
| List/array | `[]` | `[]` |
| Dictionary/object | `{}` | `{}` |
| Condition | `if` | `if` |
| Debug output | `print()` | `console.log()` |

## 15. Using ChatGPT

Ask:

> I know Python but am new to JavaScript. Explain this JavaScript by comparing its variables, functions, collections, conditions, and events to Python concepts.

## Remember

You do not need to become a JavaScript programmer.

You need to be able to see:

```javascript
const
let
function
if
for
console.log
document
addEventListener
```

and think:

> I recognize the programming ideas even if the syntax is different.
