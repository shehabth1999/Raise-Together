from django import forms
from .models import Multi_Picture, Rating


class MultiPictureForm(forms.ModelForm):
    class Meta:
        model = Multi_Picture
        fields = ['image']  # You can include other fields if needed

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']