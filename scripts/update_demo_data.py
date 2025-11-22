#!/usr/bin/env python3
"""Update and enhance demo data with more comprehensive examples."""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
sys.path.insert(0, '/home/user/Assignment_Project_Om_opate22')
os.environ.setdefault('DJANGO_SECRET_KEY', 'demo-key-for-testing')
os.environ.setdefault('DJANGO_DEBUG', 'True')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Assignment_Project_Om_opate22.Settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile, Club, PortfolioItem
from colleges.models import College, Major
from careers.models import Career

def enhance_existing_users():
    """Add more details to existing users."""
    print("Enhancing existing user profiles...")

    # Bob Martinez (EE, Junior) - Hardware focused
    bob = User.objects.filter(username='bob_martinez').first()
    if bob and hasattr(bob, 'profile'):
        bob.profile.career_goals = 'Become a robotics engineer working on autonomous systems and hardware integration'
        bob.profile.work_experience = 'Summer intern at Tesla - Autopilot hardware team'
        bob.profile.preferred_industries = 'Automotive, Robotics, IoT, Hardware'
        bob.profile.save()
        print("  Enhanced bob_martinez profile")

    # Carol Johnson (Business, Sophomore) - Business/startup focused
    carol = User.objects.filter(username='carol_johnson').first()
    if carol and hasattr(carol, 'profile'):
        carol.profile.career_goals = 'Launch my own startup or become a product manager at a tech company'
        carol.profile.preferred_industries = 'Technology, E-commerce, Fintech, Consulting'
        carol.profile.work_experience = 'Marketing Intern at McKinsey & Company'
        carol.profile.save()
        print("  Enhanced carol_johnson profile")

    # David Kim (Data Science, Junior)
    david = User.objects.filter(username='david_kim').first()
    if david and hasattr(david, 'profile'):
        david.profile.work_experience = 'Data Analyst Intern at Airbnb (Summer 2024)'
        david.profile.career_goals = 'Become a senior data scientist or ML engineer at a top tech company'
        david.profile.preferred_industries = 'Technology, Finance, E-commerce'
        david.profile.preferred_positions = 'Data Scientist, ML Engineer, Data Engineer'
        david.profile.save()
        print("  Enhanced david_kim profile")

    # Emma Wilson (ME, Freshman)
    emma = User.objects.filter(username='emma_wilson').first()
    if emma and hasattr(emma, 'profile'):
        emma.profile.career_goals = 'Design sustainable aircraft or work in renewable energy systems'
        emma.profile.clubs_interest = 'Engineering clubs, sustainability groups, women in STEM'
        emma.profile.preferred_industries = 'Aerospace, Sustainable Energy, Manufacturing'
        emma.profile.save()
        print("  Enhanced emma_wilson profile")

    # Alice Chen (CS, Senior) - Advanced projects
    alice = User.objects.filter(username='alice_chen').first()
    if alice and hasattr(alice, 'profile'):
        alice.profile.career_goals = 'AI Research Scientist or ML Engineer at top AI lab'
        alice.profile.work_experience = 'Research Assistant at MIT CSAIL, ML Intern at Google Brain'
        alice.profile.preferred_industries = 'AI/ML, Research, Technology'
        alice.profile.preferred_company = 'Google, OpenAI, DeepMind, Meta AI'
        alice.profile.save()
        print("  Enhanced alice_chen profile")

    # Demo student
    demo = User.objects.filter(username='demo_student').first()
    if demo and hasattr(demo, 'profile'):
        demo.profile.career_goals = 'Full-stack developer or software engineer at innovative tech company'
        demo.profile.work_experience = 'Software Engineering Intern at local startup'
        demo.profile.preferred_industries = 'Technology, Startups, SaaS'
        demo.profile.save()
        print("  Enhanced demo_student profile")

