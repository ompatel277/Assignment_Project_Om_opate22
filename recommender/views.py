# recommender/views.py
"""
Views for displaying AI-powered recommendations
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .engine import RecommendationEngine, get_all_recommendations
from .roadmap import RoadmapGenerator, get_roadmap_summary


@login_required
def recommendations_dashboard(request):
    """
    Main recommendations dashboard showing all recommendation types:
    - Career matches
    - Portfolio items
    - Courses
    - Clubs
    """
    profile = request.user.profile

    # Get all recommendations
    all_recs = get_all_recommendations(profile)

    context = {
        'career_recommendations': all_recs['careers'],
        'portfolio_recommendations': all_recs['portfolio_items'],
        'course_recommendations': all_recs['courses'],
        'club_recommendations': all_recs['clubs'],
        'profile': profile,
    }

    return render(request, 'recommender/dashboard.html', context)


@login_required
def career_recommendations_view(request):
    """
    Detailed view of career recommendations with full reasoning.
    """
    profile = request.user.profile
    engine = RecommendationEngine(profile)

    # Get more career recommendations
    career_recs = engine.get_career_recommendations(limit=10)

    context = {
        'recommendations': career_recs,
        'profile': profile,
    }

    return render(request, 'recommender/careers.html', context)


@login_required
def portfolio_recommendations_view(request):
    """
    Detailed view of portfolio item recommendations.
    """
    profile = request.user.profile
    engine = RecommendationEngine(profile)

    portfolio_recs = engine.get_portfolio_recommendations(limit=12)

    context = {
        'recommendations': portfolio_recs,
        'profile': profile,
    }

    return render(request, 'recommender/portfolio.html', context)


# =====================================================
#  ROADMAP VIEWS
# =====================================================

@login_required
def roadmap_view(request):
    """
    Display the complete semester-by-semester roadmap for the user.
    Shows courses, portfolio items, clubs, and milestones for each semester.
    """
    profile = request.user.profile
    generator = RoadmapGenerator(profile)

    # Generate the full roadmap
    roadmap = generator.generate_roadmap()

    # Get summary stats
    summary = generator.generate_summary()

    context = {
        'roadmap': roadmap,
        'summary': summary,
        'profile': profile,
    }

    return render(request, 'recommender/roadmap.html', context)


@login_required
def roadmap_summary_view(request):
    """
    Quick overview of the roadmap with high-level stats.
    Good for dashboard widgets.
    """
    profile = request.user.profile
    summary = get_roadmap_summary(profile)

    context = {
        'summary': summary,
        'profile': profile,
    }

    return render(request, 'recommender/roadmap_summary.html', context)