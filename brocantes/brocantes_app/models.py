from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk or not check_password(self.password, self.password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
