
from django.urls import path
from donations.views import addDonation, deleteDonation, editDonation, donationHistory
urlpatterns = [
    path('', donationHistory, name="donations.history"),
    path('donate/', addDonation, name="donations.add"),
    path('delete/<int:id>', deleteDonation, name="donations.delete"),
    path('edit/<int:id>', editDonation, name="donations.edit")
]