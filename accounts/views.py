# accounts/views.py
# Updated for A11 Assignment - Data Exports + Reports + Authentication

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
from django.contrib.auth.mixins import LoginRequiredMixin  # NEW FOR A11

from .models import UserProfile, Club, CareerPath, CareerPlan, PlanItem, Course
from .forms import SignupForm, LoginForm, UserProfileForm
from .forms_auth import TrajectSignUpForm  # NEW FOR A11
from colleges.models import College, Major

# NEW IMPORTS for Week 9 (APIs + Charts)
import json
import urllib.request
from io import BytesIO
import matplotlib

matplotlib.use("Agg")  # Use non-GUI backend
import matplotlib.pyplot as plt

# NEW IMPORTS for A11 (CSV/JSON Exports)
import csv
from datetime import datetime


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
            messages.success(request, "Account created successfully!")
            return redirect("accounts:dashboard")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


def public_signup_view(request):
    """
    Assignment 11: Public signup for external users.
    Creates regular non-staff users, logs them in automatically,
    and redirects to onboarding (college selection).
    """
    if request.method == "POST":
        form = TrajectSignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Create associated profile
            UserProfile.objects.create(user=new_user)
            # Auto-login the new user
            login(request, new_user)
            messages.success(
                request,
                f"Welcome to Traject, {new_user.username}! Let's get you set up."
            )
            return redirect("accounts:choose_college")
    else:
        form = TrajectSignUpForm()

    return render(request, "accounts/public_signup.html", {"form": form})


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
#  ENHANCED DASHBOARD VIEW
# =====================================================

@login_required
def dashboard_view(request):
    """
    Enhanced dashboard with AI recommendations and portfolio progress.
    """
    profile = request.user.profile

    # Import here to avoid circular imports
    try:
        from recommender.engine import get_all_recommendations
        from recommender.roadmap import get_roadmap_summary
        recommendations = get_all_recommendations(profile)
        roadmap_summary = get_roadmap_summary(profile)
    except Exception as e:
        # Fallback if recommender fails for any reason
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error generating recommendations: {e}")
        recommendations = {
            'careers': [],
            'portfolio_items': [],
            'courses': [],
            'clubs': []
        }
        roadmap_summary = {}

    # Get portfolio checklist stats
    from accounts.models import UserChecklist
    checklist_items = UserChecklist.objects.filter(user_profile=profile)
    total_checklist = checklist_items.count()
    completed_checklist = checklist_items.filter(status='COMPLETED').count()
    completion_rate = int((completed_checklist / total_checklist * 100)) if total_checklist > 0 else 0

    # Get courses for the user's major
    recommended_courses = []
    if profile.major:
        from accounts.models import Course
        recommended_courses = Course.objects.filter(major=profile.major)[:5]

    # Get clubs for the user's college
    recommended_clubs = []
    if profile.college:
        from accounts.models import Club
        recommended_clubs = Club.objects.filter(college=profile.college)[:5]

    context = {
        'profile': profile,
        'recommendations': recommendations,
        'roadmap_summary': roadmap_summary,
        'recommended_courses': recommended_courses,
        'recommended_clubs': recommended_clubs,
        'checklist_stats': {
            'total': total_checklist,
            'completed': completed_checklist,
            'completion_rate': completion_rate,
        }
    }

    return render(request, 'accounts/dashboard.html', context)


# =====================================================
#  ONBOARDING
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
            messages.success(request, "Profile updated successfully!")
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

    messages.success(request, f"College set to {college.college_name}.")
    return redirect("colleges:detail", pk=college.id)


# =====================================================
#  JSON API ENDPOINTS (Week 9 - Function-Based)
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
        # Skip users without profiles (like superusers)
        if not hasattr(user, 'profile'):
            continue

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
#  JSON API ENDPOINTS (Week 9 - Class-Based)
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
#  CHART GENERATION (Server-Side)
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
#  CHART PAGE VIEWS (Templates that show charts)
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


# =====================================================
#  CSV EXPORT VIEWS (Assignment 11)
# =====================================================

