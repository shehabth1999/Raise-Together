from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Project, Multi_Picture, Comment, CommentReport, Rating, Tag
from .forms import MultiPictureForm, ProjectForm, ProjectReportForm, RatingForm
from django.db.models import Count
from django.forms import modelformset_factory
from donations.forms import DonationModelForm
from django.contrib.auth.decorators import login_required


def all_project(request):
    projects = Project.objects.all()  # Retrieve all Project objects
    return render(request, 'projects/all_project.html', {'projects': projects})


def project_detail(request, project_id):

    project = get_object_or_404(Project, pk=project_id)
    comments = Comment.objects.filter(project=project)
    images = project.images.all()
    current_tags = project.tags.values_list('tag', flat=True)


    similar_projects = Project.objects.exclude(id=project_id) \
        .filter(tags__tag__in=current_tags) \
        .annotate(tag_count=Count('tags__tag')) \
        .order_by('-tag_count')[:4]


    return render(request, 'projects/project_detail.html', {
        'project': project,
        'images': images,
        'comments': comments,
        'similar_projects': similar_projects
    })




@login_required
def create_project(request):
    ImageFormSet = modelformset_factory(Multi_Picture, form=MultiPictureForm, extra=4)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Multi_Picture.objects.none())

        if project_form.is_valid() and formset.is_valid():
            project = project_form.save()

            # Process and associate tags with the project
            tags_input = project_form.cleaned_data['tags']
            tags_list = [tag.strip() for tag in tags_input.split(',')]  # Split tags by commas
            for tag in tags_list:
                tag_obj, created = Tag.objects.get_or_create(tag=tag, project=project)

            for form in formset:
                if form.cleaned_data:
                    image = form.cleaned_data.get('image')
                    img = Multi_Picture(project=project, image=image)
                    img.save()

            return redirect('projects:project_detail', project_id=project.id)
    else:
        project_form = ProjectForm()
        formset = ImageFormSet(queryset=Multi_Picture.objects.none())

    return render(request, 'projects/forms/create.html', {'project_form': project_form, 'formset': formset})

@login_required
def edit_project(request, project_id):
    # Get the project instance to edit
    project = get_object_or_404(Project, id=project_id)

    # Create an ImageFormSet for editing images
    ImageFormSet = modelformset_factory(Multi_Picture, form=MultiPictureForm, extra=3, max_num=3)

    if request.method == 'POST':
        # Create a ProjectForm instance with the updated data
        project_form = ProjectForm(request.POST, request.FILES, instance=project)

        # Create an ImageFormSet with the updated images
        formset = ImageFormSet(request.POST, request.FILES, queryset=Multi_Picture.objects.filter(project=project))

        if project_form.is_valid() and formset.is_valid():
            # Save the updated project details
            project = project_form.save()

            # Delete all existing project images
            project.images.all().delete()

            # Process and associate tags with the project
            tags_input = project_form.cleaned_data.get('tags')
            tags_list = [tag.strip() for tag in tags_input.split(',')]  # Split tags by commas
            for tag in tags_list:
                tag_obj, created = Tag.objects.get_or_create(tag=tag, project=project)

            for form in formset:
                if form.cleaned_data:
                    image = form.cleaned_data.get('image')
                    img = Multi_Picture(project=project, image=image)
                    img.save()

            return redirect('projects:project_detail', project_id=project.id)
    else:
        # Create a ProjectForm instance with the existing project data
        project_form = ProjectForm(instance=project)

        # Create an ImageFormSet with the existing project images
        formset = ImageFormSet(queryset=Multi_Picture.objects.filter(project=project))

    return render(request, 'projects/forms/edit.html',
                  {'project_form': project_form, 'formset': formset, 'project': project})

@login_required
def deleteProject(request, id):
    project = Project.objects.get(id=id)

    if request.method == 'POST':
        project.delete()
        return redirect('projects:all_project')
    return render(request,
                'projects/forms/delete.html',
                {'project': project})

@login_required
def add_comment(request, project_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        project = get_object_or_404(Project, pk=project_id)
        user = request.user
        comment = Comment(project=project, user=user, content=content)
        comment.save()
        project_id = project.pk
        return redirect(reverse('projects:project_detail', args=[project_id]))
    else:
        return render(request, 'projects/add_comment.html', {'project_id': project_id})




def report_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.project = project
            report.user = request.user
            report.save()
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = ProjectReportForm()
    return render(request, 'projects/report_project.html', {'form': form, 'project': project})





def report_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        report_content = request.POST.get('report_comment')

        user = request.user

        comment_report = CommentReport(comment=comment, user=user, report_comment=report_content)
        comment_report.save()

    return render(request, 'projects/report_comment.html')

@login_required
def rate_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    form = RatingForm()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data['rating']

             # Delete old rating for the same user if it exists
            Rating.objects.filter(user=request.user, project=project).delete()

            rating = Rating.objects.create(user=request.user, project=project, rating=rating_value)
            project.update_rating()  # Custom method in the Project model to update the average rating
            return redirect('projects:project_detail', project_id=project.id)

    return render(request, 'projects/rate_project.html', {'form': form, 'project': project})

@login_required
def myprojects(request):
    projects = Project.objects.filter(created_by = request.user)  
    return render(request, 'projects/all_project.html', {'projects': projects})