from django.shortcuts import render, redirect
from django.http import HttpResponse
from task.forms import *
from task.models import *
from datetime import date
from django.db.models import Q, Avg, Count, Min, Max, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

# Create your views here.
#Test user 'manager' or not?
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@user_passes_test(is_manager, login_url='no-permission')
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

@user_passes_test(is_employee)
def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

#admin and manager both are create a task:
@login_required
@permission_required("task.add_task", login_url='no-permission')
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

@login_required
@permission_required("task.change_task", login_url='no-permission')
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

@login_required
@permission_required("task.delete_task", login_url='no-permission')
def delete_task(request, id):
    # Alaway use "POST" method for delete operation:
    if request.method == "POST":
        task = Task.objects.get(id = id)
        task.delete()
        messages.success(request ,"Task Delete Successfully!")
        return redirect('manager-dashboard')

@login_required
@permission_required("task.view_task", login_url='no-permission')
def view_task(request):
    context = {
    }
    return render(request, "show_task.html", context)