# accounts/views.py
# Updated for A9 Assignment - JSON APIs + Chart Integration

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count
from django.template import loader
from django.views import View
from django.views.generic import TemplateView

from .models import UserProfile, Club, CareerPath
from .forms import SignupForm, LoginForm, UserProfileForm
from colleges.models import College, Major, Course

# NEW IMPORTS for Week 9 (APIs + Charts)
import json
import urllib.request
from io import BytesIO
import matplotlib

matplotlib.use("Agg")  # Use non-GUI backend
import matplotlib.pyplot as plt


# =====================================================
#  AUTHENTICATION VIEWS (Existing - No Changes)
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
    messages.info(request, "You've been logged out.")
    return redirect("accounts:login")


# =====================================================
#  DASHBOARD VIEW (Existing - No Changes)
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
#  ONBOARDING (Existing - No Changes)
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
#  PROFILE VIEWS (Existing - No Changes)
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
#  USER LIST & COLLEGE SHORTCUT (Existing - No Changes)
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


# =====================================================
#  NEW: JSON API ENDPOINTS (Week 9 - Function-Based)
# =====================================================

def api_ping_httpresponse(request):
    """
    Demonstration: HttpResponse with manual JSON serialization.
    Shows the difference between HttpResponse and JsonResponse.
    """
    payload = json.dumps({"ok": True, "message": "Ping successful using HttpResponse"})
    return HttpResponse(payload, content_type="application/json")


def api_ping_jsonresponse(request):
    """
    Demonstration: JsonResponse with automatic JSON serialization.
    Django automatically sets content_type="application/json".
    """
    return JsonResponse({"ok": True, "message": "Ping successful using JsonResponse"})


def api_users(request):
    """
    GET /api/users/
    Returns a list of all users with their profile information.
    Optional query parameter: ?q=<search_term>
    """
    q = (request.GET.get("q") or "").strip()

    users = User.objects.select_related("profile__college", "profile__major")

    if q:
        users = users.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )

    data = []
    for user in users.order_by("username"):
        profile = user.profile
        data.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "college": profile.college.abbreviation if profile.college else None,
            "major": profile.major.name if profile.major else None,
            "academic_year": profile.get_academic_year_display(),
            "gpa": float(profile.gpa) if profile.gpa else None,
        })

    return JsonResponse({"count": len(data), "results": data})


def api_users_per_college(request):
    """
    GET /api/colleges/users/
    Returns the count of users per college (aggregated data).
    Perfect for creating bar charts!
    """
    rows = (
        College.objects
        .annotate(user_count=Count("students"))
        .values("abbreviation", "college_name", "user_count")
        .order_by("abbreviation")
    )

    # Format for easy charting
    labels = [r["abbreviation"] for r in rows]
    counts = [r["user_count"] for r in rows]

    return JsonResponse({
        "labels": labels,
        "counts": counts,
        "details": list(rows)
    })


def api_users_per_academic_year(request):
    """
    GET /api/users/academic-year/
    Returns count of users per academic year (Freshman, Sophomore, etc.)
    """
    rows = (
        UserProfile.objects
        .values("academic_year")
        .annotate(count=Count("id"))
        .order_by("academic_year")
    )

    # Create readable labels
    year_labels = dict(UserProfile.ACADEMIC_YEARS)
    results = []
    for r in rows:
        results.append({
            "academic_year_code": r["academic_year"],
            "academic_year_name": year_labels.get(r["academic_year"], r["academic_year"]),
            "count": r["count"]
        })

    return JsonResponse({"results": results})


def api_courses_per_major(request):
    """
    GET /api/courses/per-major/
    Returns the count of courses available per major.
    """
    rows = (
        Major.objects
        .annotate(course_count=Count("courses"))
        .values("name", "code", "course_count")
        .order_by("name")
    )

    return JsonResponse({"results": list(rows)})


