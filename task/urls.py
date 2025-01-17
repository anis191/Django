from django.urls import path
from task.views import *

urlpatterns = [
    path("home/", home),
    path("showTask/", show_task)
]