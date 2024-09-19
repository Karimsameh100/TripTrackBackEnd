# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator


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


class AllUsers(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ('company', 'Company'),
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user_type}: {self.name}"

class Admin(AllUsers):
    allusers_ptr = models.OneToOneField(AllUsers,on_delete=models.CASCADE,parent_link=True,)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

class User(AllUsers):
    allusers_ptr = models.OneToOneField(AllUsers,on_delete=models.CASCADE,parent_link=True,)
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

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def has_module_perms(self, app_label):
        return self.is_superuser


class Bus(models.Model):
    busNumber = models.CharField(max_length=255)
    busType = models.CharField(max_length=255)
    busCapacity = models.IntegerField()

    def __str__(self):
        return self.busNumber



class Booking(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now=True)
    status = models.CharField(max_length=255, default='Pending')
    numberOfPlaces = models.IntegerField(default=1)
    totalFare = models.IntegerField()
    pickupLocation = models.CharField(max_length=255)
    dropLocation = models.CharField(max_length=255)


    def __str__(self):
        return self.status
    


class Trips(models.Model):
    tripNumber=models.IntegerField(unique=True)
    date=models.DateField()
    avilabalPlaces=models.IntegerField(null=False)
    departuerStation=models.CharField(max_length=50,null=False)
    destinationStation=models.CharField(max_length=50,null=False)
    departuerTime=models.TimeField()
    destinationTime=models.TimeField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=50,default="Pandding")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE)
    book = models.ForeignKey(Booking,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.book.status


class Company(AllUsers):
    allusers_ptr = models.OneToOneField(AllUsers,on_delete=models.CASCADE,parent_link=True,)
    about = models.TextField(default="Default about information")
    commercial_register = models.FileField(upload_to='documents/')
    work_license = models.FileField(upload_to='documents/')
    certificates = models.FileField(upload_to='documents/')
    trips = models.ManyToManyField('Trips', related_name='companies', blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, default=1)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name


class Review(models.Model):
    ReviewCustomerDetails = models.ForeignKey(User, on_delete=models.CASCADE)
    Review = models.TextField()
    ReviewCustomerRate = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f'Review by {self.ReviewCustomerDetails.email} with rate {self.ReviewCustomerRate}'
3    
    
    
class Favorite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_id = models.ForeignKey(Trips, on_delete=models.CASCADE, related_name='favorites')
    



class City(models.Model):
    Reviews = models.ManyToManyField(Review, related_name='cities')
    companies = models.ManyToManyField(Company, related_name='cities')
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    image = models.URLField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.city