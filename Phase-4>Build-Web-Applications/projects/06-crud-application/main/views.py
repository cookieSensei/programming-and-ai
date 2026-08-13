from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm
from .models import Product

def product_list(request): return render(request,"main/product_list.html",{"products":Product.objects.all()})
def product_detail(request, pk): return render(request,"main/product_detail.html",{"product":get_object_or_404(Product,pk=pk)})
def product_create(request):
    form=ProductForm(request.POST or None)
    if form.is_valid():
        product=form.save(); return redirect("product_detail",pk=product.pk)
    return render(request,"main/product_form.html",{"form":form,"title":"Add Product"})
def product_update(request, pk):
    product=get_object_or_404(Product,pk=pk); form=ProductForm(request.POST or None,instance=product)
    if form.is_valid(): form.save(); return redirect("product_detail",pk=product.pk)
    return render(request,"main/product_form.html",{"form":form,"title":"Edit Product"})
def product_delete(request, pk):
    product=get_object_or_404(Product,pk=pk)
    if request.method=="POST": product.delete(); return redirect("product_list")
    return render(request,"main/product_confirm_delete.html",{"product":product})
