#!/usr/bin/env python3
"""Populate database with comprehensive demo data."""
import os
import sys
import django

# Setup Django
sys.path.insert(0, '/home/user/Assignment_Project_Om_opate22')
os.environ.setdefault('DJANGO_SECRET_KEY', 'demo-key-for-testing')
os.environ.setdefault('DJANGO_DEBUG', 'True')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Assignment_Project_Om_opate22.Settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile, Club, PortfolioItem, CareerPath
from colleges.models import College, Major, Course
from careers.models import Career
from catalog.models import DegreeCategory, DegreeRequirement

def create_users():
    """Create diverse demo users."""
    print("Creating demo users...")

    users_data = [
        {
            'username': 'alice_chen',
            'email': 'alice@example.com',
            'first_name': 'Alice',
            'last_name': 'Chen',
            'profile': {
                'college': 'MIT',
                'major': 'Computer Science',
                'gpa': 3.9,
                'academic_year': 'SR',
                'skills': 'Python, Java, React, Machine Learning, Data Structures, Algorithms',
                'interests': 'Artificial Intelligence, Software Engineering, Research'
            }
        },
        {
            'username': 'bob_martinez',
            'email': 'bob@example.com',
            'first_name': 'Bob',
            'last_name': 'Martinez',
            'profile': {
                'college': 'Stanford',
                'major': 'Electrical Engineering',
                'gpa': 3.7,
                'academic_year': 'JR',
                'skills': 'Circuit Design, MATLAB, C++, Embedded Systems, Signal Processing',
                'interests': 'Robotics, Hardware Design, IoT'
            }
        },
        {
            'username': 'carol_johnson',
            'email': 'carol@example.com',
            'first_name': 'Carol',
            'last_name': 'Johnson',
            'profile': {
                'college': 'Harvard',
                'major': 'Business Administration',
                'gpa': 3.8,
                'academic_year': 'SO',
                'skills': 'Marketing, Finance, Excel, Public Speaking, Project Management',
                'interests': 'Entrepreneurship, Consulting, Product Management'
            }
        },
        {
            'username': 'david_kim',
            'email': 'david@example.com',
            'first_name': 'David',
            'last_name': 'Kim',
            'profile': {
                'college': 'UC Berkeley',
                'major': 'Data Science',
                'gpa': 3.85,
                'academic_year': 'JR',
                'skills': 'Python, R, SQL, Tableau, Statistics, Pandas, NumPy',
                'interests': 'Data Analytics, Machine Learning, Business Intelligence'
            }
        },
        {
            'username': 'emma_wilson',
            'email': 'emma@example.com',
            'first_name': 'Emma',
            'last_name': 'Wilson',
            'profile': {
                'college': 'MIT',
                'major': 'Mechanical Engineering',
                'gpa': 3.6,
                'academic_year': 'FR',
                'skills': 'CAD, SolidWorks, Physics, Calculus, Python',
                'interests': 'Aerospace, Sustainable Energy, Manufacturing'
            }
        }
    ]

    for user_data in users_data:
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

        # Update or create profile
        college = College.objects.filter(abbreviation=user_data['profile']['college']).first()
        major = Major.objects.filter(name=user_data['profile']['major']).first()

        profile, _ = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'college': college,
                'major': major,
                'gpa': user_data['profile']['gpa'],
                'academic_year': user_data['profile']['academic_year'],
                'skills': user_data['profile']['skills'],
                'personal_interests': user_data['profile']['interests']
            }
        )

