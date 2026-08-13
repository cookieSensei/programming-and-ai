from django.core.management.base import BaseCommand
from inventory.models import Product

class Command(BaseCommand):
    help = "Create sample products."

    def handle(self, *args, **options):
        products = [
            ("Laptop", "A sample laptop.", "50000", 5),
            ("Keyboard", "A sample keyboard.", "2000", 12),
            ("Mouse", "A sample mouse.", "1000", 20),
        ]
        for name, description, price, quantity in products:
            Product.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                    "price": price,
                    "quantity": quantity,
                },
            )
        self.stdout.write(self.style.SUCCESS("Sample products created."))
