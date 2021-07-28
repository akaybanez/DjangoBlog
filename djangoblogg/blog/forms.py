from django.forms import forms
from django.db import models
from django.forms import ModelForm
from .models import Blogs, Comments


class BlogForm(ModelForm):
    class Meta:
        model = Blogs
        fields = ['title', 'content']


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
