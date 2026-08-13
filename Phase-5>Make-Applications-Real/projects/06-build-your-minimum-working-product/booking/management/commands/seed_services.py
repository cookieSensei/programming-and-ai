from django.core.management.base import BaseCommand
from booking.models import Service

class Command(BaseCommand):
    help = "Create sample services."

    def handle(self, *args, **options):
        services = [
            ("Business Consultation", "A one-hour consultation for a business idea.", 60, "1500"),
            ("Website Planning", "A session to plan a small business website.", 90, "2500"),
            ("Product Review", "Review an early product idea and identify the next step.", 60, "1200"),
        ]
        for name, description, duration, price in services:
            Service.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                    "duration_minutes": duration,
                    "price": price,
                },
            )
        self.stdout.write(self.style.SUCCESS("Sample services created."))
