from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from categories.models import Category
from projects.models import Project
from RaiseTogether.forms import SearchForm

def index(request):
  categories= Category.get_all_categories()
  latest_projects = Project.objects.order_by('-created_at')[:5]
  latest_featured_projects = Project.objects.filter(is_featured=True).order_by('-created_at')[:5]
  return render(request, 'homepage/index.html', context={"categories":categories, 'latest_projects': latest_projects, 'latest_featured_projects': latest_featured_projects})

def search_projects(request):
    form = SearchForm(request.GET)
    projects = Project.objects.none()

    if form.is_valid():
        title = form.cleaned_data['title']
        tag = form.cleaned_data['tag']

        if title:
            projects |= Project.objects.filter(title__icontains=title)

        if tag:
            projects |= Project.objects.filter(Q(tag__name__icontains=tag) | Q(tag__name__iexact=tag))

    context = {
        'form': form,
        'projects': projects
    }

    return render(request, 'search/search.html', context)