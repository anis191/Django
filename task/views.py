from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("<h1>Welcome To Home Page</h1>")

def show_task(request):
    return HttpResponse("<h2>Tasks: <br>a.Task no-1<br>b.Task no-2<br>c.Task no-3</h2>")