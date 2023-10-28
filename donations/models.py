from django.db import models
from django.shortcuts import reverse
from accounts.models import MyUser
from projects.models import Project

class Donation(models.Model):

    amount = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    donator = models.ForeignKey(MyUser,null=True, blank=True,on_delete=models.CASCADE, related_name='donations')
    project = models.ForeignKey(Project,null=True, blank=True,on_delete=models.CASCADE, related_name='donations')
    
    @classmethod
    def all(cls) :
        return cls.objects.all()
    
    @classmethod
    def get(cls,id) :
        return cls.objects.get(id=id)
    