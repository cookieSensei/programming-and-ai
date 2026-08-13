from django.urls import path
from .views import booking_confirmation, book_service, my_bookings, service_detail, service_list

urlpatterns = [
    path("", service_list, name="service-list"),
    path("services/<int:pk>/", service_detail, name="service-detail"),
    path("services/<int:pk>/book/", book_service, name="book-service"),
    path("booking/<int:pk>/confirmation/", booking_confirmation, name="booking-confirmation"),
    path("my-bookings/", my_bookings, name="my-bookings"),
]