@login_required(login_url='accounts:login')
def export_courses_csv(request):
    """
    Assignment 11: Export all courses to CSV.
    Useful for students planning their course schedules.
    Returns a downloadable CSV file with timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"traject_courses_{timestamp}.csv"

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    # Header row
    writer.writerow(["Subject", "Number", "Title", "Credits", "Major"])

    # Get all courses from colleges.Course
    from colleges.models import Course as CollegeCourse
    courses = (
        CollegeCourse.objects
        .select_related("major")
        .order_by("subject", "number")
    )

    for course in courses:
        writer.writerow([
            course.subject,
            course.number,
            course.title,
            str(course.credits),
            course.major.name if course.major else "N/A"
        ])

    return response


@login_required(login_url='accounts:login')
def export_colleges_csv(request):
    """
    Assignment 11: Export all colleges to CSV.
    Useful for students comparing different schools.
    Includes aggregated major count for each college.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"traject_colleges_{timestamp}.csv"

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    # Header row
    writer.writerow(["Abbreviation", "College Name", "City", "State", "Number of Majors"])

    colleges = (
        College.objects
        .annotate(major_count=Count("majors"))
        .order_by("abbreviation")
    )

    for college in colleges:
        writer.writerow([
            college.abbreviation,
            college.college_name,
            college.city,
            college.state,
            college.major_count
        ])

    return response


# =====================================================
#  JSON EXPORT VIEWS (Assignment 11)
# =====================================================

@login_required(login_url='accounts:login')
def export_courses_json(request):
    """
    Assignment 11: Export all courses to JSON.
    Returns JSON with metadata (timestamp, count).
    """
    from colleges.models import Course as CollegeCourse

    courses = (
        CollegeCourse.objects
        .select_related("major", "major__college")
        .values(
            "subject",
            "number",
            "title",
            "credits",
            "major__name",
            "major__college__abbreviation"
        )
        .order_by("subject", "number")
    )

    data = {
        "generated_at": datetime.now().isoformat(),
        "record_count": courses.count(),
        "courses": list(courses)
    }

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"traject_courses_{timestamp}.json"

    response = JsonResponse(data, json_dumps_params={"indent": 2})
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@login_required(login_url='accounts:login')
def export_colleges_json(request):
    """
    Assignment 11: Export all colleges to JSON.
    Returns JSON with metadata (timestamp, count).
    """
    colleges = (
        College.objects
        .annotate(major_count=Count("majors"))
        .values(
            "abbreviation",
            "college_name",
            "city",
            "state",
            "logo_url",
            "major_count"
        )
        .order_by("abbreviation")
    )

    data = {
        "generated_at": datetime.now().isoformat(),
        "record_count": colleges.count(),
        "colleges": list(colleges)
    }

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"traject_colleges_{timestamp}.json"

    response = JsonResponse(data, json_dumps_params={"indent": 2})
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


# =====================================================
#  REPORTS VIEW (Assignment 11)
# =====================================================

class ReportsView(LoginRequiredMixin, TemplateView):
    """
    Assignment 11: Reports page showing grouped summaries.
    Displays:
    - Courses per Major
    - Students (Users) per College
    - Students per Major
    - Total counts
    """
    template_name = "accounts/reports.html"
    login_url = 'accounts:login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # 1. Courses per Major
        courses_per_major = (
            Major.objects
            .annotate(course_count=Count("courses"))
            .values("name", "college__abbreviation", "course_count")
            .order_by("-course_count")
        )

        # 2. Students (UserProfiles) per College
        students_per_college = (
            College.objects
            .annotate(student_count=Count("students"))
            .values("abbreviation", "college_name", "student_count")
            .order_by("-student_count")
        )

        # 3. Students per Major
        students_per_major = (
            Major.objects
            .annotate(student_count=Count("major_students"))
            .values("name", "college__abbreviation", "student_count")
            .order_by("-student_count")
        )

        # Summary totals
        from colleges.models import Course as CollegeCourse
        ctx["total_courses"] = CollegeCourse.objects.count()
        ctx["total_colleges"] = College.objects.count()
        ctx["total_majors"] = Major.objects.count()
        ctx["total_users"] = UserProfile.objects.count()

        ctx["courses_per_major"] = courses_per_major
        ctx["students_per_college"] = students_per_college
        ctx["students_per_major"] = students_per_major

        return ctx


# =====================================================
#  B10 ASSIGNMENT: DYNAMIC CONTENT TYPE VIEW
# =====================================================

def dynamic_view(request):
    """Dynamic view that returns different content types based on ?q= parameter."""
    query_type = request.GET.get('q', '').lower().strip()

    # TEXT FORMATS
    if query_type == 'html':
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>HTML Mode</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 50px; text-align: center;
        }
        h2 { font-size: 2.5em; }
    </style>
</head>
<body>
    <h2>Hello from HTML mode!</h2>
