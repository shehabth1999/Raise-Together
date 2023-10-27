from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from categories.models import Category
from projects.models import Project, Rating
from django.utils import timezone

def index(request):
  categories= Category.get_all_categories()
  top_rated_projects = Project.objects.filter(rating__isnull=False, end_time__gt=timezone.now()).order_by('-rating')[:5]
  latest_projects = Project.objects.order_by('-created_at')[:5]
  latest_featured_projects = Project.objects.filter(is_featured=True).order_by('-created_at')[:5]
  return render(request, 'homepage/index.html', context={"categories":categories, 'latest_projects': latest_projects, 'latest_featured_projects': latest_featured_projects, 'top_rated_projects':top_rated_projects})

def search_projects(request):
    search_type = request.GET.get('search_type', 'title')
    search_query = request.GET.get('search_query', '')

    projects = []

    if search_query:
        if search_type == 'title':
            projects = Project.objects.filter(title__icontains=search_query)
        elif search_type == 'tag':
            projects = Project.objects.filter(tag__name__icontains=search_query)

    context = {
        'search_type': search_type,
        'search_query': search_query,
        'projects': projects
    }
    return render(request, 'search/search.html', context)