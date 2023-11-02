"""
URL configuration for RaiseTogether project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from categories.views import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from django.contrib.auth.decorators import user_passes_test

urlpatterns = [
    path('', CategoryListView.as_view(), name='category.list'),
    path('<int:category_id>/', CategoryDetailView.as_view(), name='category.detail'),
    path('create/', CategoryCreateView.as_view(), name='category.create'),
    path('edit/<int:category_id>/', CategoryUpdateView.as_view(), name='category.edit'),
    path('delete/<int:category_id>/', CategoryDeleteView.as_view(), name='category.delete'),
]
