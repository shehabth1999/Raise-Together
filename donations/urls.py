
from django.urls import path
from donations.views import addDonation,donationHistory,projectDonations,searchDonations,searchDonations_project
urlpatterns = [
    path('<int:project_id>', projectDonations, name="donations.project"),
    path('history/', donationHistory, name="donations.history"),
    path('donate/<int:project_id>', addDonation, name="donations.add"),
    path('search/', searchDonations, name='donations.search'),
    path('search_project/<int:project_id>', searchDonations_project, name='donations.search_project'),
]