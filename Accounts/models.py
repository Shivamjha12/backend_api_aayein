from django.db import models
from django.contrib.auth.models import AbstractUser
from Accounts.managers import CustomUserManager

class User(AbstractUser):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Media/user/profilepictures/',null=True,blank=True)
    is_google = models.BooleanField(default=False)
    google_image_url = models.URLField(max_length=255, null=True, blank=True)
    google_id = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=10)
    intrests = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    username = None
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()


    