# Tutorial 06 — Django URLs and Views

## Why this matters

One of the most important Django concepts is how a browser URL becomes Python code.

The core relationship is:

```text
URL
 ↓
View
 ↓
Response
```

## 1. A simple view

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello!")
```

When Django calls `home`, it gives the function a request object.

The function returns a response.

## 2. Connecting a URL

In `urls.py`:

```python
from django.urls import path
from .views import home

urlpatterns = [
    path("", home),
]
```

Now:

```text
Browser requests /
       ↓
Django matches ""
       ↓
home()
```

## 3. Multiple pages

```python
urlpatterns = [
    path("", home),
    path("about/", about),
    path("contact/", contact),
]
```

Now:

```text
/          → home
/about/    → about
/contact/  → contact
```

## 4. Rendering a template

Instead of returning plain text:

```python
return HttpResponse("Hello")
```

use:

```python
from django.shortcuts import render

def home(request):
    return render(request, "main/home.html")
```

The flow becomes:

```text
URL
 ↓
home()
 ↓
home.html
 ↓
HTML response
```

## 5. Passing data

```python
def home(request):
    name = "CookieSensei"

    return render(
        request,
        "main/home.html",
        {"name": name},
    )
```

Template:

```django
<h1>Welcome to {{ name }}</h1>
```

The dictionary is context.

## 6. Querying data

```python
products = Product.objects.all()

return render(
    request,
    "main/products.html",
    {"products": products},
)
```

The template can loop through them:

```django
{% for product in products %}
    <h2>{{ product.name }}</h2>
{% endfor %}
```

## 7. Dynamic URLs

You can capture information from the URL:

```python
path(
    "products/<int:id>/",
    product_detail,
)
```

For:

```text
/products/7/
```

Django can call:

```python
def product_detail(request, id):
    ...
```

with:

```text
id = 7
```

## 8. Getting an object

You may see:

```python
product = Product.objects.get(id=id)
```

If it does not exist, this can raise an exception.

A common Django pattern is:

```python
from django.shortcuts import get_object_or_404

product = get_object_or_404(
    Product,
    id=id,
)
```

This produces a 404 response when the record cannot be found.

## 9. Redirects

After an action:

```python
return redirect("home")
```

can send the browser to another route.

A common flow:

```text
Submit form
 ↓
Save
 ↓
Redirect
 ↓
Confirmation/list page
```

## 10. Debugging 404 errors

If `/products/5/` gives a 404, trace:

```text
Browser URL
 ↓
root urls.py
 ↓
included app urls.py
 ↓
path()
 ↓
view
```

Do not immediately change the view if Django is not reaching it.

## 11. Exercise

Create:

```text
/
about/
/contact/
/products/
/products/1/
```

Make `/products/` display a list and `/products/1/` display one product.

## 12. Using ChatGPT

Ask:

> Here are my `urls.py` and `views.py`. `/products/5/` gives a 404. Explain how Django matches this URL and identify the likely problem. Do not rewrite the entire project.

## Remember

```text
URL
 ↓
URL pattern
 ↓
View
 ↓
Logic
 ↓
Response
```

A Django page is usually not a file sitting at that URL. The URL is routed to Python code that decides what response to produce.
