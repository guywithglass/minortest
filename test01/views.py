from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def home(request):
    return render(request, 'index1.html')

def areas(request):
    return render(request, 'areas.html')

def area_details(request):
    return render(request, 'area-details.html')

def response(request):
    aname = request.POST.get('name')
    aphone = request.POST.get('phone')
    alocation = request.POST.get('location')
    # print(aname, alocation)
    look = {'name':aname, 'phone': aphone, 'location':alocation}
    print(look)
    return render(request, 'response.html', look)

# account
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('register')
        else:
            user =  User.objects.create_user(first_name=name, email=email, username=username, password=password)
            user.save()
            print("User Created")
            return redirect('index')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('login')  
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'login.html')
