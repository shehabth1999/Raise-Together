from django.shortcuts import render
from django.http import HttpResponse
from categories.models import Category
from projects.models import Project

def index(request):
  categories= Category.get_all_categories()
  latest_projects = Project.objects.order_by('-created_at')[:5]
  latest_featured_projects = Project.objects.filter(is_featured=True).order_by('-created_at')[:5]
  return render(request, 'homepage/index.html', context={"categories":categories, 'latest_projects': latest_projects, 'latest_featured_projects': latest_featured_projects})