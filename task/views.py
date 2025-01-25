from django.shortcuts import render
from django.http import HttpResponse
from task.forms import *
from task.models import *
from datetime import date

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

def view_task(request):
    # retrive all data from "Task" model:
    # tasks = Task.objects.all() -->(complexity high when retrive data from reverse relation)
    # tasks = TaskDetail.objects.select_related('task').all()
    # tasks = Task.objects.select_related('project').all()
    # tasks = Project.objects.prefetch_related('task_set').all()
    # tasks = Task.objects.prefetch_related('assign_to').all()
    tasks = Employee.objects.prefetch_related('task_set').all()
    # Only pending task:
    pending_tasks = Task.objects.filter(status = "PENDING")
    # Only tasks which due_date is today:
    todays_tasks = Task.objects.filter(due_date = date.today())
    # Only those tasks whose priority is not low:
    except_low = TaskDetail.objects.exclude(priority = 'L')
    context = {
        "tasks" : tasks,
        #"pending_tasks" : pending_tasks,
        #"todays_tasks" : todays_tasks,
        #"except_low" : except_low
    }
    return render(request, "show_task.html", context)