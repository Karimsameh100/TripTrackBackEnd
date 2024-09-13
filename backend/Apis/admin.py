from django.contrib import admin

# from Apis.models import Company, User
from django.contrib import admin
from .models import User, Company
# Register your models here.

admin.site.register(User)
admin.site.register(Company)
# admin.site.register(Passenger)
# admin.site.register(Trip)
# admin.site.register(Schedual)