</body>
</html>"""
        return HttpResponse(html_content, content_type='text/html')

    elif query_type == 'text':
        return HttpResponse("Hello from plain text mode.", content_type='text/plain')

    # APPLICATION FORMATS
    elif query_type == 'json':
        return JsonResponse({"message": "Hello from JSON mode!", "ok": True})

    elif query_type == 'xml':
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>Hello from XML mode!</message>
    <ok>true</ok>
</response>"""
        return HttpResponse(xml_content, content_type='application/xml')

    # IMAGE FORMATS
    elif query_type == 'svg':
        svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200">
    <rect width="400" height="200" fill="#667eea"/>
    <circle cx="200" cy="100" r="50" fill="#ffd700"/>
    <text x="200" y="110" font-size="20" fill="white" text-anchor="middle">Hello from SVG!</text>
</svg>"""
        return HttpResponse(svg_content, content_type='image/svg+xml')

    elif query_type == 'png':
        import base64
        png_data = base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==')
        return HttpResponse(png_data, content_type='image/png')

    # AUDIO FORMATS
    elif query_type == 'mp3':
        return HttpResponse("This is an MP3 audio file placeholder", content_type='audio/mpeg')

    elif query_type == 'wav':
        return HttpResponse("This is a WAV audio file placeholder", content_type='audio/wav')

    # VIDEO FORMATS
    elif query_type == 'mp4':
        return HttpResponse("This is an MP4 video file placeholder", content_type='video/mp4')

    elif query_type == 'webm':
        return HttpResponse("This is a WebM video file placeholder", content_type='video/webm')

    # WEB-SPECIFIC FORMATS
    elif query_type == 'javascript' or query_type == 'js':
        js_content = """// Hello from JavaScript!
console.log('This is JavaScript content');
function greet() { return 'Hello World!'; }"""
        return HttpResponse(js_content, content_type='application/javascript')

    elif query_type == 'rss':
        rss_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>My Feed</title>
        <description>RSS feed example</description>
    </channel>
</rss>"""
        return HttpResponse(rss_content, content_type='application/rss+xml')

    # SPECIAL: Students Dataset
    elif query_type == 'students':
        return JsonResponse({
            "students": [
                {"name": "Alice", "major": "CS", "gpa": 3.85},
                {"name": "Bob", "major": "DS", "gpa": 3.72},
                {"name": "Charlie", "major": "Engineering", "gpa": 3.91}
            ]
        })

    # DEFAULT
    else:
        return HttpResponse("<h1>Add ?q= to the URL</h1><p>Try: ?q=html, ?q=json, ?q=text, ?q=students</p>",
                            content_type='text/html')

# =====================================================
#  CAREER PLANNING VIEWS
# =====================================================

@login_required
def career_plans_list(request):
    """List all career plans for the current user."""
    profile = request.user.profile
    plans = CareerPlan.objects.filter(user_profile=profile)
    
    context = {
        'plans': plans,
        'profile': profile,
    }
    
    return render(request, 'accounts/career_plans/list.html', context)


@login_required
def career_plan_create(request):
    """Create a new career plan."""
    from careers.models import Career
    from accounts.models import CareerPlan

    if request.method == 'POST':
        career_id = request.POST.get('career')
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        is_primary = request.POST.get('is_primary') == 'on'

        # Validation
        if not name:
            messages.error(request, "Please provide a plan name.")
        elif not career_id:
            messages.error(request, "Please select a target career.")
        else:
            try:
                career = Career.objects.get(id=career_id)
                plan = CareerPlan.objects.create(
                    user_profile=request.user.profile,
                    target_career=career,
                    name=name,
                    description=description,
                    is_primary=is_primary
                )

                if is_primary:
                    plan.set_as_primary()

                messages.success(request, f"Career plan '{name}' created successfully!")
                return redirect('accounts:career_plan_detail', plan_id=plan.id)
            except Career.DoesNotExist:
                messages.error(request, "Selected career not found.")
            except Exception as e:
                messages.error(request, f"Error creating plan: {str(e)}")

    # Get top career recommendations for quick selection
    from recommender.engine import RecommendationEngine
    engine = RecommendationEngine(request.user.profile)
    recommended_careers = engine.get_career_recommendations(limit=10)

    # Get all careers
    from careers.models import Career
    all_careers = Career.objects.all().order_by('title')

    context = {
        'recommended_careers': recommended_careers,
        'all_careers': all_careers,
    }

    return render(request, 'accounts/career_plans/create.html', context)


