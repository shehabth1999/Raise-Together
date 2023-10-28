from django.utils import timezone
import threading
from django.shortcuts import render,redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView , DeleteView, UpdateView
from accounts.models import MyUser
from accounts.forms import  Registeration ,EditProfile , CustomPasswordChangeForm
from django.views import View
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import auth_user_should_not_access
import re
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from django.contrib.auth.hashers import check_password
from projects.models import Project
from donations.models import Donation




# Create your views here.

# class EmailThread(threading.Thread):
#     def __init__(self, email):
#         self.email = email
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email.send()
        
def send_activation_email(user, request):
        current_site = get_current_site(request)
        email_subject = 'Activate your account'
        email_body = render_to_string('registration/activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email = EmailMessage(subject=email_subject, body=email_body,
                             from_email=settings.EMAIL_FROM_USER,
                             to=[user.email]
                             )
        user.activation_link_created_at = timezone.now()
        print("Activation Link Creation Time:", user.activation_link_created_at)
        user.save()
        print("Activation Link Creation Time (after save):", user.activation_link_created_at)
        email.send()
        print("Email sent successfully.")
    # if not settings.TESTING:
    #     EmailThread(email).start()

def activate_user(request, uidb64, token):
    uid = force_bytes(urlsafe_base64_decode(uidb64))
    user = MyUser.objects.get(pk=uid)
    if user and generate_token.check_token(user, token):
        expiration_time = timezone.timedelta(minutes=1)
        print("Current Time:", timezone.now())
        print("Activation Link Creation Time:", user.activation_link_created_at)
        
        if user.activation_link_created_at and timezone.now() - user.activation_link_created_at < expiration_time:
            print("Activation link has expired.")
            return render(request, 'registration/activate-failed.html', {"user": user, "reason": "Activation link expired"})
        
        user.is_email_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))

    return render(request, 'registration/activate-failed.html', {"user": user})

class Register(View):
    template_name = 'accounts/registration.html'
    def get(self, request):
        
        if request.user.username:
            print( request.user)
            return redirect('homepage.index')

        form = Registeration()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = Registeration(request.POST)
        if form.is_valid():
            if 'image' in request.FILES:
                form = Registeration(request.POST, request.FILES)
                user = form.save()
            else:
                user = form.save()
            
            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS, 'Registration successful. We sent you an email to verify your account')
            return redirect('login')
        return render(request, self.template_name, {'form': form})
    
#-----------------------------------------------------------------------------------------

# @auth_user_should_not_access
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Basic email format check using regex
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            messages.error(request, 'Email Is Not Vaild')
            return redirect('login')
        
        user = authenticate(request, username=email, password=password)
        
        if user and not user.is_email_verified:
            messages.error(request, 'Email is not verified, please check your email inbox')
            return redirect('login')

        if not user:
            messages.error(request, 'Invalid credentials, try again')
            return redirect('login')
        
        
        login(request, user)
        return redirect('homepage.index')

    if request.user.username:
        print( request.user)
        return redirect('homepage.index')
    
    return render(request, 'registration/login.html')
    
    
def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS,
                         'Successfully logged out')
    return redirect(reverse('login'))


#-----------------------------------------------------------------------------------------

class Profile(DetailView):
    model = MyUser
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return self.request.user  

    def get_context_data(self, **kwargs):
        
        context = super(Profile, self).get_context_data(**kwargs)
        user = self.request.user

        if Project.objects.filter(created_by=user).exists():
            user_projects = Project.objects.filter(created_by=user)
            context['user_projects'] = user_projects

        if Donation.objects.filter(donator=user).exists():
            user_donations = Donation.objects.filter(donator=user)
            context['user_donations'] = user_donations


        return context
#-----------------------------------------------------------------------------------------

# class Edit_Profile(UpdateView):
#     model= MyUser
#     template_name = 'registration/edit_profile.html'
#     form_class = EditProfile
#     success_url = reverse_lazy("profile.view")
#     def get_object(self, queryset=None):
#         return self.request.user #return the currently logged-in user.
    
#-----------------------------------------------------------------------------------------

def edit_profile(request):
    if request.method == "POST":
        if request.FILES :
            form = EditProfile(request.POST, request.FILES, instance=request.user)
        else:
            form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():  
            if request.POST["birth_date"] :
                birth_date_str = request.POST.get("birth_date")
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date() 
                if birth_date > timezone.now().date():
                    messages.warning(request, 'Please enter a valid date of birth!')
                    return render(request, "registration/edit_profile.html", {'form': form})
            form.save()
            print(request.POST["birth_date"])
            return redirect('profile.view') 
    else:
        form = EditProfile(instance=request.user) 
    return render(request, "registration/edit_profile.html", {'form': form})

#-----------------------------------------------------------------------------------------
    
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile.view')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'registration/edit_password.html', {'form': form})
#-----------------------------------------------------------------------------------------

# class Delete_Profile(DeleteView):
#     model= MyUser
#     template_name = 'registration/delete_profile.html'
#     success_url = reverse_lazy("account.create")
#     def get_object(self, queryset=None):
#         return self.request.user #return the currently logged-in user.    

#-----------------------------------------------------------------------------------------

def confirm_delete(request):
    if request.method == 'POST':
        confirm_password = request.POST.get('confirm_password')
        user = request.user
        if check_password(confirm_password, user.password):
            user.delete()
            messages.success(request,"your account deleted, Thank you for your time with us")
            return redirect('login')
        messages.error(request, 'Incorrect password, Profile deletion failed.')
        return redirect('profile.delete.confirm')
    return render(request, 'accounts/confirm_delete.html')      

#-----------------------------------------------------------------------------------------    
# def send_reset_password_email(user, request):
#         current_site = get_current_site(request)
#         email_subject = 'Reset Your Password'
#         email_body = render_to_string('registration/reset_password.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': generate_token.make_token(user)
#         })
#         email = EmailMessage(subject=email_subject, body=email_body,
#                              from_email=settings.EMAIL_FROM_USER,
#                              to=[user.email]
#                              )
#         print("Email sent successfully.")
# #-----------------------------------------------------------------------------------------

# def forget_password_page(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')

#         try:
#             user = MyUser.objects.get(email=email)
#             send_reset_password_email(user, request)
#             messages.success(request, f'We sent you an email to reset your password: {user.email}')
#             return redirect('login')

#         except MyUser.DoesNotExist:
#             messages.error(request, f'The Email {email} did not match any account, please try again')
#             return redirect('account.forget.password')

#     return render(request, 'registration/forget_password_page.html')