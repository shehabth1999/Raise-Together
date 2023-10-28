from django import forms
from .models import Multi_Picture, Project, Tag, ProjectReport, CommentReport
from django.forms import inlineformset_factory


class MultiPictureForm(forms.ModelForm):
    class Meta:
        model = Multi_Picture
        fields = ['image']  # You can include other fields if needed


MultiPictureFormSet = inlineformset_factory(Project, Multi_Picture, fields=('image',), extra=1)
TagFormSet = inlineformset_factory(Project, Tag, fields=('tag',), extra=1)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }




class ProjectReportForm(forms.ModelForm):
    class Meta:
        model = ProjectReport
        fields = ['report_reason']
        widgets = {
            'report_reason': forms.Textarea(attrs={'rows': 3}),
        }




class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)


