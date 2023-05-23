from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager as DefaultUserManager

class UserManager(DefaultUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    objects = UserManager()

    def __str__(self):
        return self.username