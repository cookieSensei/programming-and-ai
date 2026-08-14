# Tutorial 04 - HTML Forms

## Why this matters

A static website displays information.

An application lets users send information back.

Forms are the bridge between the browser and Django.

Common examples:

- booking
- contact
- login
- registration
- search
- feedback
- product creation

## 1. Basic form

```html
<form method="post">
    <label for="name">Name</label>

    <input
        type="text"
        id="name"
        name="name"
    >

    <button type="submit">Submit</button>
</form>
```

Conceptually:

```text
form
 ↓
contains submission

input
 ↓
collects information

button
 ↓
submits
```

## 2. The `name` attribute

Consider:

```html
<input type="text" name="customer_name">
```

If the user types:

```text
Ashish
```

the submitted information can be represented as:

```text
customer_name = Ashish
```

Django can then read that value.

## 3. Input types

```html
<input type="text" name="name">
<input type="email" name="email">
<input type="password" name="password">
<input type="date" name="date">
<input type="number" name="quantity">
```

Different input types provide different browser behavior and basic validation.

## 4. Textarea

```html
<textarea
    name="message"
    rows="5"
></textarea>
```

Useful for longer text.

## 5. Select

```html
<select name="service">
    <option value="consulting">Consulting</option>
    <option value="training">Training</option>
</select>
```

The user sees readable choices while the application receives a defined value.

## 6. GET vs POST

A useful beginner model:

```text
GET  → request/read information
POST → submit information
```

For example:

```text
GET /products/
 ↓
show products

POST /booking/
 ↓
create booking
```

This is a simplified model; real applications use both methods in more situations.

## 7. Django POST flow

A view may contain:

```python
if request.method == "POST":
    ...
```

The overall flow:

```text
GET
 ↓
show form

POST
 ↓
receive data
 ↓
validate
 ↓
save/process
 ↓
redirect or show errors
```

## 8. CSRF protection

Django commonly requires:

```django
{% csrf_token %}
```

inside POST forms:

```django
<form method="post">
    {% csrf_token %}

    <input name="name">

    <button type="submit">Submit</button>
</form>
```

CSRF protection helps prevent unwanted requests made from another website using a user's browser session.

You do not need to understand the cryptography.

Remember:

> If Django expects CSRF protection, do not remove it simply because the token looks unfamiliar.

## 9. Validation

User input cannot automatically be trusted.

Examples:

```text
email = hello
quantity = -500
date = invalid
```

Your application should validate information before using or storing it.

HTML can provide basic validation:

```html
<input type="email" required>
```

But server-side validation is still necessary because users can send requests without using your exact browser form.

## 10. Django Forms

Django provides a form system:

```python
from django import forms

class BookingForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
```

Django can help with validation and error handling.

## 11. ModelForm

When a form maps closely to a model:

```text
Model
 ↓
ModelForm
 ↓
HTML form
 ↓
User
 ↓
Model
 ↓
Database
```

`ModelForm` can reduce repetitive code.

## 12. Redirect after POST

A common successful flow is:

```text
POST
 ↓
save
 ↓
redirect
 ↓
GET result page
```

This helps avoid accidental duplicate submissions on refresh.

## 13. Debugging a form

Check:

1. Is the form using the expected method?
2. Do inputs have `name` attributes?
3. Is CSRF included?
4. Does the Django view handle POST?
5. Is validation failing?
6. Is the database save succeeding?
7. Is the browser being redirected?

## 14. Exercise

Build a booking form with:

```text
Name
Email
Service
Date
```

Implement:

```text
GET /booking/
 ↓
show form

POST /booking/
 ↓
validate
 ↓
save
 ↓
confirmation
```

## 15. Using ChatGPT

Give AI the form, view, form class if present, and exact error.

Ask:

> Explain the request flow and identify where the problem occurs before suggesting a fix.

## Remember

```text
User
 ↓
HTML form
 ↓
HTTP request
 ↓
Django
 ↓
validation
 ↓
application logic
 ↓
database/action
 ↓
response
```
