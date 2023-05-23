from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from account.models import User
import random

def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password == password2:
            username = first_name.lower() + last_name.lower() + str(random.randint(1000, 9999))
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, phone=phone)
            messages.success(request, "You're succesfuly registered !")
            return redirect('account:redirect_to_cloud' )
    else:
        return render(request, 'register.html')

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('cloud:cloud_home')
        else:
            messages.error(request, "There was an error logging in, try again...")
            return redirect('account:redirect_to_cloud')
    elif request.user.is_authenticated:
        return redirect('cloud:cloud_home')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('account:redirect_to_cloud')

def redirect_to_cloud(request):
    if request.user.is_authenticated:
        return redirect('cloud:cloud_home')
    else:
        return redirect('account:login_user')