def create_additional_users():
    """Create more diverse demo users."""
    print("Creating additional demo users...")

    additional_users = [
        {
            'username': 'frank_zhang',
            'email': 'frank@example.com',
            'first_name': 'Frank',
            'last_name': 'Zhang',
            'profile': {
                'college': 'MIT',
                'major': 'Computer Science',
                'gpa': 3.45,
                'academic_year': 'SO',
                'skills': 'Python, C, Linux, Git, Algorithms',
                'interests': 'Open Source, Systems Programming, Cybersecurity',
                'career_goals': 'Work on open source projects and contribute to Linux kernel',
                'work_experience': 'Teaching Assistant for Introduction to Programming'
            }
        },
        {
            'username': 'grace_park',
            'email': 'grace@example.com',
            'first_name': 'Grace',
            'last_name': 'Park',
            'profile': {
                'college': 'Stanford',
                'major': 'Computer Science',
                'gpa': 3.95,
                'academic_year': 'JR',
                'skills': 'Python, TensorFlow, PyTorch, Computer Vision, NLP',
                'interests': 'Artificial Intelligence, Research, Healthcare AI',
                'career_goals': 'PhD in AI/ML, research scientist at top tech company or academia',
                'work_experience': 'Research Assistant - Stanford AI Lab, AI Research Intern at DeepMind'
            }
        },
        {
            'username': 'henry_brown',
            'email': 'henry@example.com',
            'first_name': 'Henry',
            'last_name': 'Brown',
            'profile': {
                'college': 'UC Berkeley',
                'major': 'Computer Science',
                'gpa': 3.55,
                'academic_year': 'SR',
                'skills': 'JavaScript, TypeScript, React, Vue, Node.js, GraphQL',
                'interests': 'Web Development, UI/UX, Developer Tools',
                'career_goals': 'Senior Frontend Engineer or Engineering Manager',
                'work_experience': 'Frontend Engineer Intern at Stripe, Full-stack Intern at Notion'
            }
        },
        {
            'username': 'isabel_garcia',
            'email': 'isabel@example.com',
            'first_name': 'Isabel',
            'last_name': 'Garcia',
            'profile': {
                'college': 'Harvard',
                'major': 'Computer Science',
                'gpa': 3.7,
                'academic_year': 'JR',
                'skills': 'Figma, Adobe XD, User Research, Prototyping, HTML/CSS',
                'interests': 'Product Design, Accessibility, Human-Computer Interaction',
                'career_goals': 'Lead product designer at a mission-driven tech company',
                'work_experience': 'UX Design Intern at Microsoft, Design Intern at Duolingo'
            }
        },
        {
            'username': 'jason_lee',
            'email': 'jason@example.com',
            'first_name': 'Jason',
            'last_name': 'Lee',
            'profile': {
                'college': 'Stanford',
                'major': 'Electrical Engineering',
                'gpa': 3.8,
                'academic_year': 'SR',
                'skills': 'FPGA, Verilog, ARM, Embedded C, PCB Design',
                'interests': 'Hardware Engineering, Chip Design, IoT',
                'career_goals': 'Hardware Engineer at Apple or semiconductor company',
                'work_experience': 'Hardware Engineering Intern at Apple, Research at Stanford Hardware Lab'
            }
        }
    ]

    for user_data in additional_users:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        if created:
            user.set_password('demo123')
            user.save()
            print(f"  Created user: {user.username}")

        college = College.objects.filter(abbreviation=user_data['profile']['college']).first()
        major = Major.objects.filter(name=user_data['profile']['major']).first()

        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'college': college,
                'major': major,
                'gpa': user_data['profile']['gpa'],
                'academic_year': user_data['profile']['academic_year'],
                'skills': user_data['profile']['skills'],
                'personal_interests': user_data['profile']['interests'],
                'career_goals': user_data['profile'].get('career_goals', ''),
                'work_experience': user_data['profile'].get('work_experience', '')
            }
        )

