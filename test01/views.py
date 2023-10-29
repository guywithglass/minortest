from django.http import HttpResponse
from django.shortcuts import render
from django import forms

def index(request):
    return render(request, 'index.html')

def response(request):
    aname = request.POST.get('name')
    alocation = request.POST.get('location')
    print(aname, alocation)
    look = {'name':aname, 'location':alocation}
    return render(request, 'response.html', look)

def login(request):
    return render(request, 'login.html')