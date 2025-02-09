from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from user.forms import *
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
def sign_up(request):
    form = CustomRegisterForm
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('CreatePassword'))
            user.is_active = False
            user.save()
            messages.success(request, "A confirmation mail sent. Check your email")
            return redirect('sign-in')
    return render(request, "registration/register.html", {"form":form})

def sign_in(request):
    # Django custom sign-in/login form:
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, "registration/login.html", {'form':form})

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        # now varify token using build in authenticate function:
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid user id and url's")
    except:
        return HttpResponse('User Not Found!')