def create_portfolio_items():
    """Create comprehensive portfolio items."""
    print("Creating portfolio items...")

    items_data = [
        {
            'title': 'E-commerce Web Application',
            'description': 'Full-stack e-commerce platform with payment integration, user authentication, and admin dashboard',
            'item_type': 'PROJECT',
            'difficulty_level': 'ADVANCED',
            'estimated_hours': 120,
            'skills_gained': 'React, Node.js, MongoDB, Stripe API, Authentication'
        },
        {
            'title': 'AWS Certified Solutions Architect',
            'description': 'Professional certification demonstrating expertise in AWS cloud architecture and services',
            'item_type': 'CERT',
            'difficulty_level': 'INTERMEDIATE',
            'estimated_hours': 80,
            'skills_gained': 'AWS, Cloud Computing, Architecture Design, Security'
        },
        {
            'title': 'Mobile Fitness Tracking App',
            'description': 'React Native app with activity tracking, calorie counter, and social features',
            'item_type': 'PROJECT',
            'difficulty_level': 'INTERMEDIATE',
            'estimated_hours': 100,
            'skills_gained': 'React Native, Mobile Development, API Integration'
        },
        {
            'title': 'Machine Learning Internship at Google',
            'description': 'Summer internship working on recommendation systems and neural networks',
            'item_type': 'INTERNSHIP',
            'difficulty_level': 'ADVANCED',
            'estimated_hours': 480,
            'skills_gained': 'Python, TensorFlow, Neural Networks, Recommendation Systems'
        },
        {
            'title': 'Open Source Contribution to React',
            'description': 'Bug fixes and feature additions to the React JavaScript library',
            'item_type': 'PROJECT',
            'difficulty_level': 'ADVANCED',
            'estimated_hours': 60,
            'skills_gained': 'JavaScript, React Internals, Open Source, Git'
        },
        {
            'title': 'Hackathon Winner - FinTech App',
            'description': 'Won 1st place at MIT Hackathon for personal finance management app',
            'item_type': 'COMPETITION',
            'difficulty_level': 'INTERMEDIATE',
            'estimated_hours': 48,
            'skills_gained': 'Rapid Prototyping, Teamwork, Finance APIs, Presentation'
        },
        {
            'title': 'Build a Blockchain from Scratch',
            'description': 'Educational project implementing a basic blockchain and cryptocurrency',
            'item_type': 'PROJECT',
            'difficulty_level': 'ADVANCED',
            'estimated_hours': 80,
            'skills_gained': 'Cryptography, Blockchain, Python, Distributed Systems'
        },
        {
            'title': 'UI/UX Design Portfolio',
            'description': 'Collection of 10+ web and mobile app designs with user research documentation',
            'item_type': 'PROJECT',
            'difficulty_level': 'INTERMEDIATE',
            'estimated_hours': 90,
            'skills_gained': 'Figma, User Research, Wireframing, Prototyping'
        },
        {
            'title': 'Complete React Developer Course',
            'description': 'Comprehensive online course covering React, Redux, and modern web development',
            'item_type': 'CERT',
            'difficulty_level': 'BEGINNER',
            'estimated_hours': 40,
            'skills_gained': 'React, Redux, JavaScript, Web Development'
        },
        {
            'title': 'Data Science Internship',
            'description': 'Analyze business data and create predictive models for a tech startup',
            'item_type': 'INTERNSHIP',
            'difficulty_level': 'INTERMEDIATE',
            'estimated_hours': 320,
            'skills_gained': 'Python, Pandas, Machine Learning, Data Visualization'
        }
    ]

    for item_data in items_data:
        PortfolioItem.objects.get_or_create(
            title=item_data['title'],
            defaults=item_data
        )

def create_clubs():
    """Create diverse clubs."""
    print("Creating clubs...")

    clubs_data = [
        {
            'name': 'Computer Science Society',
            'college': 'MIT',
            'description': 'Student organization for CS majors. Weekly coding challenges, tech talks, and networking events.',
            'category': 'Academic'
        },
        {
            'name': 'Robotics Club',
            'college': 'MIT',
            'description': 'Design and build robots for competitions. Participate in FIRST Robotics and other challenges.',
            'category': 'Academic'
        },
        {
            'name': 'Entrepreneurship Association',
            'college': 'Stanford',
            'description': 'Support student startups with mentorship, funding opportunities, and pitch competitions.',
            'category': 'Professional'
        },
        {
            'name': 'Women in Technology',
            'college': 'Stanford',
            'description': 'Empowering women in tech through workshops, mentorship, and industry connections.',
            'category': 'Professional'
        },
        {
            'name': 'Data Science Club',
            'college': 'UC Berkeley',
            'description': 'Explore data analytics, machine learning, and AI through projects and competitions.',
            'category': 'Academic'
        },
        {
            'name': 'Investment Banking Club',
            'college': 'Harvard',
            'description': 'Prepare for finance careers with case studies, networking, and industry insights.',
            'category': 'Professional'
        },
        {
            'name': 'Debate Team',
            'college': 'Harvard',
            'description': 'Competitive debate team participating in national tournaments and public speaking events.',
            'category': 'Social'
        },
        {
            'name': 'Hackathon Organizers',
            'college': 'MIT',
            'description': 'Organize and run hackathons, bringing together students to build innovative projects.',
            'category': 'Academic'
        },
        {
            'name': 'AI Research Group',
            'college': 'Stanford',
            'description': 'Undergraduate research group focusing on artificial intelligence and deep learning.',
            'category': 'Academic'
        },
        {
            'name': 'Product Management Club',
            'college': 'UC Berkeley',
            'description': 'Learn product management skills through case studies, speakers, and PM simulations.',
            'category': 'Professional'
        }
    ]

    for club_data in clubs_data:
        college = College.objects.filter(abbreviation=club_data['college']).first()
        Club.objects.get_or_create(
            name=club_data['name'],
            college=college,
            defaults={
                'description': club_data['description'],
                'category': club_data['category']
            }
        )

