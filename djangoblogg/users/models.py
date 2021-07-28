from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager #calls CustomManager class in managers.py

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True) #identifying field
    
    USERNAME_FIELD = 'email' #overrides username field
    REQUIRED_FIELDS = [] #REQUIRED_FIELDS must contain all required fields on your user model, but should not contain the USERNAME_FIELD or password as these fields will always be prompted for.

    objects = CustomUserManager()

    def __str__(self):
        return self.email