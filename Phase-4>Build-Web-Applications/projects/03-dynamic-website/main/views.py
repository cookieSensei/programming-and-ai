from django.shortcuts import get_object_or_404, render

PRODUCTS=[
 {"id":1,"name":"Laptop","price":50000,"description":"A practical work laptop.","available":True},
 {"id":2,"name":"Keyboard","price":2000,"description":"A comfortable mechanical keyboard.","available":True},
 {"id":3,"name":"Mouse","price":1000,"description":"A simple wireless mouse.","available":False},
 {"id":4,"name":"Monitor","price":12000,"description":"A 27-inch productivity monitor.","available":True},
 {"id":5,"name":"Webcam","price":3500,"description":"A webcam for online meetings.","available":True},
]

def products(request): return render(request,"main/products.html",{"products":PRODUCTS})
def product_detail(request, product_id):
    product = next((item for item in PRODUCTS if item["id"] == product_id), None)
    if product is None:
        from django.http import Http404
        raise Http404("Product not found")
    return render(request,"main/product_detail.html",{"product":product})
