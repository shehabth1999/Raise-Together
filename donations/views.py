from django.shortcuts import render, redirect,reverse
from donations.models import Donation
from donations.forms import DonationModelForm, SearchForm
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def donationHistory(request):
    donations = Donation.all()
    userDonations=[]
    for donation in donations :
        if donation.donator and donation.donator.id == request.user.id :
            userDonations.push(donation)
    return render(request,'donations/history.html',{'donations':userDonations})

@login_required()
def addDonation(request):
    form = DonationModelForm()
    if request.method == 'POST':
        form = DonationModelForm(request.POST)
        if form.is_valid():
            donation = form.save() 
            donation.donator = request.user
            donation.save()
            return redirect(donation.details_url())
    return render(request, 'donations/forms/create.html',context={"form": form})

@login_required()
def editDonation(request, id):
    donation = Donation.get(id)
    if donation.donator and donation.donator.id == request.user.id:
        form = DonationModelForm(instance=donation)
        if request.method== 'POST':
            form =  DonationModelForm(request.POST, instance=donation)
            if form.is_valid():
                form.save()
                return redirect(donation.details_url())
        return  render(request, 'donations/forms/edit.html', context={"form":form})
    messages.error(request, 'only owner can edit his donation')
    return redirect(donation.details_url())

@login_required()
def deleteDonation(request, id):
    donation = Donation.get(id)
    if donation.donator and donation.donator.id == request.user.id:
        donation.delete()
        return redirect(reverse('donations.index'))
    messages.error(request, 'only owner can delete his donation')
    return redirect(donation.details_url())
