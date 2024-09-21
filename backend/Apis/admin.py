from django.contrib import admin
from .models import *
# Register your models here.


# Register the Admin model for admin interface
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_staff', 'is_superuser']


admin.site.register(User)
admin.site.register(Company)

admin.site.register(Review)
admin.site.register(Trips)
admin.site.register(Bus)
admin.site.register(Booking)
admin.site.register(Favorite)
admin.site.register(City)





