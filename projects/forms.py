from django import forms
from .models import Multi_Picture, Project, Tag, ProjectReport, CommentReport, CommentReply
from django.forms import inlineformset_factory


class MultiPictureForm(forms.ModelForm):
    class Meta:
        model = Multi_Picture
        fields = ['image']  


MultiPictureFormSet = forms.modelformset_factory(
    Multi_Picture,
    form=MultiPictureForm,
    extra=1,
    max_num=10,  # Set a maximum number of images if needed
    validate_max=True,
)


# class ProjectForm(forms.ModelForm):
#     tags = forms.CharField(max_length=200, required=False, help_text="Enter tags separated by commas")

#     class Meta:
#         model = Project
#         # fields = ['title', 'details', 'total_target', 'start_time', 'end_time','category']
#         fields='__all__'
#         widgets = {
#             'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#             'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#             'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}),
#         }

class ProjectForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, required=False, help_text="Enter tags separated by commas")
    class Meta:
        model = Project
        fields = '__all__'
        title = forms.CharField(max_length=200, required=True)  # Make title field required
        details = forms.CharField(max_length=300, widget=forms.Textarea, required=True)  # Make details field required​​​​​​​​
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}),
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


class CommentReplyForm(forms.ModelForm):
    content = forms.CharField(label='Reply To Comment', widget=forms.Textarea)
    class Meta:
        model = CommentReply
        fields = ['content']
