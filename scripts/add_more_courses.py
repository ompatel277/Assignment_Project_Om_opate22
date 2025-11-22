#!/usr/bin/env python3
"""Add courses for all demo user majors."""
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

from accounts.models import Course
from colleges.models import Major, College

def add_courses_for_major(major_name, college_abbr, courses_data):
    """Add courses for a specific major at a college."""
    try:
        major = Major.objects.get(name=major_name, college__abbreviation=college_abbr)
        print(f"\nAdding courses for {major_name} at {college_abbr}...")

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                subject=course_data['subject'],
                number=course_data['number'],
                major=major,
                defaults={
                    'title': course_data['title'],
                    'credits': course_data.get('credits', 4),
                    'description': course_data.get('description', '')
                }
            )
            if created:
                print(f"  ✓ Created: {course.subject} {course.number}")
    except Major.DoesNotExist:
        print(f"  ✗ Major '{major_name}' at {college_abbr} not found")

# Courses for Computer Science at UIUC
uiuc_cs_courses = [
    {'subject': 'CS', 'number': '124', 'title': 'Introduction to Computer Science I', 'credits': 3},
    {'subject': 'CS', 'number': '128', 'title': 'Introduction to Computer Science II', 'credits': 3},
    {'subject': 'CS', 'number': '173', 'title': 'Discrete Structures', 'credits': 3},
    {'subject': 'CS', 'number': '225', 'title': 'Data Structures', 'credits': 4},
    {'subject': 'CS', 'number': '233', 'title': 'Computer Architecture', 'credits': 4},
    {'subject': 'CS', 'number': '341', 'title': 'System Programming', 'credits': 4},
    {'subject': 'CS', 'number': '357', 'title': 'Numerical Methods I', 'credits': 3},
    {'subject': 'CS', 'number': '374', 'title': 'Introduction to Algorithms & Models of Computation', 'credits': 4},
    {'subject': 'CS', 'number': '411', 'title': 'Database Systems', 'credits': 3},
    {'subject': 'CS', 'number': '421', 'title': 'Programming Languages & Compilers', 'credits': 3},
    {'subject': 'CS', 'number': '440', 'title': 'Artificial Intelligence', 'credits': 3},
    {'subject': 'CS', 'number': '446', 'title': 'Machine Learning', 'credits': 4},
]

# Courses for Computer Science at MIT
mit_cs_courses = [
    {'subject': 'CS', 'number': '6.0001', 'title': 'Introduction to Computer Science and Programming in Python', 'credits': 6},
    {'subject': 'CS', 'number': '6.0002', 'title': 'Introduction to Computational Thinking and Data Science', 'credits': 6},
    {'subject': 'CS', 'number': '6.006', 'title': 'Introduction to Algorithms', 'credits': 12},
    {'subject': 'CS', 'number': '6.031', 'title': 'Elements of Software Construction', 'credits': 12},
    {'subject': 'CS', 'number': '6.034', 'title': 'Artificial Intelligence', 'credits': 12},
    {'subject': 'CS', 'number': '6.036', 'title': 'Introduction to Machine Learning', 'credits': 12},
    {'subject': 'CS', 'number': '6.046', 'title': 'Design and Analysis of Algorithms', 'credits': 12},
]

# Courses for Computer Science at Stanford
stanford_cs_courses = [
    {'subject': 'CS', 'number': '106A', 'title': 'Programming Methodology', 'credits': 5},
    {'subject': 'CS', 'number': '106B', 'title': 'Programming Abstractions', 'credits': 5},
    {'subject': 'CS', 'number': '107', 'title': 'Computer Organization & Systems', 'credits': 5},
    {'subject': 'CS', 'number': '109', 'title': 'Introduction to Probability for Computer Scientists', 'credits': 5},
    {'subject': 'CS', 'number': '161', 'title': 'Design and Analysis of Algorithms', 'credits': 5},
    {'subject': 'CS', 'number': '221', 'title': 'Artificial Intelligence: Principles and Techniques', 'credits': 3},
    {'subject': 'CS', 'number': '229', 'title': 'Machine Learning', 'credits': 3},
]

