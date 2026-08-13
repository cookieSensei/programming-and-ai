from django.shortcuts import render
from .forms import BookingForm
from .models import Service

def home(request):
    return render(request, "main/home.html", {"services": Service.objects.all()})

def book(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        booking = form.save()
        return render(request, "main/confirmation.html", {"booking": booking})
    return render(request, "main/book.html", {"form": form})
