from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()



class Twitt(models.Model):
    author = models.ForeignKey(User, related_name="twitts", on_delete=models.CASCADE)
    text = models.TextField(max_length=280)
    publish_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text[:10]


    @property
    def number_of_comments(self):
        return Comment.objects.filter(twitt_connected=self).count()



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    twitt_connected = models.ForeignKey(Twitt, on_delete=models.CASCADE)
    text = models.TextField(max_length=280)
    publish_date = models.DateTimeField(default=timezone.now)
