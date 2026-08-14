# Tutorial 09 - Django Forms and User Input

## Why this matters

Forms collect information. Django must receive, validate, process, and often store that information.

The complete flow is:

```text
User
 ↓
HTML form
 ↓
HTTP request
 ↓
Django view
 ↓
Validation
 ↓
Application logic
 ↓
Database / action
 ↓
Response
```

## 1. HTML is only the beginning

A browser form might contain:

```html
<form method="post">
    <input type="text" name="name">
    <button type="submit">Book</button>
</form>
```

The browser sends the submitted values.

Django still has to decide what to do with them.

## 2. Django Forms

Django provides a form system:

```python
from django import forms

class BookingForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
```

The form can validate incoming information.

## 3. Form validity

Conceptually:

```python
if form.is_valid():
    ...
else:
    ...
```

If the email is invalid, Django can expose a form error.

This is better than manually trusting strings received from the browser.

## 4. `cleaned_data`

After validation, Django forms provide cleaned values:

```python
if form.is_valid():
    name = form.cleaned_data["name"]
```

This is a major reason to use Django's form system.

## 5. ModelForm

If your form creates or updates a model, a `ModelForm` may be useful:

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

For beginner projects, this often removes repetitive code.

## 6. GET and POST

A common pattern:

```python
def booking(request):
    if request.method == "POST":
        ...
    else:
        ...
```

Conceptually:

```text
GET
 ↓
show form

POST
 ↓
receive form
 ↓
validate
 ↓
save
```

## 7. CSRF

Django normally requires:

```django
{% csrf_token %}
```

in POST forms.

It provides protection against cross-site request forgery.

Do not remove it just because it looks unfamiliar.

If you encounter a CSRF error, understand the cause rather than disabling protection blindly.

## 8. Validation

Never trust user input.

Examples:

```text
email = invalid
quantity = negative
date = impossible
```

Client-side validation can improve user experience:

```html
<input type="email" required>
```

But server-side validation remains important because a user can send requests without using your HTML form.

## 9. Saving a booking

Conceptually:

```python
if form.is_valid():
    Booking.objects.create(
        name=form.cleaned_data["name"],
        email=form.cleaned_data["email"],
    )
```

The database is now part of the workflow.

## 10. Redirect after success

A common pattern:

```text
POST
 ↓
Validate
 ↓
Save
 ↓
Redirect
 ↓
GET confirmation
```

This is often called Post/Redirect/Get.

It helps avoid accidental duplicate submissions after refreshing a POST response.

## 11. Displaying errors

A template can display form errors.

For example:

```django
{{ form.name.errors }}
```

You may also let Django render the form:

```django
{{ form.as_p }}
```

This is convenient for learning, though later you may want more control over HTML and styling.

## 12. Exercise

Create a booking form:

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
redirect to confirmation
```

Then deliberately submit invalid data and observe the errors.

## 13. Debugging

Check:

```text
form method
input names
csrf token
view POST branch
form.is_valid()
database save
redirect
```

## 14. Using ChatGPT

Ask:

> Here is my Django form and view. Explain what happens from the moment the user clicks Submit until the Booking is saved. Identify where validation occurs. Do not rewrite my code.

## Remember

Forms are not just HTML.

They are a pipeline:

```text
browser
 ↓
request
 ↓
validation
 ↓
application logic
 ↓
database
 ↓
response
```
