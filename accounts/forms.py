from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import MyUser

class Registeration(UserCreationForm):
    phone = forms.IntegerField(label='Phone name')
    image = forms.ImageField(label='Profile Picture')

    class Meta:
        model = MyUser
        fields = ("first_name","last_name","email","username","password1","password2","phone","image")
        # fields = '__all__'

    def clean_email(self):
            email = self.cleaned_data['email']
            if self.instance.email == email:
                return email  
            if MyUser.objects.filter(email=email).exists():
                raise forms.ValidationError("Email Already Exists.")
            return email