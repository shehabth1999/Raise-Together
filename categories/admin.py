from django.contrib import admin
from categories.models import Category
# Register your models here.

admin.site.register(Category)

# class adminCategory(admin.ModelAdmin):
#     list_display = ('name',)

# admin.site.register(Category, adminCategory)