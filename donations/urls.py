
from django.urls import path
from donations.views import addDonation,donationHistory,projectDonations
urlpatterns = [
    path('<int:project_id>', projectDonations, name="donations.project"),
    path('history/', donationHistory, name="donations.history"),
    path('donate/<int:project_id>', addDonation, name="donations.add"),
]