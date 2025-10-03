from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .models import UserProfile
from .forms import SignupForm, LoginForm, UserProfileForm


# --- Signup ---
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created.')
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {'form': form})


# --- Login ---
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {'form': form})


# --- Logout ---
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


# --- Dashboard ---
@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")


# --- Profile (self + others) ---
@login_required
def profile_view(request, username=None):
    if username:
        user_obj = get_object_or_404(User, username=username)
    else:
        user_obj = request.user

    return render(request, "accounts/profile.html", {'user': user_obj})


# --- Edit Profile ---
@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {"form": form})


# --- User List ---
@login_required
def user_list_http(request):
    """HttpResponse version: manually load template and return"""
    users = User.objects.all()
    template = loader.get_template("accounts/user_list.html")
    context = {"users": users}
    return HttpResponse(template.render(context, request))