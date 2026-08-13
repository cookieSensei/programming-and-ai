from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import BookingForm
from .models import Booking, Service

def service_list(request):
    services = Service.objects.order_by("name")
    return render(request, "booking/service_list.html", {"services": services})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, "booking/service_detail.html", {"service": service})

@login_required
def book_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.service = service
            booking.save()
            return redirect("booking-confirmation", pk=booking.pk)
    else:
        form = BookingForm()
    return render(request, "booking/book_service.html", {"service": service, "form": form})

@login_required
def booking_confirmation(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    return render(request, "booking/booking_confirmation.html", {"booking": booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).select_related("service").order_by("-booking_date")
    return render(request, "booking/my_bookings.html", {"bookings": bookings})