def add_more_portfolio_items():
    """Add more diverse portfolio items."""
    print("Adding more portfolio items...")

    new_items = [
        {
            'title': 'iOS Mobile App Development',
            'description': 'Build native iOS applications using Swift and SwiftUI with App Store deployment',
            'item_type': 'PROJECT',
            'difficulty_level': 'INTERMEDIATE',
            'estimated_hours': 100,
            'skills_gained': 'Swift, SwiftUI, iOS Development, Xcode, App Store'
        },
        {
            'title': 'Google Cloud Professional Certificate',
            'description': 'Professional certification for Google Cloud Platform architecture and engineering',
            'item_type': 'CERT',
            'difficulty_level': 'ADVANCED',
            'estimated_hours': 60,
            'skills_gained': 'GCP, Cloud Architecture, Kubernetes, BigQuery'
        },
        {
            'title': 'Research Publication in AI Conference',
            'description': 'Publish original research at top-tier AI/ML conference (NeurIPS, ICML, CVPR)',
            'item_type': 'MILESTONE',
            'difficulty_level': 'ADVANCED',
            'estimated_hours': 400,
            'skills_gained': 'Research, Academic Writing, Machine Learning, Peer Review'
        },
        {
            'title': 'Contribute to Open Source (10+ PRs)',
            'description': 'Make meaningful contributions to popular open source projects on GitHub',
            'item_type': 'PROJECT',
            'difficulty_level': 'INTERMEDIATE',
            'estimated_hours': 80,
            'skills_gained': 'Git, Open Source, Code Review, Community Collaboration'
        },
        {
            'title': 'Software Engineering Internship at FAANG',
            'description': 'Summer internship at Facebook, Amazon, Apple, Netflix, or Google',
            'item_type': 'INTERNSHIP',
            'difficulty_level': 'ADVANCED',
            'estimated_hours': 480,
            'skills_gained': 'Large-scale Systems, Professional Development, Agile, Mentorship'
        },
        {
            'title': 'Kaggle Competition - Top 10%',
            'description': 'Place in top 10% of a Kaggle machine learning competition',
            'item_type': 'COMPETITION',
            'difficulty_level': 'ADVANCED',
            'estimated_hours': 120,
            'skills_gained': 'ML Competition, Feature Engineering, Model Tuning, Data Science'
        },
        {
            'title': 'Technical Blog with 1000+ Readers',
            'description': 'Start a technical blog and grow audience to 1000+ monthly readers',
            'item_type': 'MILESTONE',
            'difficulty_level': 'BEGINNER',
            'estimated_hours': 60,
            'skills_gained': 'Technical Writing, Content Creation, SEO, Community Building'
        },
        {
            'title': 'System Design Course',
            'description': 'Complete comprehensive system design course covering scalability and architecture',
            'item_type': 'CERT',
            'difficulty_level': 'INTERMEDIATE',
            'estimated_hours': 50,
            'skills_gained': 'System Design, Scalability, Databases, Caching, Load Balancing'
        },
        {
            'title': 'LeetCode - 300+ Problems Solved',
            'description': 'Solve 300+ LeetCode problems across easy, medium, and hard difficulties',
            'item_type': 'MILESTONE',
            'difficulty_level': 'INTERMEDIATE',
            'estimated_hours': 150,
            'skills_gained': 'Algorithms, Data Structures, Problem Solving, Interview Prep'
        },
        {
            'title': 'Startup Founder - Launch MVP',
            'description': 'Found a startup and launch minimum viable product with real users',
            'item_type': 'PROJECT',
            'difficulty_level': 'ADVANCED',
            'estimated_hours': 500,
            'skills_gained': 'Entrepreneurship, Product Development, Marketing, Fundraising'
        }
    ]

    for item_data in new_items:
        PortfolioItem.objects.get_or_create(
            title=item_data['title'],
            defaults=item_data
        )

