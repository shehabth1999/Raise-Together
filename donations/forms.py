from django import forms
from donations.models import  Donation
from projects.models import Project


class DonationModelForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']