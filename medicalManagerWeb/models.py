from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class MedicalUser(AbstractUser):
    display_name = models.CharField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class UserSignUpRequest(models.Model):
    display_name = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    email = models.EmailField()


class KeyToken(models.Model):
    user = models.ForeignKey(MedicalUser, on_delete=models.CASCADE)
    public_key = models.CharField(max_length=1000, null=True)
    refresh_token = models.CharField(max_length=1000, null=True)