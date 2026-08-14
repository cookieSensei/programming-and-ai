# Tutorial 16 - Debugging Django Applications

## Why this tutorial exists

Every developer encounters errors.

Your goal is not to avoid errors.

Your goal is to become comfortable investigating them.

Instead of:

> Everything is broken.

learn to think:

> The error is information about one part of my application.

## 1. Read the error

Suppose Django reports:

```text
django.db.utils.OperationalError:
no such table: main_product
```

That already tells you something important:

```text
Django tried to use a database table
        ↓
The table does not exist
```

## 2. Start near the bottom of a traceback

Tracebacks can be long.

Start with:

- exception type
- final error message
- file/line in your own code

Then work upward if necessary.

## 3. Common errors

### ModuleNotFoundError

Python cannot find a package/module.

Check:

```bash
which python
python -m pip --version
python -m pip list
```

Make sure the virtual environment is active.

### TemplateDoesNotExist

Django cannot find a template.

Check:

```text
template filename
template directory
render() path
extends path
template configuration
```

### NoReverseMatch

Django could not build a URL.

Check:

```text
URL name
arguments
{% url %}
redirect()
```

### 404

Django could not match the requested URL.

Trace:

```text
Browser URL
 ↓
urls.py
 ↓
path()
 ↓
view
```

### 500

Something failed inside the application.

Read the traceback and find the first meaningful line involving your code.

### no such table

Investigate migrations:

```bash
python manage.py showmigrations
python manage.py migrate
```

If you changed a model:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. A debugging process

Use this sequence:

```text
1. What did I expect?
2. What actually happened?
3. What is the exact error?
4. Which file/line is involved?
5. What changed recently?
6. Can I reproduce it?
7. What is the smallest fix?
```

## 5. Check the environment

If a package is missing:

```bash
which python
python -m pip --version
python -m pip list
```

The Python and pip paths should belong to your project's environment.

## 6. Separate server and browser problems

Some errors happen on the server:

```text
Python
Django
database
templates
views
```

Others happen in the browser:

```text
JavaScript
DOM
CSS
resource loading
```

Use:

```text
Terminal → server-side errors

Console → JavaScript/browser errors

Network → HTTP/resource failures
```

## 7. Example: CSS missing

Suppose:

```text
HTML works
CSS missing
```

Do not immediately rewrite the CSS.

Check:

```text
template
 ↓
static path
 ↓
browser network request
 ↓
CSS response
```

If the browser never receives the CSS, changing CSS rules will not help.

## 8. Example: form fails

Suppose:

```text
Submit
 ↓
500
```

Check:

```text
request method
 ↓
view
 ↓
form validation
 ↓
model/database
 ↓
redirect
```

The error tells you which layer failed.

## 9. Don't randomly change many files

Bad debugging:

```text
Error
 ↓
change 5 files
 ↓
new error
 ↓
change 5 more
 ↓
confusion
```

Better:

```text
Error
 ↓
identify layer
 ↓
identify file
 ↓
one change
 ↓
test
```

## 10. Git as a safety net

Before a significant experiment:

```bash
git status
git add .
git commit -m "Working booking form"
```

Now you have a checkpoint.

This makes experimentation safer.

## 11. Use ChatGPT effectively

Give AI:

```text
Exact error
Relevant code
Project structure if relevant
Expected behavior
Actual behavior
Recent changes
```

Then ask:

> Identify the root cause and suggest the smallest fix. Do not rewrite unrelated code.

## 12. Intentionally break things

One excellent exercise is to deliberately create small mistakes:

- change a template path
- change a URL name
- break a static-file path
- introduce a Python syntax error
- change a model without migrating

Then debug each problem.

You are training the skill of investigation.

## 13. The debugging mindset

Debugging is:

```text
Observe
 ↓
Understand
 ↓
Hypothesize
 ↓
Change
 ↓
Test
```

Not:

```text
Panic
 ↓
copy random code
 ↓
change everything
```

## Remember

You are not expected to know every Django error.

You are expected to know how to investigate one.

That is a much more transferable skill.
