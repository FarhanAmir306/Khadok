from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.



class CustomUser(AbstractUser):
   
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('RIDER', 'Rider'),
        ('CUSTOMER', 'Customer')
    )
   
    username = None
    email = models.EmailField(_("email address"), unique=True)
    avatar=models.ImageField(upload_to='accounts/images/',null=True,blank=True)
    phone=models.CharField(max_length=14,null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    password=models.CharField(max_length=20,null=True,blank=True)
    confirm_password=models.CharField(max_length=20,null=True,blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True, default='Customer')


    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ['first_name','last_name','avatar','phone','address','password','confirm_password']
    REQUIRED_FIELDS = []


    objects = CustomUserManager()

    def __str__(self):
        return self.email