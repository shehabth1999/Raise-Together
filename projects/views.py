
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Project, Multi_Picture, Rating
from .forms import MultiPictureForm, RatingForm


# Create your views here.


def all_project(request):
    projects = Project.objects.all()  # Retrieve all Project objects
    return render(request, 'projects/all_project.html', {'projects': projects})


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Retrieve all images related to the project
    images = Multi_Picture.objects.filter(project=project)

    return render(request, 'projects/project_detail.html', {'project': project, 'images': images})


def upload_multi_picture(request, project_id):
    project = Project.objects.get(pk=project_id)

    if request.method == 'POST':
        form = MultiPictureForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.project = project
            new_image.save()
            return redirect('project_detail', project_id=project_id)

    else:
        form = MultiPictureForm()

    # Pass the 'project' object to the template context along with its 'title'
    return render(request, 'projects/upload_multi_picture.html', {'project': project, 'form': form})


def add_rating(request, project_id):
    project = Project.objects.get(pk=project_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.project = project
            rating.save()
            return redirect('project_detail', project_id=project_id)

    else:
        form = RatingForm()

    return render(request, 'projects/add_rating.html', {'form': form, 'project': project})