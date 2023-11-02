from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from .models import Category
from .forms import CategoryForm
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        return render(self.request, 'categories/no_permission_template.html')

class CategoryListView(SuperuserRequiredMixin, View):
    template_name = 'categories/categories.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by('id')
        return render(request, self.template_name, {'categories': categories})


class CategoryDetailView(View):
    template_name = 'categories/show.html'

    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        return render(request, self.template_name, {'category': category})


class CategoryCreateView(SuperuserRequiredMixin, View):
    template_name = 'categories/create.html'

    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('category.list'))
        return render(request, self.template_name, {'form': form})


class CategoryUpdateView(SuperuserRequiredMixin, View):
    template_name = 'categories/edit.html'

    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(instance=category)
        return render(request, self.template_name, {'form': form, 'category': category})

    def post(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect(reverse('category.list'))
        return render(request, self.template_name, {'form': form, 'category': category})


class CategoryDeleteView(SuperuserRequiredMixin, View):
    template_name = 'categories/delete.html'

    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        return render(request, self.template_name, {'category': category})

    def post(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        if not category.projects.all():
            category.delete()
            return redirect(reverse('category.list'))
        messages.error(request, "Can't Remove! This Category Has Projects!")
        return redirect(reverse('category.list'))
