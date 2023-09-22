from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.hashers import make_password

class UserManager(UserManager):


    def create_user(self, email, password, **extra):
        if not email:
            raise ValueError("the email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save()
        return user



    def create_superuser(self, email, password, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('is_active',True)

        if extra.get('is_staff') is not True:
            raise ValueError('superuser must be staff true')
        if extra.get('is_superuser') is  not True:
            raise ValueError('superuser must have is_superuser=True')
        return self.create_user(email, password, **extra)


class CustomUser(AbstractUser):


    email = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30,blank=True)
    username = models.CharField(max_length=30, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.username = self.name+' user'
        return super().save(*args,**kwargs)


