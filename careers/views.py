# careers/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Career

# ============================
# 1️⃣  Career List View
# ============================
@login_required
def career_list_view(request):
    """
    Displays all available careers.
    Future enhancement: filter based on user's profile skills or interests.
    """
    careers = Career.objects.all().order_by("title")
    return render(request, "careers/career_list.html", {"careers": careers})


# ============================
# 2️⃣  Career Detail View
# ============================
@login_required
def career_detail_view(request, pk):
    """
    Displays details for a single career.
    """
    career = get_object_or_404(Career, pk=pk)
    return render(request, "careers/career_detail.html", {"career": career})


# ============================
# 3️⃣  (Optional) Recommended Careers
# ============================
@login_required
def recommended_careers_view(request):
    """
    Filters careers that align with user's profile skills or interests.
    """
    user_profile = getattr(request.user, "profile", None)
    recommended = Career.objects.none()

    if user_profile and (user_profile.skills or user_profile.personal_interests):
        keywords = set(user_profile.skills or []) | set(user_profile.personal_interests or [])
        recommended = Career.objects.filter(
            description__icontains=list(keywords)[0]
        )[:10] if keywords else Career.objects.none()

    return render(request, "careers/recommended_careers.html", {"recommended": recommended})
