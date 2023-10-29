from django.shortcuts import render, redirect,reverse, get_object_or_404
from donations.models import Donation
from donations.forms import DonationModelForm
from django.contrib import messages
from projects.models import Project
from django.contrib.auth.decorators import login_required
from accounts.models import MyUser


@login_required
def donationHistory(request):
    donations = Donation.objects.filter(donator=request.user)
    # donations = request.user.donations
    return render(request,'donations/history.html',{'donations':donations})

@login_required
def projectDonations(request,project_id):
    project = get_object_or_404(Project, id=project_id)
    donations = project.donations
    donations = Donation.objects.filter(project=project)
    return render(request,'donations/projectDonations.html',{'donations':donations, 'project':project})

@login_required()
def addDonation(request, project_id):
    form = DonationModelForm()
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = DonationModelForm(request.POST)
        if form.is_valid():
            donation = form.save() 
            donation.donator = request.user
            donation.project = project
            donation.save()
            project.current_target = project.current_target + donation.amount
            project.save()
            messages.success(request, 'Donated successfully')
            return redirect(reverse('projects:project_detail', args=[project_id]))
    return render(request, 'donations/forms/donate.html',context={"form": form})

def searchDonations(request):
    search_type = request.GET.get('search_type', 'project')
    search_query = request.GET.get('search_query', '')
    donations = []
    if search_query:
        if search_type == 'project':
            donations = Donation.objects.filter(id__in=Project.objects.filter(title__icontains=search_query).values('donations'),donator=request.user)
        elif search_type == 'amount':
            donations = Donation.objects.filter(amount=search_query,donator=request.user)
    return render(request,'donations/history.html',{'donations':donations})

def searchDonations_project(request,project_id):
    project = Project.get(project_id)
    search_type = request.GET.get('search_type', 'donator')
    search_query = request.GET.get('search_query', '')
    donations = []
    if search_query:
        if search_type == 'donator':
            donations = Donation.objects.filter(id__in=MyUser.objects.filter(username__icontains=search_query).values('donations'),project=project)
        elif search_type == 'amount':
            donations = Donation.objects.filter(amount=search_query,project=project)
    return render(request,'donations/projectDonations.html',{'donations':donations, 'project':project})