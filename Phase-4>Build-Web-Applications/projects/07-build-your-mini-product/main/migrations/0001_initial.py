from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[
        migrations.CreateModel(name="Service",fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("name",models.CharField(max_length=120)),("description",models.TextField()),("price",models.DecimalField(decimal_places=2,max_digits=10))]),
        migrations.CreateModel(name="Booking",fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("customer_name",models.CharField(max_length=120)),("email",models.EmailField(max_length=254)),("preferred_date",models.DateField()),("created_at",models.DateTimeField(auto_now_add=True)),("service",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to="main.service"))]),
    ]
