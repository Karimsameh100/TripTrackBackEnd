
from django.contrib import admin
from django.urls import path,include
from . import views


from django.urls import path
from .views import CompanyRegisterView, UserRegisterView, LoginView

urlpatterns = [
    path('',views.home, name='home'),
    path('register/company/', CompanyRegisterView.as_view(), name='company-register'),
    path('register/user/', UserRegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),
]







