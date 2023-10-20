from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import DetailView , DeleteView, UpdateView
from accounts.models import MyUser
from accounts.forms import  Registeration
# Create your views here.

class Register(CreateView):
    model = MyUser
    template_name = 'accounts/registeration.html'
    form_class = Registeration
    success_url = reverse_lazy('profile')

class Profile(DetailView):
    model = MyUser
    template_name = 'accounts/profile.html'
    def get_object(self, queryset=None):
        return self.request.user #return the currently logged-in user.
