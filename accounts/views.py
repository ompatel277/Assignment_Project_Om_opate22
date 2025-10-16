# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.db.models import Q
from django.template import loader

from .models import UserProfile
from .forms import SignupForm, LoginForm, UserProfileForm
from colleges.models import College, Major, Course


# =====================================================
#  AUTHENTICATION VIEWS
# =====================================================

def signup_view(request):
    """Handle user signup and automatic login."""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "🎉 Account created successfully!")
            return redirect("accounts:dashboard")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    """Handle user login."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("accounts:dashboard")
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """Logout and redirect to login page."""
    logout(request)
    messages.info(request, "You’ve been logged out.")
    return redirect("accounts:login")


# =====================================================
#  DASHBOARD VIEW
# =====================================================

@login_required
def dashboard_view(request):
    """
    Display the user's dashboard with personalized recommendations.
    """
    profile = request.user.profile

    # --- Recommended Courses (based on user's major) ---
    recommended_courses = []
    if profile.major:
        recommended_courses = (
            Course.objects.filter(major=profile.major)
            .order_by("subject", "number")[:8]
        )

    # --- Placeholder lists (to be expanded later) ---
    recommended_clubs = []
    recommended_careers = []

    return render(
        request,
        "accounts/dashboard.html",
        {
            "user": request.user,
            "profile": profile,
            "recommended_courses": recommended_courses,
            "recommended_clubs": recommended_clubs,
            "recommended_careers": recommended_careers,
        },
    )


# =====================================================
#  ONBOARDING (CHOOSE COLLEGE)
# =====================================================

@login_required
def choose_college_view(request):
    """
    Let the user pick their college and major during onboarding.
    """
    profile = request.user.profile
    colleges = College.objects.all().order_by("abbreviation")

    # If user already chose a college, skip onboarding
    if profile.college:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        college_id = request.POST.get("college")
        major_id = request.POST.get("major")

        if not college_id:
            messages.error(request, "Please select a college to continue.")
            return redirect("accounts:choose_college")

        college = get_object_or_404(College, id=college_id)
        profile.college = college

        if major_id:
            major = Major.objects.filter(id=major_id, college=college).first()
            if major:
                profile.major = major

        profile.save()
        messages.success(request, f"Welcome to {college.college_name}!")
        return redirect("accounts:dashboard")

    return render(request, "accounts/choose_college.html", {"colleges": colleges})


# =====================================================
#  PROFILE VIEWS
# =====================================================

@login_required
def profile_view(request, username=None):
    """
    Display either the current user's profile or another user's profile.
    """
    user_obj = get_object_or_404(User, username=username) if username else request.user
    return render(request, "accounts/profile.html", {"user": user_obj})


@login_required
def edit_profile_view(request):
    """
    Allow the user to update their academic and personal profile details.
    """
    profile = request.user.profile

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect("accounts:profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {"form": form})


# =====================================================
#  USER LIST & COLLEGE SHORTCUT
# =====================================================

@login_required
def user_list_http(request):
    """Render a basic list of all users (for debugging/demo)."""
    users = User.objects.all().select_related("profile")
    template = loader.get_template("accounts/user_list.html")
    return HttpResponse(template.render({"users": users}, request))


@login_required
def set_college(request, college_id):
    """
    Allow a logged-in user to set their college directly from a college page.
    """
    college = get_object_or_404(College, id=college_id)
    profile = request.user.profile
    profile.college = college
    profile.save()

    messages.success(request, f"🎓 College set to {college.college_name}.")
    return redirect("colleges:detail", pk=college.id)
