# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class UserManager(BaseUserManager):
#     def create_user(self, email, name, phone_number, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, name=name, phone_number=phone_number, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user



# class User(AbstractBaseUser):
#     name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=20)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     confirm_password = models.CharField(max_length=255)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name', 'phone_number', 'confirm_password']
    
    
#     objects = UserManager()

#     def __str__(self):
#         return self.email

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    commercial_register = models.FileField(upload_to='documents/')
    work_license = models.FileField(upload_to='documents/')
    certificates = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, phone_number, password, **extra_fields)



class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'confirm_password']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f'Review by {self.user.email} with rate {self.rate}'
    
    
    
# ====trips , schedule , passenger 
# class Passenger(models.Model):
#     user_name=models.CharField(max_length=50)
#     phone=models.CharField(max_length=20)
#     city=models.CharField(max_length=50)
#     street=models.CharField(max_length=50)
#     SSN=models.IntegerField()
#     # password=models.IntegerField(max_length=20)
#     email=models.EmailField(max_length=30)
    
    
#     def _str_(self):
#         return self.user_name  

# class Trip(models.Model):
#     passenger_id = models.ManyToManyField(Passenger) 
#     date = models.DateField()
#     avilable_places = models.IntegerField()
#     departure_station = models.CharField(max_length=50)
#     stop_stations = models.CharField(max_length=50) 
#     departure_time = models.TimeField(max_length=50)
#     stop_time = models.TimeField(max_length=50) 
#     price = models.FloatField()
#     status = models.BooleanField()

#     def _str_(self):
#         return self.date
    

# class Schedual(models.Model):
#     passenger_id = models.ForeignKey(Passenger ,on_delete=models.CASCADE,null=True,blank=True)  
#     trip_id = models.ForeignKey(Trip ,on_delete=models.CASCADE,null=True,blank=True)  

