# accounts/portfolio_views.py
"""
Views for Portfolio Checklist Management
Allows users to view, add, and track their portfolio items
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q

from .models import PortfolioItem, UserChecklist


# =====================================================
#  PORTFOLIO CHECKLIST VIEW
# =====================================================

@login_required
def portfolio_checklist_view(request):
    """
    Display user's portfolio checklist with all their tracked items.
    Shows items grouped by status.
    """
    profile = request.user.profile

    # Get all checklist items for this user
    checklist_items = UserChecklist.objects.filter(
        user_profile=profile
    ).select_related('portfolio_item').order_by('-priority', '-added_at')

    # Group by status for better UI
    planned = checklist_items.filter(status='PLANNED')
    in_progress = checklist_items.filter(status='IN_PROGRESS')
    completed = checklist_items.filter(status='COMPLETED')

    # Calculate statistics
    total_items = checklist_items.count()
    completed_count = completed.count()
    completion_rate = int((completed_count / total_items * 100)) if total_items > 0 else 0

    # Get suggested items (not yet added to checklist)
    suggested_items = PortfolioItem.objects.exclude(
        user_checklists__user_profile=profile
    ).order_by('difficulty_level', 'title')[:6]

    context = {
        'planned': planned,
        'in_progress': in_progress,
        'completed': completed,
        'total_items': total_items,
        'completed_count': completed_count,
        'completion_rate': completion_rate,
        'suggested_items': suggested_items,
    }

    return render(request, 'accounts/portfolio_checklist.html', context)


# =====================================================
#  ADD PORTFOLIO ITEM TO CHECKLIST
# =====================================================

@login_required
def add_to_checklist(request, item_id):
    """
    Add a portfolio item to user's checklist.
    """
    profile = request.user.profile
    portfolio_item = get_object_or_404(PortfolioItem, id=item_id)

    # Check if already in checklist
    if UserChecklist.objects.filter(user_profile=profile, portfolio_item=portfolio_item).exists():
        messages.warning(request, f"{portfolio_item.title} is already in your checklist.")
        return redirect('accounts:portfolio_checklist')

    # Create checklist item
    UserChecklist.objects.create(
        user_profile=profile,
        portfolio_item=portfolio_item,
        status='PLANNED',
        priority='MEDIUM'
    )

    messages.success(request, f"✅ Added {portfolio_item.title} to your checklist!")
    return redirect('accounts:portfolio_checklist')


# =====================================================
#  UPDATE CHECKLIST ITEM STATUS
# =====================================================

@login_required
def update_checklist_status(request, checklist_id):
    """
    Update the status of a checklist item.
    Supports: PLANNED → IN_PROGRESS → COMPLETED
    """
    checklist_item = get_object_or_404(
        UserChecklist,
        id=checklist_id,
        user_profile=request.user.profile
    )

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in ['PLANNED', 'IN_PROGRESS', 'COMPLETED', 'ABANDONED']:
            checklist_item.status = new_status

            # Update timestamps
            if new_status == 'IN_PROGRESS' and not checklist_item.started_at:
                checklist_item.started_at = timezone.now()
            elif new_status == 'COMPLETED':
                checklist_item.completed_at = timezone.now()
                checklist_item.progress_percentage = 100

            checklist_item.save()

            messages.success(request, f"Updated {checklist_item.portfolio_item.title} status!")
        else:
            messages.error(request, "Invalid status.")

    return redirect('accounts:portfolio_checklist')


# =====================================================
#  UPDATE PROGRESS PERCENTAGE (AJAX)
# =====================================================

@login_required
def update_progress(request, checklist_id):
    """
    AJAX endpoint to update progress percentage.
    Returns JSON response.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

    checklist_item = get_object_or_404(
        UserChecklist,
        id=checklist_id,
        user_profile=request.user.profile
    )

    try:
        progress = int(request.POST.get('progress', 0))

        # Validate range
        if not 0 <= progress <= 100:
            return JsonResponse({'success': False, 'error': 'Progress must be 0-100'})

        checklist_item.progress_percentage = progress

        # Auto-update status based on progress
        if progress == 0:
            checklist_item.status = 'PLANNED'
        elif progress == 100:
            checklist_item.status = 'COMPLETED'
            if not checklist_item.completed_at:
                checklist_item.completed_at = timezone.now()
        else:
            checklist_item.status = 'IN_PROGRESS'
            if not checklist_item.started_at:
                checklist_item.started_at = timezone.now()

        checklist_item.save()

        return JsonResponse({
            'success': True,
            'progress': progress,
            'status': checklist_item.get_status_display()
        })

    except ValueError:
        return JsonResponse({'success': False, 'error': 'Invalid progress value'})


