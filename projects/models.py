from django.db import models
from django.shortcuts import reverse
from accounts.models import MyUser
from django.utils import timezone
from categories.models import Category
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField(max_length=300)
    total_target = models.DecimalField(max_digits=10, decimal_places=2, default=250000)
    start_time = models.DateTimeField(auto_now_add=False,default=timezone.now)
    end_time = models.DateTimeField(auto_now=False,default=None)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=None)
    current_target = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def update_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
            self.rating = round(average_rating, 2)
        else:
            self.rating = None
        self.save()

class Tag(models.Model):
    tag=models.CharField(max_length=100, unique=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tag',null=True)


    def __str__(self):
        return self.tag

class Multi_Picture(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)




    def get_detail_url(self):
       return  reverse('project_detail', args=[self.id])




class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments' )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.project.title if self.project else 'Unknown Project'}"


class ProjectReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    report_reason = models.TextField()

    def __str__(self):
        return f"Report for {self.project.title} by {self.user.username}"
    
class Rating(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE ,related_name='ratings')
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)