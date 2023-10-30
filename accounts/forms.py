from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import MyUser
from django.core.validators import RegexValidator
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils import timezone


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


class EditProfile(forms.ModelForm):
    class Meta:
        model = MyUser
        fields =  [ "first_name","last_name","phone","image","birth_date","facebook_profile","country"]
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }
    def clean_Birthdate(self):
        birthdate = self.cleaned_data['Birthdate']
        if birthdate > timezone.now().date():
            raise ValidationError("Birthdate cannot be in the future.")
        return birthdate
    


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = MyUser
        fields = ['old_password', 'new_password1', 'new_password2']

    old_password = forms.CharField(
    label="Old Password",
    widget=forms.PasswordInput(),
    help_text=""
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(),
        help_text=""
    )
    new_password12 = forms.CharField(
        label="New Password Confirmation",
        widget=forms.PasswordInput(),
        help_text=""
    )
