from django.urls import path 
from accounts.views import Register, Profile, Delete_Profile, activate_user, login_user, logout_user , change_password , edit_profile
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('register/', Register.as_view(), name = "account.create"),
    path('profile/', login_required( Profile.as_view()), name = "profile.view"),
    path('edit/', login_required(edit_profile), name = "profile.edit"),
    path('delete/', login_required(Delete_Profile.as_view()), name = "profile.delete"),
    path('login/', login_user , name='login'),
    path('logout/', logout_user , name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate_user, name='activate'),
    path('editPassword/', change_password, name='profile.edit.Password'),

]

