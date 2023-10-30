from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from django.core.validators import URLValidator


class MyUser(AbstractUser):
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='accounts/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    activation_link_created_at = models.DateTimeField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    country = CountryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
