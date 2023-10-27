from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class MyUser(AbstractUser):
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='accounts/', blank=True, null=True, default='None')
    is_email_verified = models.BooleanField(default=False)
    activation_link_created_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
