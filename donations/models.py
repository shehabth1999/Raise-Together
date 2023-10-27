from django.db import models

from django.db import models
from django.shortcuts import reverse
from accounts.models import MyUser
from projects.models import Project

class Donation(models.Model):

    amount = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    donator = models.ForeignKey(MyUser,null=False, blank=True,on_delete=models.CASCADE, related_name='donations')
    project = models.ForeignKey(Project,null=False, blank=True,on_delete=models.CASCADE, related_name='donations')
    
    def details_url (self):
        return reverse('donation.details', args=[self.id])
    
    def delete_url (self):
        return reverse('donation.delete', args=[self.id])
    
    def edit_url (self):
        return reverse('donation.edit', args=[self.id])
    
    @classmethod
    def all(cls) :
        return cls.objects.all()
    
    @classmethod
    def get(cls,id) :
        return cls.objects.get(id=id)
    