def create_careers():
    """Create more career options."""
    print("Creating careers...")

    careers_data = [
        {
            'title': 'Full Stack Developer',
            'company': 'Tech Companies',
            'description': 'Build end-to-end web applications using modern frameworks like React, Node.js, and databases. Work on both frontend UI and backend systems. Salary: $85,000 - $150,000. Growth: 22%',
            'industries': ['Technology', 'Software', 'Startups'],
            'skills': ['JavaScript', 'React', 'Node.js', 'Databases', 'APIs']
        },
        {
            'title': 'Data Scientist',
            'company': 'Data Companies',
            'description': 'Analyze complex data sets using statistical methods, machine learning, and data visualization to drive business decisions. Salary: $95,000 - $165,000. Growth: 35%',
            'industries': ['Technology', 'Finance', 'Healthcare'],
            'skills': ['Python', 'Machine Learning', 'Statistics', 'Data Visualization', 'SQL']
        },
        {
            'title': 'Product Manager',
            'company': 'Product Companies',
            'description': 'Lead product strategy and roadmap, coordinate cross-functional teams, and deliver features that users love. Salary: $100,000 - $180,000. Growth: 18%',
            'industries': ['Technology', 'E-commerce', 'SaaS'],
            'skills': ['Product Strategy', 'Analytics', 'Communication', 'Agile', 'User Research']
        },
        {
            'title': 'Machine Learning Engineer',
            'company': 'AI Companies',
            'description': 'Design and implement ML models, work with neural networks, and deploy AI systems at scale. Salary: $110,000 - $200,000. Growth: 40%',
            'industries': ['AI/ML', 'Technology', 'Research'],
            'skills': ['Python', 'TensorFlow', 'PyTorch', 'Neural Networks', 'Deep Learning']
        },
        {
            'title': 'UX/UI Designer',
            'company': 'Design Studios',
            'description': 'Create intuitive user interfaces and experiences through research, wireframing, prototyping, and user testing. Salary: $70,000 - $130,000. Growth: 15%',
            'industries': ['Design', 'Technology', 'Consulting'],
            'skills': ['Figma', 'User Research', 'Prototyping', 'Visual Design', 'Usability Testing']
        },
        {
            'title': 'DevOps Engineer',
            'company': 'Cloud Companies',
            'description': 'Automate infrastructure, manage CI/CD pipelines, and ensure reliable system deployment and monitoring. Salary: $95,000 - $160,000. Growth: 25%',
            'industries': ['Technology', 'Cloud Computing', 'Infrastructure'],
            'skills': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Linux']
        },
        {
            'title': 'Cybersecurity Analyst',
            'company': 'Security Firms',
            'description': 'Protect systems from security threats, conduct penetration testing, and implement security best practices. Salary: $85,000 - $145,000. Growth: 31%',
            'industries': ['Cybersecurity', 'Finance', 'Government'],
            'skills': ['Network Security', 'Penetration Testing', 'Cryptography', 'Risk Analysis', 'Security Tools']
        },
        {
            'title': 'Cloud Architect',
            'company': 'Enterprise Companies',
            'description': 'Design scalable cloud infrastructure using AWS, Azure, or GCP. Optimize for performance, cost, and reliability. Salary: $120,000 - $200,000. Growth: 28%',
            'industries': ['Cloud Computing', 'Technology', 'Enterprise'],
            'skills': ['AWS', 'Azure', 'Architecture Design', 'Scalability', 'Cost Optimization']
        }
    ]

    for career_data in careers_data:
        Career.objects.get_or_create(
            title=career_data['title'],
            defaults=career_data
        )

