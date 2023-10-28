from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Project, Multi_Picture, Comment, CommentReport, Rating
from .forms import MultiPictureForm, ProjectForm, MultiPictureFormSet, TagFormSet, ProjectReportForm, RatingForm
from django.db.models import Count
from donations.forms import DonationModelForm
from django.contrib.auth.decorators import login_required


def all_project(request):
    projects = Project.objects.all()  # Retrieve all Project objects
    return render(request, 'projects/all_project.html', {'projects': projects})


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    comments = Comment.objects.filter(project=project)

    images = Multi_Picture.objects.filter(project=project)


    # Get the tags of the current project
    current_tags = project.tags.values_list('tag', flat=True)

     # Query for similar projects based on shared tags, excluding the current project
    similar_projects = Project.objects.exclude(id=project_id) \
        .filter(tags__tag__in=current_tags) \
        .annotate(tag_count=Count('tags__tag')) \
        .order_by('-tag_count')[:4]
    
    current_target = project.current_target
    total_target = project.total_target

    percentage = (current_target / total_target) * 100


    return render(request, 'projects/project_detail.html', {
        'project': project,
        'images': images,
        'comments': comments,
        'similar_projects': similar_projects,
        'percentage': percentage
    })





@login_required
def upload_multi_picture(request, project_id):
    project = Project.objects.get(pk=project_id)

    if request.method == 'POST':
        form = MultiPictureForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.project = project
            new_image.save()
            return redirect(f'/projects/project_detail/{project_id}', project_id=project_id)

    else:
        form = MultiPictureForm()

    # Pass the 'project' object to the template context along with its 'title'
    return render(request, 'projects/upload_multi_picture.html', {'project': project, 'form': form})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            images_formset = MultiPictureFormSet(request.POST, request.FILES, instance=project, prefix='images')
            tags_formset = TagFormSet(request.POST, instance=project, prefix='tags')
            if images_formset.is_valid() and tags_formset.is_valid():
                images_formset.save()
                tags_formset.save()
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = ProjectForm()
        images_formset = MultiPictureFormSet(prefix='images')
        tags_formset = TagFormSet(prefix='tags')
    return render(request, 'projects/forms/create.html', {'form': form, 'images_formset': images_formset, 'tags_formset': tags_formset})

@login_required
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
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
        images_formset = MultiPictureFormSet(instance=project, prefix='images')
        tags_formset = TagFormSet(instance=project, prefix='tags')
    return render(request, 'projects/forms/edit.html', {'form': form, 'images_formset': images_formset, 'tags_formset': tags_formset})



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



@login_required
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




@login_required
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