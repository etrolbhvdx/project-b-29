from django.db import models

class User(models.Model):
    def __str__(self):
        return self.email
    email = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
