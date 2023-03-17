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


class Offering(models.Model):
    section = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    enrollment = models.CharField(max_length=200)
    if_full = models.BooleanField(default=False)

    def __str__(self):
        return self.section