def create_courses():
    """Create more course offerings."""
    print("Creating courses...")

    courses_data = [
        {
            'subject': 'CS',
            'number': '50',
            'title': 'Introduction to Computer Science',
            'college': 'Harvard',
            'credits': 4,
            'description': 'Foundational computer science course covering algorithms, data structures, and programming.'
        },
        {
            'subject': 'CS',
            'number': '106A',
            'title': 'Programming Methodology',
            'college': 'Stanford',
            'credits': 5,
            'description': 'Introduction to programming using Java, covering problem-solving and software engineering principles.'
        },
        {
            'subject': 'CS',
            'number': '188',
            'title': 'Artificial Intelligence',
            'college': 'UC Berkeley',
            'credits': 4,
            'description': 'Machine learning, neural networks, search algorithms, and AI applications.'
        },
        {
            'subject': 'CS',
            'number': '6.006',
            'title': 'Introduction to Algorithms',
            'college': 'MIT',
            'credits': 4,
            'description': 'Design and analysis of algorithms including sorting, graph algorithms, and dynamic programming.'
        },
        {
            'subject': 'CS',
            'number': '229',
            'title': 'Machine Learning',
            'college': 'Stanford',
            'credits': 4,
            'description': 'Supervised and unsupervised learning, deep learning, and practical ML applications.'
        },
        {
            'subject': 'DATA',
            'number': '100',
            'title': 'Principles of Data Science',
            'college': 'UC Berkeley',
            'credits': 4,
            'description': 'Data cleaning, exploration, visualization, and statistical inference using Python.'
        },
        {
            'subject': 'CS',
            'number': '6.034',
            'title': 'Artificial Intelligence',
            'college': 'MIT',
            'credits': 4,
            'description': 'Search, knowledge representation, learning, and neural networks.'
        },
        {
            'subject': 'CS',
            'number': '161',
            'title': 'Computer Security',
            'college': 'Stanford',
            'credits': 3,
            'description': 'Cryptography, network security, web security, and secure system design.'
        }
    ]

    from catalog.models import Course as CatalogCourse
    for course_data in courses_data:
        college = College.objects.filter(abbreviation=course_data['college']).first()
        if not college:
            continue

        CatalogCourse.objects.get_or_create(
            subject=course_data['subject'],
            number=course_data['number'],
            college=college,
            defaults={
                'title': course_data['title'],
                'credits': course_data['credits'],
                'description': course_data['description']
            }
        )

def create_categories():
    """Create catalog categories."""
    print("Creating degree categories...")

    # Get CS major from MIT
    cs_major = Major.objects.filter(name='Computer Science', college__abbreviation='MIT').first()
    if not cs_major:
        print("  Skipping categories - CS major not found")
        return

    categories_data = [
        {'name': 'Core Requirements', 'min_credits': 40},
        {'name': 'Major Requirements', 'min_credits': 60},
        {'name': 'Electives', 'min_credits': 20},
        {'name': 'General Education', 'min_credits': 30},
    ]

    for cat_data in categories_data:
        DegreeCategory.objects.get_or_create(
            name=cat_data['name'],
            major=cs_major,
            defaults={'min_credits': cat_data['min_credits']}
        )

def main():
    """Run all data population functions."""
    print("\n" + "="*60)
    print("POPULATING DATABASE WITH COMPREHENSIVE DEMO DATA")
    print("="*60 + "\n")

    create_users()
    create_portfolio_items()
    create_clubs()
    create_careers()
    create_courses()
    create_categories()

    print("\n" + "="*60)
    print("DEMO DATA POPULATION COMPLETE!")
    print("="*60)
    print("\nDemo Users Created (all passwords: 'demo123'):")
    print("  - alice_chen (CS @ MIT, Senior, GPA 3.9)")
    print("  - bob_martinez (EE @ Stanford, Junior, GPA 3.7)")
    print("  - carol_johnson (Business @ Harvard, Sophomore, GPA 3.8)")
    print("  - david_kim (Data Science @ Berkeley, Junior, GPA 3.85)")
    print("  - emma_wilson (ME @ MIT, Freshman, GPA 3.6)")
    print("  - demo_student (existing user)")
    print("\nYou can now login with any of these accounts to see how different")
    print("profiles, majors, and academic years display in the dashboard!")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
