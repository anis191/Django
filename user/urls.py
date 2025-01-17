from django.urls import path
from user.views import *

urlpatterns = [
    path("userHome/", user_home)
]