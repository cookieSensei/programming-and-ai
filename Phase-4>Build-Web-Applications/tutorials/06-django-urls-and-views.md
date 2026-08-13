# Tutorial 06 — Django URLs and Views

## Why This Matters

URLs and views are the first Django connection students should understand.

## URL Patterns

```python
urlpatterns = [
    path("", home),
    path("about/", about),
]
```

This maps `/` to `home()` and `/about/` to `about()`.

## Views

```python
def home(request):
    return render(request, "pages/home.html")
```

A view receives a request and returns a response.

## Passing Data

```python
def products(request):
    products = [
        {"name": "Laptop", "price": 50000},
        {"name": "Mouse", "price": 1000},
    ]
    return render(request, "products.html", {"products": products})
```

The dictionary is context passed to the template.

## Dynamic URLs

```python
path("products/<int:id>/", product_detail)
```

For `/products/5/`, Django can call `product_detail(request, id=5)`.

## Remember

A URL does not directly create a page. It points Django toward code that decides what response to produce.

## Using ChatGPT

Ask: **“Explain why this URL pattern calls this view and what request means at a beginner level.”**
