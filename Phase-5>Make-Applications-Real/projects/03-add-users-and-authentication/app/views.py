from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Task

@login_required
def home(request):
    tasks = Task.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "app/home.html", {"tasks": tasks})
