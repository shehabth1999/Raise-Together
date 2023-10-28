from django.urls import path 
from accounts.views import Register, Profile, activate_user, login_user, logout_user , change_password , edit_profile, confirm_delete
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', Register.as_view(), name = "account.create"),
    path('profile/', login_required( Profile.as_view()), name = "profile.view"),
    path('edit/', login_required(edit_profile), name = "profile.edit"),
    path('delete/', confirm_delete, name = "profile.delete.confirm"),
    path('login/', login_user , name='login'),
    path('logout/', logout_user , name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate_user, name='activate'),
    path('editPassword/', change_password, name='profile.edit.Password'),
#     path('forgetPassword/', forget_password_page, name='account.forget.password'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset/password_reset_form.html'),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset/password_reset_complete.html'),
         name='password_reset_complete'),

    

]

