from django.utils import timezone
import threading
from django.shortcuts import render,redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView , DeleteView, UpdateView
from accounts.models import MyUser
from accounts.forms import  Registeration
from django.views import View
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import auth_user_should_not_access
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseBadRequest

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
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = MyUser.objects.get(pk=uid)
    if user and generate_token.check_token(user, token):
        expiration_time = timezone.timedelta(minutes=1)
        print("Current Time:", timezone.now())
        print("Activation Link Creation Time:", user.activation_link_created_at)
        
        if user.activation_link_created_at and timezone.now() - user.activation_link_created_at > expiration_time:
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

@auth_user_should_not_access
def login_user(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user and not user.is_email_verified:
                messages.error(request, 'Email is not verified, please check your email inbox')
                return render(request, 'registration/login.html', {'form': form}, status=HttpResponseBadRequest.status_code)

            if not user:
                messages.error(request, 'Invalid credentials, try again')
                return render(request, 'registration/login.html', {'form': form}, status=HttpResponseBadRequest.status_code)
            
            login(request, user)
            messages.success(request, f'Welcome {user.username}')
            return redirect(reverse('projects.index'))

    return render(request, 'registration/login.html', {'form': form})

#-----------------------------------------------------------------------------------------

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
        return self.request.user #return the currently logged-in user.

class Edit_Profile(UpdateView):
    model= MyUser
    template_name = 'registration/edit_profile.html'
    form_class = Registeration
    success_url = reverse_lazy("login")
    def get_object(self, queryset=None):
        return self.request.user #return the currently logged-in user.

class Delete_Profile(DeleteView):
    model= MyUser
    template_name = 'registration/delete_profile.html'
    success_url = reverse_lazy("account.create")
    def get_object(self, queryset=None):
        return self.request.user #return the currently logged-in user.    
    