from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import uuid
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .auth import admin_only
from django.core.mail import send_mail
from django.conf import settings
from .helpers import *
# Create your views here.


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def user_register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).first():
            messages.add_message(request, messages.ERROR,
                                 'username alredy exists')
            return redirect('/register')

        if User.objects.filter(email=email).first():
            messages.add_message(request, messages.ERROR,
                                 'email alredy exists')
            return redirect('/register')

        user_obj = User.objects.create(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()

        auth_token = str(uuid.uuid4())

        profile_obj = Profile.objects.create(
            user=user_obj, auth_token=auth_token)
        profile_obj.save()

        email_verification(email, auth_token)
        return redirect('/token')

    return render(request, 'accounts/register.html')


def user_login(request):
    # if request.method == 'POST':
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         user = authenticate(
    #             request, username=data['username'], password=data['password'])
    #         if user is not None:
    #             login(request, user)
    #             return redirect('/dashboard')
    #         else:
    #             messages.add_message(
    #                 request, messages.ERROR, 'please provide correct credentials')
    #             return render(request, 'accounts/login.html', {'form': form})

    # context = {
    #     'form': LoginForm
    # }
    # return render(request, 'accounts/login.html', context)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.error(request, 'User not found')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        if user_obj.is_superuser:
            login(request, authenticate(
                request, username=username, password=password))
            return redirect('/admin/dashboard')

        if not profile_obj.is_verify:
            messages.error(request, 'Your email not verified')
            return redirect('/login')

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'email and passord mismatch')
            return redirect('/login')

        if user is not None:
            login(request, user)
            return redirect('/')

        login(request, user)
        return redirect('/')

    return render(request, 'accounts/login.html')


def success_request(request):
    return render(request, 'accounts/success.html')


def token_send(request):
    return render(request, 'accounts/token_send.html')

# *****************account verification******************


def verify(request, auth_token):

    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verify:
            messages.success(request, 'Account already Verified')
            return redirect('/login')
        profile_obj.is_verify = True
        profile_obj.save()
        messages.success(request, 'your account has been verified')
        return redirect('/login')
    else:
        return redirect('/error')


def error_page(request):
    return render(request, 'accounts/error.html')


def email_verification(email, token):
    subject = 'Your account needs to be verified'
    message = f'link to verify http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

# *******************forget password********************


def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not User.objects.filter(email=email).first():
            messages.error(request, 'User not found')
            return redirect('/forgetpassword')

        user_obj = User.objects.get(email=email)
        token = str(uuid.uuid4())
        profile_obj = Profile.objects.get(user=user_obj)
        profile_obj.forget_pass_token = token
        profile_obj.save()

        send_forget_password_mail(email, token)
        messages.success(request, 'Verification code sent. Check your mail')
        return redirect('/forgetpassword')

    return render(request, 'accounts/forgetpassword.html')


# *****************change password****************


def change_password(request, token):

    profile_obj = Profile.objects.filter(forget_pass_token=token).first()
    context = {
        'user_id': profile_obj.user.id
    }
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user_id = request.POST.get('user_id')

        if user_id is None:
            messages.error(request, 'User not found')
            return redirect(f'/changepassword/{token}')

        if new_password != confirm_password:
            messages.error(request, 'Password did not match')
            return redirect(f'/changepassword/{token}')

        user_obj = User.objects.get(id=user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        return redirect('/login')

    return render(request, 'accounts/changepassword.html', context)


def user_logout(request):
    logout(request)
    return redirect('/login')


# @ login_required
# @ admin_only
# def dashboard(request):
#     return render(request, 'accounts/dashboard.html')
