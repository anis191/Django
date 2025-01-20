from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    context = {
        "name" : "Anisul Alam",
        "age" : 24,
        "address" : "Chittagong",
        "cgpa" : [2.55, 3.44, 3.57, 2.55, 3.00, 3.23, 2.98, 3.99, 2.11, 2.00],
        "isTrue" : True
    }
    return render(request, "test.html", context)