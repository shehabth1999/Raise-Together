from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from categories.models import Categoty





class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField(max_length=300)
    total_target = models.DecimalField(max_digits=10, decimal_places=2, default=250000)
    start_time = models.DateTimeField(auto_now_add=False,default=timezone.now)
    end_time = models.DateTimeField(auto_now=False,default=None)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    current_target = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # category = models.ForeignKey(Category, on_delete=models.PROTECT)
    def __str__(self):
        return self.title

class Tag(models.Model):
    name=models.CharField(max_length=100, unique=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tag',null=True)


    def __str__(self):
        return self.name

class Multi_Picture(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.project.title}: {self.rating}"
