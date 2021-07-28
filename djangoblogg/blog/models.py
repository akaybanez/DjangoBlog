from django.db import models
from users.models import CustomUser

import datetime

# Create your models here.


class Blogs(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField()
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True) #first creation
    date_updated = models.DateTimeField(auto_now=True) #automatic update

    def __str__(self):  # called in admin side
        return self.title


class Likes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
