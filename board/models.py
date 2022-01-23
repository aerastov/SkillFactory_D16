from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField


class Post(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    CAT = (('tank', 'Танк'), ('heal', 'Хил'))
    category = models.CharField(max_length=10, choices=CAT, verbose_name='Категория')
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256, verbose_name='Название')
    text = RichTextField()


class Reply(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    status = models.BooleanField(default=False)
