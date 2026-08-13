from django.shortcuts import render

def home(request): return render(request, "main/home.html")
def services(request): return render(request, "main/services.html")
def about(request): return render(request, "main/about.html")
def pricing(request): return render(request, "main/pricing.html")
def contact(request): return render(request, "main/contact.html")
