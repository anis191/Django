from django.shortcuts import render, redirect
from django.http import HttpResponse
from task.forms import *
from task.models import *
from datetime import date
from django.db.models import Q, Avg, Count, Min, Max, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

# CBV view practice:
class Greetings(View):
    greeting = "Hello Everyone!"

    def get(self, request):
        return HttpResponse(self.greeting)

class HiGreetings(Greetings):
    # greeting = "Hi Everyone!"
    pass


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

""" Task Create view [Function-Based Views (FBVs)] """
'''
#admin and manager both are create a task:
@login_required
@permission_required("task.add_task", login_url='no-permission')
def create_task(request):
    task_form = TaskModelForm()  # For 'GET'
    task_detail_form = TaskDetailModelForm()

    # For 'POST':
    if request.method == 'POST':
        task_form = TaskModelForm(request.POST) # For 'GET'
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
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
'''

""" Task Create view [Class-Based Views (CBVs)] """
create_decorators = [login_required, permission_required("task.add_task", login_url='no-permission')]
# @method_decorator(create_decorators, name="dispatch")
# @method_decorator(permission_required("task.add_task", login_url='no-permission'), name="dispatch")
class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'task.add_task'
    login_url = 'sign-in'
    template_name = 'task_form.html'

    def get(self, request, *args, **kwargs):
        # task_form = TaskModelForm()
        # task_detail_form = TaskDetailModelForm()
        # context = {
            # "task_form" : task_form,
            # "task_detail_form" : task_detail_form
        # }
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get('task_detail_form', TaskDetailModelForm())
        return context

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request ,"Task Created Successfully!")
            context = self.get_context_data(task_form=task_form, task_detail_form=task_detail_form)
            return render(request, self.template_name, context)
            # return redirect('create-task')

'''
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
'''
class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)
        task_detail_form = TaskDetailModelForm(request.POST,request.FILES,instance=getattr(self.object, 'details', None))
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request ,"Task Update Successfully!")
            return redirect('update-task', self.object.id)
        return redirect('update-task', self.object.id)
'''
@login_required
@permission_required("task.delete_task", login_url='no-permission')
def delete_task(request, id):
    # Alaway use "POST" method for delete operation:
    if request.method == "POST":
        task = Task.objects.get(id = id)
        task.delete()
        messages.success(request ,"Task Delete Successfully!")
        return redirect('manager-dashboard')
'''
class DeleteTask(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'task.delete_task'
    model = Task
    success_url = reverse_lazy('manager-dashboard')
    pk_url_kwarg = 'id'
    def delete(self, request, *args, **kwargs):
        messages.success(self.request ,"Task Delete Successfully!")

view_task_decorators = [login_required, permission_required("task.view_task",login_url='no-permission')]
@method_decorator(view_task_decorators, name="dispatch")
class ViewTask(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'show_task.html'
    # return render(request, "show_task.html", context)

    def get_queryset(self):
        queryset = Project.objects.annotate(
            num_task=Count('task')
        ).order_by('num_task')
        return queryset
    

# @login_required
# @permission_required("task.view_task", login_url='no-permission')
# def task_details(request, task_id):
    # task = Task.objects.get(id = task_id)
    # status_choices = STATUS_CHOICES
    # if request.method == "POST":
        # selected_data = request.POST.get('task_status')
        # task.status = selected_data
        # task.save()
        # return redirect('task-details', task.id)
    # return render(request, 'task_details.html', {"task" : task, "status_choices": status_choices})

task_detail_decorators = [login_required, permission_required("task.view_task",login_url='no-permission')]
@method_decorator(task_detail_decorators, name="dispatch")
class TaskDetails(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = STATUS_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_data = request.POST.get('task_status')
        task.status = selected_data
        task.save()
        return redirect('task-details', task.id)
    
