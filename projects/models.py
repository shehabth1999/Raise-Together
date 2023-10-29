from django.db import models
from django.shortcuts import reverse
from accounts.models import MyUser
from django.utils import timezone
from categories.models import Category


class Project(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Canceled', 'Canceled'),
        ('Completed', 'Completed'),
    ]
    title = models.CharField(max_length=200)
    details = models.TextField(max_length=300)
    total_target = models.DecimalField(max_digits=10, decimal_places=2, default=250000)
    start_time = models.DateTimeField(auto_now_add=False,default=timezone.now)
    end_time = models.DateTimeField(auto_now=False,default=None)
    current_target = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(MyUser,null=True , blank=True, on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name='projects')
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active',blank=True)

    def __str__(self):
        return self.title

    def update_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
            average_rating = round(average_rating, 2)
            self.rating = average_rating
            self.save()
            return average_rating
        self.rating = None
        return None

class Tag(models.Model):
    tag=models.CharField(max_length=100, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tags',null=True)


    def __str__(self):
        return f" Name of Project : {self.project.title} - Name of  tag is : {self.tag}"

class Multi_Picture(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/images/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Name of Project : {self.project.title} - {self.image}"
    
    def get_detail_url(self):
       return  reverse('project_detail', args=[self.id])
    
    def get_image_url(self):
        return f'/media/{self.image}'


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

    def __str__(self):
        return f"{self.project.title}: {self.rating}"

class CommentReport(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,default=None)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    report_comment = models.TextField()

    def __str__(self):
        return f"Comment Report for {self.comment}"


class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.comment}"
        