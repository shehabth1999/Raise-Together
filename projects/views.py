
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Project, Multi_Picture, Rating
from .forms import MultiPictureForm, RatingForm
from projects.forms import ProjectForm ,MultiPictureFormSet ,TagFormSet
from django.views import View





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




# def editForm(request, id):
#     project = Project.objects.get(id=id)
#     form = ProjectForm(instance = project)
#     if request.method== 'POST':
#         form =  ProjectForm(request.POST, request.FILES, instance = project)
#         if form.is_valid():
#             form.save()
#             return redirect('project_detail', project_id=project.id)

#     return  render(request,  'projects/forms/edit.html',
#                    context={"form":form})

# def create_project(request):
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             project = form.save()
#             return redirect('project_detail', project_id=project.id)
#     else:
#         form = ProjectForm()
#     return render(request, 'projects/forms/create.html', {'form': form})

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            images_formset = MultiPictureFormSet(request.POST, request.FILES, instance=project, prefix='images')
            tags_formset = TagFormSet(request.POST, instance=project, prefix='tags')
            if images_formset.is_valid() and tags_formset.is_valid():
                images_formset.save()
                tags_formset.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
        images_formset = MultiPictureFormSet(prefix='images')
        tags_formset = TagFormSet(prefix='tags')
    return render(request, 'projects/forms/create.html', {'form': form, 'images_formset': images_formset, 'tags_formset': tags_formset})

def editForm(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            images_formset = MultiPictureFormSet(request.POST, request.FILES, instance=project, prefix='images')
            tags_formset = TagFormSet(request.POST, instance=project, prefix='tags')
            if images_formset.is_valid() and tags_formset.is_valid():
                images_formset.save()
                tags_formset.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
        images_formset = MultiPictureFormSet(instance=project, prefix='images')
        tags_formset = TagFormSet(instance=project, prefix='tags')
    return render(request, 'projects/forms/edit.html', {'form': form, 'images_formset': images_formset, 'tags_formset': tags_formset})


# def deleteProject(request, id):
#     project = Project.objects.get(id=id)
#     project.delete()
#     url = reverse('all_project')
#     return redirect(url)

# listings/views.py

def deleteProject(request, id):
    project = Project.objects.get(id=id)

    if request.method == 'POST':
        project.delete()
        return redirect('all_project')
    return render(request,
                'projects/forms/delete.html',
                {'project': project})