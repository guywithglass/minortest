from django.shortcuts import render
from django import forms

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

# def home(request):
#     return render(request, 'index01.html')

def response(request):
    aname = request.POST.get('name')
    aphone = request.POST.get('phone')
    alocation = request.POST.get('location')
    # print(aname, alocation)
    look = {'name':aname, 'phone': aphone, 'location':alocation}
    print(look)
    return render(request, 'response.html', look)

def login(request):
    return render(request, 'login.html')


