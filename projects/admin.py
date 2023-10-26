from django.contrib import admin
from .models import Project, Multi_Picture, Tag, Comment, ProjectReport, CommentReport


# Register your models here.
admin.site.register(Project)
admin.site.register(Multi_Picture)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(ProjectReport)
admin.site.register(CommentReport)