# Courses for Computer Science at Harvard
harvard_cs_courses = [
    {'subject': 'CS', 'number': '50', 'title': 'Introduction to Computer Science', 'credits': 4},
    {'subject': 'CS', 'number': '51', 'title': 'Abstraction and Design in Computation', 'credits': 4},
    {'subject': 'CS', 'number': '61', 'title': 'Systems Programming and Machine Organization', 'credits': 4},
    {'subject': 'CS', 'number': '121', 'title': 'Introduction to Theoretical Computer Science', 'credits': 4},
    {'subject': 'CS', 'number': '124', 'title': 'Data Structures and Algorithms', 'credits': 4},
    {'subject': 'CS', 'number': '181', 'title': 'Machine Learning', 'credits': 4},
]

# Data Science courses for UC Berkeley
berkeley_ds_courses = [
    {'subject': 'DATA', 'number': '8', 'title': 'Foundations of Data Science', 'credits': 4},
    {'subject': 'DATA', 'number': '100', 'title': 'Principles and Techniques of Data Science', 'credits': 4},
    {'subject': 'DATA', 'number': '102', 'title': 'Data, Inference, and Decisions', 'credits': 4},
    {'subject': 'DATA', 'number': '140', 'title': 'Probability for Data Science', 'credits': 4},
]

# Electrical Engineering courses for Stanford
stanford_ee_courses = [
    {'subject': 'EE', 'number': '101A', 'title': 'Circuits I', 'credits': 4},
    {'subject': 'EE', 'number': '101B', 'title': 'Circuits II', 'credits': 4},
    {'subject': 'EE', 'number': '102A', 'title': 'Signal Processing and Linear Systems I', 'credits': 4},
    {'subject': 'EE', 'number': '108', 'title': 'Digital Systems Design', 'credits': 4},
]

# Business courses for Harvard
harvard_business_courses = [
    {'subject': 'ECON', 'number': '10a', 'title': 'Principles of Economics', 'credits': 4},
    {'subject': 'ECON', 'number': '10b', 'title': 'Principles of Economics', 'credits': 4},
    {'subject': 'ECON', 'number': '1010a', 'title': 'Intermediate Microeconomics', 'credits': 4},
    {'subject': 'STAT', 'number': '110', 'title': 'Introduction to Probability', 'credits': 4},
]

# Mechanical Engineering courses for MIT
mit_me_courses = [
    {'subject': 'ME', 'number': '2.001', 'title': 'Mechanics and Materials I', 'credits': 12},
    {'subject': 'ME', 'number': '2.002', 'title': 'Mechanics and Materials II', 'credits': 12},
    {'subject': 'ME', 'number': '2.003', 'title': 'Modeling Dynamics and Control I', 'credits': 12},
    {'subject': 'ME', 'number': '2.004', 'title': 'Modeling Dynamics and Control II', 'credits': 12},
]

print("="*70)
print("ADDING COURSES FOR ALL DEMO USER MAJORS")
print("="*70)

add_courses_for_major('Computer Science', 'UIUC', uiuc_cs_courses)
add_courses_for_major('Computer Science', 'MIT', mit_cs_courses)
add_courses_for_major('Computer Science', 'Stanford', stanford_cs_courses)
add_courses_for_major('Computer Science', 'Harvard', harvard_cs_courses)
add_courses_for_major('Data Science', 'UC Berkeley', berkeley_ds_courses)
add_courses_for_major('Electrical Engineering', 'Stanford', stanford_ee_courses)
add_courses_for_major('Business Administration', 'Harvard', harvard_business_courses)
add_courses_for_major('Mechanical Engineering', 'MIT', mit_me_courses)

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
total_courses = Course.objects.count()
print(f"Total courses in database: {total_courses}")
print("\nCourses by major:")
from collections import defaultdict
courses_by_major = defaultdict(int)
for course in Course.objects.all():
    key = f"{course.major.name} ({course.major.college.abbreviation})"
    courses_by_major[key] += 1

for major, count in sorted(courses_by_major.items()):
    print(f"  {major}: {count} courses")

print("\n✅ Course data updated!")
