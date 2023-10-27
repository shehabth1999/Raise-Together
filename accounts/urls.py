from django.urls import path , include
from accounts.views import Register, Profile, Edit_Profile, Delete_Profile, activate_user, login_user, logout_user
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('register/', Register.as_view(), name = "account.create"),
    path('profile/', login_required( Profile.as_view()), name = "profile.view"),
    path('edit/', login_required(Edit_Profile.as_view()), name = "profile.edit"),
    path('delete/', login_required(Delete_Profile.as_view()), name = "profile.delete"),
    path('login/', login_user , name='login'),
    path('logout/', logout_user , name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate_user, name='activate'),

]

