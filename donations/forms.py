from django import forms
from donations.models import  Donation

class DonationModelForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'

class SearchForm(forms.Form):
    find = forms.DateField(required=False)