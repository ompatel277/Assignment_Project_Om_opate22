#!/usr/bin/env python3
"""Add portfolio checklist items to demo users with realistic progress."""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
sys.path.insert(0, '/home/user/Assignment_Project_Om_opate22')
os.environ.setdefault('DJANGO_SECRET_KEY', 'demo-key-for-testing')
os.environ.setdefault('DJANGO_DEBUG', 'True')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Assignment_Project_Om_opate22.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile, PortfolioItem, UserChecklist

def add_portfolio_to_users():
    """Add realistic portfolio items to each demo user."""
    print("Adding portfolio checklist items to demo users...")

    # Alice Chen - CS Senior (Advanced projects, completed internships)
    alice = User.objects.filter(username='alice_chen').first()
    if alice and hasattr(alice, 'profile'):
        print("  Adding items for alice_chen...")
        items_alice = [
            {'item': 'Machine Learning Internship at Google', 'status': 'COMPLETED', 'notes': 'Completed Summer 2024. Worked on recommendation systems.'},
            {'item': 'Open Source Contribution to React', 'status': 'COMPLETED', 'notes': 'Merged 3 PRs with performance improvements'},
            {'item': 'Research Publication in AI Conference', 'status': 'IN_PROGRESS', 'notes': 'Paper under review for NeurIPS 2025'},
            {'item': 'LeetCode - 300+ Problems Solved', 'status': 'COMPLETED', 'notes': '350+ problems solved across all difficulty levels'},
            {'item': 'AWS Certified Solutions Architect', 'status': 'PLANNED', 'notes': 'Planning to get certified before graduation'},
        ]

        for item_data in items_alice:
            item = PortfolioItem.objects.filter(title__icontains=item_data['item']).first()
            if item:
                UserChecklist.objects.get_or_create(
                    user_profile=alice.profile,
                    portfolio_item=item,
                    defaults={
                        'status': item_data['status'],
                        'notes': item_data['notes']
                    }
                )

    # Bob Martinez - EE Junior (Hardware projects)
    bob = User.objects.filter(username='bob_martinez').first()
    if bob and hasattr(bob, 'profile'):
        print("  Adding items for bob_martinez...")
        items_bob = [
            {'item': 'Software Engineering Internship at FAANG', 'status': 'COMPLETED', 'notes': 'Hardware Engineering Intern at Tesla, Summer 2024'},
            {'item': 'Hackathon Winner', 'status': 'COMPLETED', 'notes': 'Won 2nd place at Stanford Hardware Hackathon'},
            {'item': 'Technical Blog', 'status': 'IN_PROGRESS', 'notes': 'Writing about embedded systems and IoT. 500+ readers.'},
            {'item': 'System Design Course', 'status': 'PLANNED', 'notes': 'Need to learn system design for interviews'},
        ]

        for item_data in items_bob:
            item = PortfolioItem.objects.filter(title__icontains=item_data['item']).first()
            if item:
                UserChecklist.objects.get_or_create(
                    user_profile=bob.profile,
                    portfolio_item=item,
                    defaults={
                        'status': item_data['status'],
                        'notes': item_data['notes']
                    }
                )

    # Carol Johnson - Business Sophomore (PM focused)
    carol = User.objects.filter(username='carol_johnson').first()
    if carol and hasattr(carol, 'profile'):
        print("  Adding items for carol_johnson...")
        items_carol = [
            {'item': 'Hackathon Winner - FinTech App', 'status': 'COMPLETED', 'notes': 'Won 1st place at Harvard Business + Tech Hackathon'},
            {'item': 'Startup Founder - Launch MVP', 'status': 'IN_PROGRESS', 'notes': 'Building SaaS product for student organizations'},
            {'item': 'UI/UX Design Portfolio', 'status': 'IN_PROGRESS', 'notes': '5 case studies completed, working on 3 more'},
            {'item': 'Complete React Developer Course', 'status': 'COMPLETED', 'notes': 'Completed to build my startup MVP'},
            {'item': 'Technical Blog', 'status': 'PLANNED', 'notes': 'Want to blog about PM and startups'},
        ]

        for item_data in items_carol:
            item = PortfolioItem.objects.filter(title__icontains=item_data['item']).first()
            if item:
                UserChecklist.objects.get_or_create(
                    user_profile=carol.profile,
                    portfolio_item=item,
                    defaults={
                        'status': item_data['status'],
                        'notes': item_data['notes']
                    }
                )

    # David Kim - Data Science Junior
    david = User.objects.filter(username='david_kim').first()
    if david and hasattr(david, 'profile'):
        print("  Adding items for david_kim...")
        items_david = [
            {'item': 'Data Science Internship', 'status': 'COMPLETED', 'notes': 'Data Analyst Intern at Airbnb, Summer 2024'},
            {'item': 'Kaggle Competition - Top 10%', 'status': 'COMPLETED', 'notes': 'Placed 8th/1000+ in Titanic competition'},
            {'item': 'AWS Certified Solutions Architect', 'status': 'IN_PROGRESS', 'notes': 'Studying for certification, exam scheduled'},
            {'item': 'LeetCode - 300+ Problems Solved', 'status': 'IN_PROGRESS', 'notes': '200 problems solved so far'},
            {'item': 'Technical Blog', 'status': 'COMPLETED', 'notes': 'Data science blog with 1200+ monthly readers'},
        ]

        for item_data in items_david:
            item = PortfolioItem.objects.filter(title__icontains=item_data['item']).first()
            if item:
                UserChecklist.objects.get_or_create(
                    user_profile=david.profile,
                    portfolio_item=item,
                    defaults={
                        'status': item_data['status'],
                        'notes': item_data['notes']
                    }
                )

    # Emma Wilson - ME Freshman (Just starting)
    emma = User.objects.filter(username='emma_wilson').first()
    if emma and hasattr(emma, 'profile'):
        print("  Adding items for emma_wilson...")
        items_emma = [
            {'item': 'Complete React Developer Course', 'status': 'IN_PROGRESS', 'notes': 'Learning web dev for personal projects'},
            {'item': 'Technical Blog', 'status': 'PLANNED', 'notes': 'Want to document my engineering journey'},
            {'item': 'LeetCode - 300+ Problems Solved', 'status': 'PLANNED', 'notes': 'Starting with easy problems'},
        ]

        for item_data in items_emma:
            item = PortfolioItem.objects.filter(title__icontains=item_data['item']).first()
            if item:
                UserChecklist.objects.get_or_create(
                    user_profile=emma.profile,
                    portfolio_item=item,
                    defaults={
                        'status': item_data['status'],
                        'notes': item_data['notes']
                    }
                )

    # Demo Student - Intermediate level
    demo = User.objects.filter(username='demo_student').first()
    if demo and hasattr(demo, 'profile'):
        print("  Adding items for demo_student...")
        items_demo = [
            {'item': 'E-commerce Web Application', 'status': 'COMPLETED', 'notes': 'Built full-stack app with React and Node.js'},
            {'item': 'Mobile Fitness Tracking App', 'status': 'IN_PROGRESS', 'notes': 'Working on React Native version'},
            {'item': 'Complete React Developer Course', 'status': 'COMPLETED', 'notes': 'Completed with certificate'},
            {'item': 'LeetCode - 300+ Problems Solved', 'status': 'IN_PROGRESS', 'notes': '150 problems solved, targeting 300'},
            {'item': 'AWS Certified Solutions Architect', 'status': 'PLANNED', 'notes': 'Planning to get certified this year'},
            {'item': 'Open Source Contribution', 'status': 'PLANNED', 'notes': 'Looking for good first issues'},
        ]

        for item_data in items_demo:
            item = PortfolioItem.objects.filter(title__icontains=item_data['item']).first()
            if item:
                UserChecklist.objects.get_or_create(
                    user_profile=demo.profile,
                    portfolio_item=item,
                    defaults={
                        'status': item_data['status'],
                        'notes': item_data['notes']
                    }
                )

    # Grace Park - AI Research focus
    grace = User.objects.filter(username='grace_park').first()
    if grace and hasattr(grace, 'profile'):
        print("  Adding items for grace_park...")
        items_grace = [
            {'item': 'Machine Learning Internship at Google', 'status': 'COMPLETED', 'notes': 'DeepMind Research Intern 2024'},
            {'item': 'Research Publication in AI Conference', 'status': 'COMPLETED', 'notes': 'Published at ICML 2024'},
            {'item': 'Kaggle Competition - Top 10%', 'status': 'COMPLETED', 'notes': 'Top 5% in multiple ML competitions'},
            {'item': 'LeetCode - 300+ Problems Solved', 'status': 'COMPLETED', 'notes': '400+ problems for interview prep'},
        ]

        for item_data in items_grace:
            item = PortfolioItem.objects.filter(title__icontains=item_data['item']).first()
            if item:
                UserChecklist.objects.get_or_create(
                    user_profile=grace.profile,
                    portfolio_item=item,
                    defaults={
                        'status': item_data['status'],
                        'notes': item_data['notes']
                    }
                )

    # Henry Brown - Frontend focused
    henry = User.objects.filter(username='henry_brown').first()
    if henry and hasattr(henry, 'profile'):
        print("  Adding items for henry_brown...")
        items_henry = [
            {'item': 'Software Engineering Internship at FAANG', 'status': 'COMPLETED', 'notes': 'Frontend Intern at Stripe'},
            {'item': 'E-commerce Web Application', 'status': 'COMPLETED', 'notes': 'Built e-commerce platform with Next.js'},
            {'item': 'Open Source Contribution', 'status': 'COMPLETED', 'notes': '15+ PRs to Vue.js and React ecosystem'},
            {'item': 'Technical Blog', 'status': 'COMPLETED', 'notes': 'Frontend blog with 2000+ monthly readers'},
            {'item': 'System Design Course', 'status': 'IN_PROGRESS', 'notes': 'Preparing for senior SWE interviews'},
        ]

        for item_data in items_henry:
            item = PortfolioItem.objects.filter(title__icontains=item_data['item']).first()
            if item:
                UserChecklist.objects.get_or_create(
                    user_profile=henry.profile,
                    portfolio_item=item,
                    defaults={
                        'status': item_data['status'],
                        'notes': item_data['notes']
                    }
                )

def main():
    """Run the portfolio addition."""
    print("\n" + "="*60)
    print("ADDING PORTFOLIO CHECKLIST ITEMS TO DEMO USERS")
    print("="*60 + "\n")

    add_portfolio_to_users()

    # Show summary
    print("\n" + "="*60)
    print("PORTFOLIO CHECKLIST SUMMARY")
    print("="*60)

    for username in ['alice_chen', 'bob_martinez', 'carol_johnson', 'david_kim',
                     'emma_wilson', 'demo_student', 'grace_park', 'henry_brown']:
        user = User.objects.filter(username=username).first()
        if user and hasattr(user, 'profile'):
            checklist = UserChecklist.objects.filter(user_profile=user.profile)
            completed = checklist.filter(status='COMPLETED').count()
            in_progress = checklist.filter(status='IN_PROGRESS').count()
            planned = checklist.filter(status='PLANNED').count()
            total = checklist.count()
            completion = int((completed / total * 100)) if total > 0 else 0

            print(f"\n{username}:")
            print(f"  Total Items: {total}")
            print(f"  Completed: {completed} | In Progress: {in_progress} | Planned: {planned}")
            print(f"  Portfolio Complete: {completion}%")

    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()
