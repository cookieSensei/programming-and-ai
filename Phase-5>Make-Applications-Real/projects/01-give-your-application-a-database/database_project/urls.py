from django.contrib import admin
from django.urls import path
from inventory.views import product_list, product_detail

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", product_list, name="product-list"),
    path("products/<int:pk>/", product_detail, name="product-detail"),
]
