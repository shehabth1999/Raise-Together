from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import DetailView , DeleteView, UpdateView
from django.contrib.auth.models import  User
from accounts.forms import  Registeration
# Create your views here.

class Register(CreateView):
    model = User
    template_name = 'accounts/registeration.html'
    form_class = Registeration
    success_url = reverse_lazy('profile')

class Profile(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    def get_object(self, queryset=None):
        return self.request.user #return the currently logged-in user.
