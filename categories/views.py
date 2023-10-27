from django.shortcuts import render
from django.views.generic import DetailView
from categories.models import Category

# Create your views here.

class CategoryDetails(DetailView):
  model = Category
  template_name = 'categories/show.html'
  context_object_name = 'category'