# =====================================================
#  UPDATE PRIORITY (AJAX)
# =====================================================

@login_required
def update_priority(request, checklist_id):
    """
    AJAX endpoint to update item priority.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

    checklist_item = get_object_or_404(
        UserChecklist,
        id=checklist_id,
        user_profile=request.user.profile
    )

    priority = request.POST.get('priority')

    if priority in ['LOW', 'MEDIUM', 'HIGH']:
        checklist_item.priority = priority
        checklist_item.save()

        return JsonResponse({
            'success': True,
            'priority': priority,
            'priority_display': checklist_item.get_priority_display()
        })

    return JsonResponse({'success': False, 'error': 'Invalid priority'})


# =====================================================
#  REMOVE FROM CHECKLIST
# =====================================================

@login_required
def remove_from_checklist(request, checklist_id):
    """
    Remove an item from the user's checklist.
    """
    checklist_item = get_object_or_404(
        UserChecklist,
        id=checklist_id,
        user_profile=request.user.profile
    )

    item_title = checklist_item.portfolio_item.title
    checklist_item.delete()

    messages.success(request, f"Removed {item_title} from your checklist.")
    return redirect('accounts:portfolio_checklist')


# =====================================================
#  BROWSE ALL PORTFOLIO ITEMS
# =====================================================

@login_required
def browse_portfolio_items(request):
    """
    Browse all available portfolio items with filtering.
    """
    profile = request.user.profile

    # Get all items
    items = PortfolioItem.objects.all()

    # Apply filters
    item_type = request.GET.get('type')
    difficulty = request.GET.get('difficulty')

    if item_type:
        items = items.filter(item_type=item_type)
    if difficulty:
        items = items.filter(difficulty_level=difficulty)

    # Get items already in user's checklist
    user_checklist_ids = UserChecklist.objects.filter(
        user_profile=profile
    ).values_list('portfolio_item_id', flat=True)

    # Annotate items with "in_checklist" flag
    items_with_status = []
    for item in items.order_by('difficulty_level', 'title'):
        items_with_status.append({
            'item': item,
            'in_checklist': item.id in user_checklist_ids
        })

    context = {
        'items': items_with_status,
        'item_types': PortfolioItem.ITEM_TYPES,
        'selected_type': item_type,
        'selected_difficulty': difficulty,
    }

    return render(request, 'accounts/browse_portfolio.html', context)


# =====================================================
#  PORTFOLIO ITEM DETAIL
# =====================================================

@login_required
def portfolio_item_detail(request, item_id):
    """
    Show detailed information about a portfolio item.
    """
    item = get_object_or_404(PortfolioItem, id=item_id)
    profile = request.user.profile

    # Check if user has this in their checklist
    user_checklist_item = UserChecklist.objects.filter(
        user_profile=profile,
        portfolio_item=item
    ).first()

    # Get related careers
    related_careers = item.related_careers.all()

    context = {
        'item': item,
        'user_checklist_item': user_checklist_item,
        'related_careers': related_careers,
        'skills_list': item.get_skills_list(),
    }

    return render(request, 'accounts/portfolio_item_detail.html', context)