def api_clubs_per_college(request):
    """
    GET /api/clubs/per-college/
    Returns the count of clubs per college.
    """
    rows = (
        College.objects
        .annotate(club_count=Count("clubs"))
        .values("abbreviation", "college_name", "club_count")
        .order_by("abbreviation")
    )

    return JsonResponse({"results": list(rows)})


# =====================================================
#  NEW: JSON API ENDPOINTS (Week 9 - Class-Based)
# =====================================================

class UsersAPI(View):
    """
    Class-based view for the Users API.
    GET /api/class-users/?q=<search_term>
    Demonstrates class-based API implementation.
    """

    def get(self, request):
        q = (request.GET.get("q") or "").strip()

        users = User.objects.select_related("profile__college", "profile__major")

        if q:
            users = users.filter(
                Q(username__icontains=q) |
                Q(email__icontains=q)
            )

        data = []
        for user in users.order_by("username"):
            profile = user.profile
            data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "college": profile.college.abbreviation if profile.college else None,
                "major": profile.major.name if profile.major else None,
                "gpa": float(profile.gpa) if profile.gpa else None,
            })

        return JsonResponse({"count": len(data), "results": data})


# =====================================================
#  NEW: CHART GENERATION (Server-Side)
# =====================================================

def users_per_college_chart_png(request):
    """
    Generates a PNG bar chart showing users per college.
    This view:
    1. Fetches data from our own JSON API
    2. Uses matplotlib to create a chart
    3. Returns the chart as a PNG image (HttpResponse)
    """
    # Build the full URL to our API endpoint
    api_url = request.build_absolute_uri('/accounts/api/colleges/users/')
    # Fetch data from our API
    with urllib.request.urlopen(api_url) as response:
        data = json.load(response)

    labels = data["labels"]
    counts = data["counts"]

    # Create the chart
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

    # Bar chart with traject colors
    bars = ax.bar(labels, counts, color="#FF6B35", edgecolor="#1A1A2E", linewidth=1.5)

    # Styling
    ax.set_title("Students per College", fontsize=16, fontweight="bold", color="#1A1A2E")
    ax.set_xlabel("College", fontsize=12, color="#1A1A2E")
    ax.set_ylabel("Number of Students", fontsize=12, color="#1A1A2E")
    ax.tick_params(axis="x", rotation=45, labelsize=10)
    ax.tick_params(axis="y", labelsize=10)

    # Add count labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10)

    # Grid for readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    fig.tight_layout()

    # Save to BytesIO buffer
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)

    return HttpResponse(buf.getvalue(), content_type="image/png")


def users_per_year_chart_png(request):
    """
    Generates a PNG pie chart showing distribution of students by academic year.
    """
    api_url = request.build_absolute_uri('/accounts/api/users/academic-year/')
    with urllib.request.urlopen(api_url) as response:
        data = json.load(response)

    results = data["results"]

    if not results:
        # Return a blank chart if no data
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=16)
        ax.axis('off')
    else:
        labels = [r["academic_year_name"] for r in results]
        sizes = [r["count"] for r in results]

        fig, ax = plt.subplots(figsize=(10, 7), dpi=100)

        colors = ['#FF6B35', '#F7931E', '#FDC830', '#37B5A6', '#4ECDC4']
        explode = [0.05] * len(labels)  # Slightly separate all slices

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            colors=colors,
            explode=explode,
            startangle=90,
            textprops={'fontsize': 11}
        )

        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title("Student Distribution by Academic Year",
                     fontsize=16, fontweight="bold", pad=20)

    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)

    return HttpResponse(buf.getvalue(), content_type="image/png")


# =====================================================
#  NEW: CHART PAGE VIEWS (Templates that show charts)
# =====================================================

class UsersChartPage(TemplateView):
    """
    Displays the users per college chart in a template.
    """
    template_name = "accounts/users_chart.html"


class AcademicYearChartPage(TemplateView):
    """
    Displays the academic year distribution chart in a template.
    """
    template_name = "accounts/academic_year_chart.html"