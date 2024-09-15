from django.contrib import admin

# from Apis.models import Company, User
from django.contrib import admin
from .models import User, Company,Trips,Bus,Booking,Review,Favorite
# Register your models here.

admin.site.register(User)
admin.site.register(Company)

admin.site.register(Review)
admin.site.register(Trips)
admin.site.register(Bus)
admin.site.register(Booking)
admin.site.register(Favorite)






