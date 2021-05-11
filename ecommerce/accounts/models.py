from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    name = models.CharField(max_length=80)
    email= models.EmailField(max_length=100,unique=True)

    date = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=10,choices=(('Male','Male'),('Female','Female'),('Others','Others')))
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20)

    def __str__(self):
        return self.email

class GuestEmail(models.Model):
    email       = models.EmailField()

    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email





