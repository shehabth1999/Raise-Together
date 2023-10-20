from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='media/accounts/', blank=True, null=True)
