
from django.contrib import admin
from django.urls import path,include
from . import views


from django.urls import path
from .views import *
from .views import CompanyRegisterView, UserRegisterView, LoginView,trips,trip

urlpatterns = [
    path('',views.home, name='home'),
    path('register/company/', CompanyRegisterView.as_view(), name='company-register'),
    path('register/user/', UserRegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('user/<int:pk>',UserRegisterView_pk.as_view(),name='list_user'),
    path('Mixinuser_list/',views.Mixinuser_list.as_view()),
    path('mixinuser_pk/<int:pk>',views.mixinuser_pk.as_view()),
    path('all/trips/',trips,name='trips'),
    path('selected/trip/<int:pk>',trip,name='trip'),

]