def add_more_careers():
    """Add more diverse career paths."""
    print("Adding more career paths...")

    new_careers = [
        {
            'title': 'Backend Engineer',
            'company': 'Tech Companies',
            'description': 'Build scalable server-side applications, APIs, and microservices. Work with databases, caching, and distributed systems. Salary: $90,000 - $160,000. Growth: 20%',
            'industries': ['Technology', 'SaaS', 'E-commerce'],
            'skills': ['Python', 'Java', 'Go', 'PostgreSQL', 'Redis', 'Docker']
        },
        {
            'title': 'Mobile Developer (iOS/Android)',
            'company': 'Mobile Companies',
            'description': 'Create native mobile applications for iOS and Android platforms. Focus on performance, user experience, and platform APIs. Salary: $85,000 - $155,000. Growth: 18%',
            'industries': ['Mobile', 'Technology', 'Gaming'],
            'skills': ['Swift', 'Kotlin', 'React Native', 'Flutter', 'Mobile UI/UX']
        },
        {
            'title': 'Engineering Manager',
            'company': 'Tech Leadership',
            'description': 'Lead engineering teams, manage technical roadmaps, and drive project execution. Balance technical and people management. Salary: $130,000 - $220,000. Growth: 12%',
            'industries': ['Technology', 'Management', 'Leadership'],
            'skills': ['Leadership', 'Project Management', 'Technical Strategy', 'Mentoring', 'Agile']
        },
        {
            'title': 'Research Scientist',
            'company': 'Research Labs',
            'description': 'Conduct cutting-edge research in AI, ML, or computer science. Publish papers and advance the field. Salary: $100,000 - $180,000. Growth: 22%',
            'industries': ['Research', 'AI/ML', 'Academia'],
            'skills': ['Research', 'Machine Learning', 'Mathematics', 'Academic Writing', 'Python']
        },
        {
            'title': 'Site Reliability Engineer (SRE)',
            'company': 'Cloud Companies',
            'description': 'Ensure system reliability, scalability, and performance. Build monitoring, alerting, and automation tools. Salary: $100,000 - $170,000. Growth: 24%',
            'industries': ['Technology', 'Cloud', 'Infrastructure'],
            'skills': ['Linux', 'Kubernetes', 'Monitoring', 'Automation', 'Python', 'Terraform']
        },
        {
            'title': 'Quantitative Analyst',
            'company': 'Finance/Trading',
            'description': 'Apply mathematical and statistical methods to financial markets. Build trading algorithms and risk models. Salary: $120,000 - $250,000. Growth: 15%',
            'industries': ['Finance', 'Trading', 'Hedge Funds'],
            'skills': ['Mathematics', 'Statistics', 'Python', 'C++', 'Financial Modeling']
        },
        {
            'title': 'Technical Product Manager',
            'company': 'Product Companies',
            'description': 'Bridge technical and business teams. Define product requirements with deep technical understanding. Salary: $110,000 - $190,000. Growth: 16%',
            'industries': ['Technology', 'Product', 'SaaS'],
            'skills': ['Product Management', 'Technical Knowledge', 'APIs', 'SQL', 'Analytics']
        },
        {
            'title': 'Security Engineer',
            'company': 'Security Companies',
            'description': 'Build and maintain security systems, conduct audits, and respond to incidents. Protect infrastructure and data. Salary: $95,000 - $165,000. Growth: 28%',
            'industries': ['Cybersecurity', 'Technology', 'Finance'],
            'skills': ['Security', 'Penetration Testing', 'Incident Response', 'Cryptography', 'Network Security']
        }
    ]

    for career_data in new_careers:
        Career.objects.get_or_create(
            title=career_data['title'],
            defaults=career_data
        )

def main():
    """Run all update functions."""
    print("\n" + "="*60)
    print("UPDATING DEMO DATA WITH ENHANCEMENTS")
    print("="*60 + "\n")

    enhance_existing_users()
    create_additional_users()
    add_more_portfolio_items()
    add_more_careers()

    # Final counts
    print("\n" + "="*60)
    print("UPDATED DEMO DATA SUMMARY")
    print("="*60)
    print(f"Total Users: {User.objects.count()}")
    print(f"Total Portfolio Items: {PortfolioItem.objects.count()}")
    print(f"Total Clubs: {Club.objects.count()}")
    print(f"Total Careers: {Career.objects.count()}")
    print("\nAll demo accounts use password: 'demo123'")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
