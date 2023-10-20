from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings


class MyUser(AbstractUser):
    phone = models.IntegerField(default=1)
    image = models.ImageField(upload_to='media/accounts/',blank=True,null=True)
    # class Meta(User.Meta):
    #     swappable = 'AUTH_USER_MODEL'

# user = AbstractUser()

