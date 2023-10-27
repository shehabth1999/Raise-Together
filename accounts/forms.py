from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import MyUser
from django.core.validators import RegexValidator

class Registeration(UserCreationForm):
    phone = forms.CharField(
        label='Phone Number',
        validators=[
            RegexValidator(
                regex=r'^01[0125][0-9]{8}$',
                message='Phone number must be 11 digits, and starts with 010/011/012/015',
                code='invalid_phone_number'
            ),])
    image = forms.ImageField(label='Profile Picture', help_text = '', required=False)

    class Meta:
        model = MyUser
        fields = ("first_name","last_name","email","username","password1","password2","phone","image")

    def clean_email(self):
            email = self.cleaned_data['email']
            if self.instance.email == email:
                return email  
            if MyUser.objects.filter(email=email).exists():
                raise forms.ValidationError("Email Already Exists.")
            return email
    
    def __init__(self, *args, **kwargs):
        super(Registeration, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = ''