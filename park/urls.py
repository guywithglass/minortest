from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('response/', views.response, name='response'),
    path('login/', views.login, name='login')
]

