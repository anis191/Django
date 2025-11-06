from django.shortcuts import render, redirect
from django.http import HttpResponse
from task.forms import *
from task.models import *
from datetime import date
from django.db.models import Q, Avg, Count, Min, Max, Sum
from django.contrib import messages

# Create your views here.

def manager_dashboard(request):
    type = request.GET.get('type')
    '''
    Need:
    1.Total Task, 2.Completed Task, 3.Task In Progress, 4.ToDos(In Pending)
    '''
    # tasks = Task.objects.select_related('details').prefetch_related('assign_to').all()
    # Access all needed data from database:
    counts = Task.objects.aggregate(
        total_task = Count('id'),
        completed_task = Count('id', filter=(Q(status='COMPLETED'))),
        InProgress_task = Count('id', filter=(Q(status='IN_PROGRESS'))),
        pending_task = Count('id', filter=(Q(status='PENDING'))),
    )

    base_query = Task.objects.select_related('details').prefetch_related('assign_to')
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    else:
        tasks = base_query.all()
    context = {
        "tasks" : tasks,
        "counts" : counts
    }
    return render(request, "dashboard/manager-dashboard.html", context)

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    context = {
        "form" : TestForm(),
    }
    return render(request, "test.html", context)

def create_task(request):
    task_form = TaskModelForm()  # For 'GET'
    task_detail_form = TaskDetailModelForm()

    # For 'POST':
    if request.method == 'POST':
        task_form = TaskModelForm(request.POST) # For 'GET'
        task_detail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request ,"Task Created Successfully!")
            return redirect('create-task')
    context = {
        "task_form" : task_form,
        "task_detail_form" : task_detail_form
    }
    return render(request, "task_form.html", context)

def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)  # For 'GET'
    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)

    # For 'POST':
    if request.method == 'POST':
        task_form = TaskModelForm(request.POST, instance=task) # For 'GET'
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request ,"Task Update Successfully!")
            return redirect('update-task', id)
    context = {
        "task_form" : task_form,
        "task_detail_form" : task_detail_form
    }
    return render(request, "task_form.html", context)

def delete_task(request, id):
    # Alaway use "POST" method for delete operation:
    if request.method == "POST":
        task = Task.objects.get(id = id)
        task.delete()
        messages.success(request ,"Task Delete Successfully!")
        return redirect('manager-dashboard')

def view_task(request):
    context = {
    }
    return render(request, "show_task.html", context)