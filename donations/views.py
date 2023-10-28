from django.shortcuts import render, redirect,reverse, get_object_or_404
from donations.models import Donation
from donations.forms import DonationModelForm
from django.contrib import messages
from projects.models import Project
from django.contrib.auth.decorators import login_required


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
    return render(request,'donations/projectDonations.html',{'donations':donations})

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