# Tutorial 09 — Django Forms and User Input

## Why This Matters

Students need to understand how user input moves through a Django application.

## Flow

```text
User
 ↓
HTML form
 ↓
Request
 ↓
Django view
 ↓
Validation
 ↓
Application logic
 ↓
Response
```

## Django Forms

Django can generate and validate forms:

```python
class BookingForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
```

## Model Forms

When a form maps closely to a database model, `ModelForm` can reduce repetitive code:

```text
Model → ModelForm → HTML form
```

## POST and Redirect

A common successful flow is:

```text
POST
 ↓
Save
 ↓
Redirect
 ↓
GET result page
```

This helps avoid accidental repeated submissions.

## Try It

Build a booking form with name, email, service, and date. Validate required fields.

## Using ChatGPT

Ask: **“Explain this Django form from user input all the way to the database, and identify where validation happens.”**
