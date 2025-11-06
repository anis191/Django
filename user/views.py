from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from user.forms import *

# Create your views here.
def sign_up(request):
    form = CustomRegisterForm
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
    return render(request, "registration/register.html", {"form":form})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, "registration/login.html")

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')