from django.shortcuts import render
from django.http import HttpResponse
from categories.models import Category

def index(request):
  categories= Category.get_all_categories()
  return render(request, 'homepage/index.html', context={"categories":categories})