@login_required
def career_plan_detail(request, plan_id):
    """View and manage a specific career plan."""
    from accounts.models import CareerPlan, PlanItem
    from recommender.engine import RecommendationEngine
    
    plan = get_object_or_404(CareerPlan, id=plan_id, user_profile=request.user.profile)
    
    # Get plan items
    plan_items = plan.plan_items.all()

    # Get recommendations for this career
    engine = RecommendationEngine(request.user.profile)
    portfolio_recs = engine.get_portfolio_recommendations(limit=20)
    course_recs = engine.get_course_recommendations(limit=10)

    # Calculate progress and counts
    progress = plan.get_progress_percentage()
    completed_count = plan_items.filter(status='COMPLETED').count()
    in_progress_count = plan_items.filter(status='IN_PROGRESS').count()
    planned_count = plan_items.filter(status='PLANNED').count()

    context = {
        'plan': plan,
        'plan_items': plan_items,
        'portfolio_recs': portfolio_recs,
        'course_recs': course_recs,
        'progress': progress,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'planned_count': planned_count,
    }
    
    return render(request, 'accounts/career_plans/detail.html', context)


@login_required
def career_plan_add_item(request, plan_id):
    """Add an item to a career plan."""
    from accounts.models import CareerPlan, PlanItem, PortfolioItem
    
    plan = get_object_or_404(CareerPlan, id=plan_id, user_profile=request.user.profile)
    
    if request.method == 'POST':
        item_type = request.POST.get('item_type')  # 'portfolio' or 'course' or 'custom'
        priority = int(request.POST.get('priority', 5))
        target_semester = request.POST.get('target_semester', '')
        notes = request.POST.get('notes', '')
        
        plan_item = PlanItem(
            career_plan=plan,
            priority=priority,
            target_semester=target_semester,
            notes=notes
        )
        
        if item_type == 'portfolio':
            portfolio_item_id = request.POST.get('portfolio_item_id')
            portfolio_item = PortfolioItem.objects.get(id=portfolio_item_id)
            plan_item.portfolio_item = portfolio_item
        elif item_type == 'course':
            course_id = request.POST.get('course_id')
            course = Course.objects.get(id=course_id)
            plan_item.course = course
        elif item_type == 'custom':
            plan_item.custom_title = request.POST.get('custom_title')
            plan_item.custom_description = request.POST.get('custom_description', '')
        
        plan_item.save()
        messages.success(request, "Item added to your career plan!")
        return redirect('accounts:career_plan_detail', plan_id=plan.id)
    
    return redirect('accounts:career_plan_detail', plan_id=plan.id)


@login_required
def career_plan_delete(request, plan_id):
    """Delete a career plan."""
    from accounts.models import CareerPlan
    
    plan = get_object_or_404(CareerPlan, id=plan_id, user_profile=request.user.profile)
    
    if request.method == 'POST':
        plan_name = plan.name
        plan.delete()
        messages.success(request, f"Career plan '{plan_name}' deleted successfully.")
        return redirect('accounts:career_plans_list')
    
    return redirect('accounts:career_plan_detail', plan_id=plan.id)


@login_required
def career_plan_edit(request, plan_id):
    """Edit a career plan."""
    from accounts.models import CareerPlan
    from careers.models import Career

    plan = get_object_or_404(CareerPlan, id=plan_id, user_profile=request.user.profile)

    if request.method == 'POST':
        plan.name = request.POST.get('name')
        plan.description = request.POST.get('description', '')
        plan.is_active = request.POST.get('is_active') == 'on'
        plan.save()

        messages.success(request, f"Career plan '{plan.name}' updated successfully!")
        return redirect('accounts:career_plan_detail', plan_id=plan.id)

    context = {
        'plan': plan,
    }

    return render(request, 'accounts/career_plans/edit.html', context)


@login_required
def career_plan_set_primary(request, plan_id):
    """Set a career plan as the primary plan."""
    from accounts.models import CareerPlan

    plan = get_object_or_404(CareerPlan, id=plan_id, user_profile=request.user.profile)

    if request.method == 'POST':
        # Unset all other primary plans
        CareerPlan.objects.filter(user_profile=request.user.profile).update(is_primary=False)

        # Set this plan as primary
        plan.is_primary = True
        plan.save()

        messages.success(request, f"'{plan.name}' is now your primary career plan!")

    return redirect('accounts:career_plan_detail', plan_id=plan.id)


@login_required
def plan_item_update_status(request, item_id):
    """Update the status of a plan item."""
    from accounts.models import PlanItem

    item = get_object_or_404(PlanItem, id=item_id, career_plan__user_profile=request.user.profile)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(PlanItem.STATUS_CHOICES):
            item.status = new_status
            if new_status == 'COMPLETED':
                item.mark_completed()
            else:
                item.save()
            messages.success(request, f"Status updated to {item.get_status_display()}")

    return redirect('accounts:career_plan_detail', plan_id=item.career_plan.id)
