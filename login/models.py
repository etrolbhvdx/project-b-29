from django.db import models
from django.urls import reverse


class User(models.Model):
    def __str__(self):
        return self.email
    email = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)


class Message(models.Model):
    message_text = models.CharField(max_length=200)
    school_name = models.CharField(max_length=200,default="uva")
    equivalency_name = models.CharField(max_length=200,default="None")

    def __str__(self):
        return "Class="+self.message_text+", School="+self.school_name+", Equivalency="+self.equivalency_name


class Offering(models.Model):
    section = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    enrollment = models.CharField(max_length=200)
    if_full = models.BooleanField(default=False)

    def __str__(self):
        return self.section


class Transfer(models.Model):
    transferClass = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    transferCredits = models.CharField(max_length=200)
    UVAClass = models.CharField(max_length=200)
    UVACredits = models.CharField(max_length=200)
class ApprovedTransfer(models.Model):
    class_name = models.CharField(max_length=200)
    school_name = models.CharField(max_length=200, default="uva")
    equivalency_name = models.CharField(max_length=200, default="None")

    def __str__(self):
        return "Class="+self.class_name+", School="+self.school_name+", Equivalency="+self.equivalency_name
