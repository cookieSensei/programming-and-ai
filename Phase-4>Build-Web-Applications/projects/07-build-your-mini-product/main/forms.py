from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["customer_name", "email", "service", "preferred_date"]
        widgets = {"preferred_date": forms.DateInput(attrs={"type":"date"})}
