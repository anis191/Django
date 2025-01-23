from django.shortcuts import render
from django.http import HttpResponse
from task.forms import *
from task.models import *

# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    context = {
        "form" : TestForm(),
    }
    return render(request, "test.html", context)

def create_task(request):
    form = TaskModelForm()  # For 'GET'
    # For 'POST':
    if request.method == 'POST':
        form = TaskModelForm(request.POST) # For 'GET'
        if form.is_valid():
            form.save()
            return render(request, "task_form.html", {"form":form, 'message' : "Task added successfully!"})
    context = {
        "form" : form
    }
    return render(request, "task_form.html", context)