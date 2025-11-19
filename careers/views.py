# careers/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Career

# ============================
# Career List View
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
# Career Detail View
# ============================
@login_required
def career_detail_view(request, pk):
    """
    Displays details for a single career.
    """
    career = get_object_or_404(Career, pk=pk)
    return render(request, "careers/career_detail.html", {"career": career})


# ============================
# Recommended Careers (Optional)
# ============================
@login_required
def recommended_careers_view(request):
    """
    Filters careers that align with user's profile skills or interests.
    """
    user_profile = getattr(request.user, "profile", None)
    recommended = Career.objects.none()

    if user_profile:
        # Use the model's helper methods to get lists of skills and interests
        skills_list = user_profile.get_skills_list()
        interests_list = user_profile.get_interests_list()
        keywords = set(skills_list) | set(interests_list)

        if keywords:
            # Filter careers that match any of the keywords
            from django.db.models import Q
            query = Q()
            for keyword in keywords:
                query |= Q(description__icontains=keyword) | Q(title__icontains=keyword)
            recommended = Career.objects.filter(query).distinct()[:10]

    return render(request, "careers/recommended_careers.html", {"recommended": recommended})
