from django.db import migrations

def seed_services(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.bulk_create([
        Service(name="Discovery Call", description="A 30-minute introductory call.", price=0),
        Service(name="Consultation", description="A one-hour consultation.", price=2500),
    ])

def remove_services(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(name__in=["Discovery Call", "Consultation"]).delete()

class Migration(migrations.Migration):
    dependencies = [("main", "0001_initial")]
    operations = [migrations.RunPython(seed_services, remove_services)]
