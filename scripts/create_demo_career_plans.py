#!/usr/bin/env python
"""
Create demo career plans for demo users
"""
import os
import sys
import django

# Setup Django
sys.path.append('/home/user/Assignment_Project_Om_opate22')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Assignment_Project_Om_opate22.Settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import CareerPlan, PlanItem, Course, PortfolioItem
from careers.models import Career

print("=" * 70)
print("CREATING DEMO CAREER PLANS")
print("=" * 70)

# Get demo users
demo_users = ['demo_student', 'alice_chen', 'bob_smith', 'charlie_davis', 'emma_wilson']

for username in demo_users:
    try:
        user = User.objects.get(username=username)
        profile = user.profile

        print(f"\nCreating career plans for {username}...")

        # Get some careers for this user
        from recommender.engine import RecommendationEngine
        engine = RecommendationEngine(profile)
        career_recs = engine.get_career_recommendations(limit=5)

        if career_recs:
            # Create 2-3 career plans per user
            num_plans = min(3, len(career_recs))

            for i in range(num_plans):
                rec = career_recs[i]
                career = rec['career']

                # Create plan
                plan_name = f"Plan {chr(65+i)}: {career.title}"

                plan, created = CareerPlan.objects.get_or_create(
                    user_profile=profile,
                    target_career=career,
                    defaults={
                        'name': plan_name,
                        'description': f"Career path targeting {career.title} role",
                        'is_primary': (i == 0),  # First plan is primary
                        'is_active': True
                    }
                )

                if created:
                    print(f"  ✓ Created: {plan_name}")

                    # Add some plan items
                    # Add courses if available
                    courses = Course.objects.filter(major=profile.major)[:3]
                    for course in courses:
                        PlanItem.objects.create(
                            career_plan=plan,
                            course=course,
                            status='PLANNED',
                            priority=5,
                            target_semester='Fall 2024'
                        )

                    # Add portfolio items
                    portfolio_items = PortfolioItem.objects.all()[:2]
                    for item in portfolio_items:
                        PlanItem.objects.create(
                            career_plan=plan,
                            portfolio_item=item,
                            status='PLANNED',
                            priority=7
                        )

                    # Add custom milestones
                    PlanItem.objects.create(
                        career_plan=plan,
                        custom_title=f"Complete {career.title} interview prep",
                        custom_description="Practice coding problems and system design",
                        status='PLANNED',
                        priority=8
                    )

                    print(f"    Added {plan.plan_items.count()} items to plan")
                else:
                    print(f"  - Plan already exists: {plan_name}")
        else:
            print(f"  ⚠ No career recommendations for {username}")

    except User.DoesNotExist:
        print(f"  ✗ User {username} not found")
    except Exception as e:
        print(f"  ✗ Error for {username}: {e}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

total_plans = CareerPlan.objects.count()
total_items = PlanItem.objects.count()

print(f"Total career plans: {total_plans}")
print(f"Total plan items: {total_items}")

print("\n✅ Demo career plans created!")
