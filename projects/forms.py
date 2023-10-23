from django import forms
from projects.models import  Project ,Multi_Picture, Rating ,Tag
from django.forms import inlineformset_factory


class MultiPictureForm(forms.ModelForm):
    class Meta:
        model = Multi_Picture
        fields = ['image']  # You can include other fields if needed

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']

# class createProjectForm(forms.Form):
#   title = forms.CharField(max_length=200)
#   details = forms.CharField(max_length=300,required=True)
#   total_target = forms.DecimalField(max_digits=10, decimal_places=2 )
#   end_time = forms.DateTimeField()
#   current_target = forms.DecimalField(max_digits=10, decimal_places=2)

# class ProjectModelForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = '__all__'  

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'start_time', 'end_time', 'created_by', 'current_target']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

MultiPictureFormSet = inlineformset_factory(Project, Multi_Picture, fields=('image',), extra=1)
TagFormSet = inlineformset_factory(Project, Tag, fields=('tag',), extra=1)