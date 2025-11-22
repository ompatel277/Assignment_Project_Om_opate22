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
    Detailed view of portfolio item recommendations with filtering.
    """
    profile = request.user.profile
    engine = RecommendationEngine(profile)

    # Get all portfolio recommendations
    portfolio_recs = engine.get_portfolio_recommendations(limit=50)

    # Filter by category if specified
    category = request.GET.get('category', 'all')
    if category and category != 'all':
        portfolio_recs = [rec for rec in portfolio_recs if rec['item'].item_type == category]

    context = {
        'recommendations': portfolio_recs,
        'profile': profile,
        'selected_category': category,
    }

    return render(request, 'recommender/portfolio.html', context)


# =====================================================
#  ROADMAP VIEWS
# =====================================================

@login_required
def roadmap_view(request):
    """
    Display roadmaps based on user's career plans.
    Allows selecting specific plan or comparing multiple plans.
    """
    from accounts.models import CareerPlan

    profile = request.user.profile

    # Get all user's career plans
    career_plans = CareerPlan.objects.filter(user_profile=profile)

    # Get selected plan (or primary plan by default)
    selected_plan_id = request.GET.get('plan')
    compare_mode = request.GET.get('compare') == 'true'

    if compare_mode and career_plans.count() > 0:
        # Compare mode: show multiple roadmaps
        roadmaps_data = []
        for plan in career_plans:
            generator = RoadmapGenerator(profile)
            roadmaps_data.append({
                'plan': plan,
                'roadmap': generator.generate_roadmap(),
                'summary': generator.generate_summary()
            })

        context = {
            'compare_mode': True,
            'roadmaps_data': roadmaps_data,
            'career_plans': career_plans,
            'profile': profile,
        }
    else:
        # Single plan mode
        selected_plan = None

        if selected_plan_id:
            selected_plan = career_plans.filter(id=selected_plan_id).first()
        else:
            # Default to primary plan or first plan
            selected_plan = career_plans.filter(is_primary=True).first() or career_plans.first()

        generator = RoadmapGenerator(profile)
        roadmap = generator.generate_roadmap()
        summary = generator.generate_summary()

        context = {
            'compare_mode': False,
            'roadmap': roadmap,
            'summary': summary,
            'profile': profile,
            'career_plans': career_plans,
            'selected_plan': selected_plan,
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