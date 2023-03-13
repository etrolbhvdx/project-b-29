from django.db import models
from django.urls import reverse


class User(models.Model):
    def __str__(self):
        return self.email
    email = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)


class Message(models.Model):
    message_text = models.CharField(max_length=200)

    def __str__(self):
        return self.message_text
