from django.db import models
from django.shortcuts import  reverse

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=100, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.name}"
  
  @classmethod
  def get_all_categories(cls):
    return  cls.objects.all()
  
  def get_show_url(self):
    return  reverse('category.detail', args=[self.id])