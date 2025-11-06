from django.urls import path
from task.views import *

urlpatterns = [
    path('manager-dashboard/', manager_dashboard),
    path('user-dashboard/', user_dashboard),
    path('test/', test),
    path('create-task/', create_task),
    path('view-task/', view_task),
]