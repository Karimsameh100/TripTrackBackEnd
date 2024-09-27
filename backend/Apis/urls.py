
from django.contrib import admin
from django.urls import path,include
from . import views
from .views import *

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
    path('all-users/', AllUsersView.as_view(), name='all-users'),
    path('cities/', CityView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityView.as_view(), name='city-detail'),
    path('favorites/', FavoriteListCreateView.as_view(), name='favorite-list-create'),
    path('user/admin/', AdminView.as_view(), name='admin-list'),
    path('user/admin/<int:pk>/', AdminView_pk.as_view(), name='admin-detail'),
    path('find/trip/',findTrips,name='findtrips'),
    path("booking/data/",booking,name='booking'),
    path('booking/<int:pk>/update-status/', update_booking_status, name='update-booking-status'),
    path('currant-user/',views.CurrentUserView.as_view(),name='currentuser'),
    # path('create-payment/', views.CreatePaymentView.as_view(), name='create_payment'),
    path('payments/', PaymentView.as_view()),
    path('payments/<int:pk>/', SinglePaymentView.as_view()),
    path('company/<int:pk>/', CompanyDetailView.as_view()),



]







