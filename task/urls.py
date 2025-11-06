from django.urls import path
from task.views import *

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name="manager-dashboard"),
    path('user-dashboard/', user_dashboard, name="user-dashboard"),
    # path('create-task/', create_task, name="create-task"), #For FBVs
    path('create-task/', CreateTask.as_view(), name="create-task"), #For CBVs
    path('view-task/', ViewTask.as_view(), name="view-task"),
    path('update-task/<int:id>/', UpdateTask.as_view(), name="update-task"),
    # path('delete-task/<int:id>/', delete_task, name="delete-task"),
    path('delete-task/<int:id>/', DeleteTask.as_view(), name="delete-task"),
    path('task/<int:task_id>/details/', TaskDetails.as_view(), name="task-details"),

    # CBV path practice:
    path('greeting/', Greetings.as_view(), name='greeting'),
    path('hi-greeting/', HiGreetings.as_view(greeting = "Hi Everyone!"), name='hi-greeting'),
]