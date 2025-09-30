from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import User, UserProfile
from .forms import SignupForm, LoginForm  # make sure class name matches your forms.py
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout


# Signup
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],  # ✅ corrected
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password1'],  # ✅ corrected
            )
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created.')
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {'form': form})  # ✅ always return


# Login
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome Back, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid Credentials')
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {'form': form})  # ✅ always return


# Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('login')  # ✅ lowercase fixed


# Dashboard
@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")  # ✅ fixed typo


# List users with HttpResponse
def user_list_http(request):
    users = User.objects.all()
    template = loader.get_template('accounts/user_list.html')
    context = {"users": users}
    return HttpResponse(template.render(context, request))


# List users with render shortcut
def user_list_render(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})
