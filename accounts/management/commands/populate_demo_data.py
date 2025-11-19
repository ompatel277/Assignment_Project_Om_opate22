from django.core.management.base import BaseCommand
from colleges.models import College, Major
from accounts.models import Course, Club, PortfolioItem, UserProfile
from careers.models import Career
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Populate database with demo data for Traject'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data population...')

        # Create data
        self.create_colleges()
        self.create_majors()
        self.create_courses()
        self.create_careers()
        self.create_clubs()
        self.create_portfolio_items()
        self.create_demo_users()

        self.stdout.write(self.style.SUCCESS('Successfully populated demo data!'))

    def create_colleges(self):
        """Create sample colleges"""
        colleges_data = [
            {
                'college_name': 'Massachusetts Institute of Technology',
                'abbreviation': 'MIT',
                'city': 'Cambridge',
                'state': 'Massachusetts',
                'logo_url': ''
            },
            {
                'college_name': 'Stanford University',
                'abbreviation': 'STANFORD',
                'city': 'Stanford',
                'state': 'California',
                'logo_url': ''
            },
            {
                'college_name': 'University of California, Berkeley',
                'abbreviation': 'BERKELEY',
                'city': 'Berkeley',
                'state': 'California',
                'logo_url': ''
            },
            {
                'college_name': 'Carnegie Mellon University',
                'abbreviation': 'CMU',
                'city': 'Pittsburgh',
                'state': 'Pennsylvania',
                'logo_url': ''
            },
            {
                'college_name': 'University of Illinois Urbana-Champaign',
                'abbreviation': 'UIUC',
                'city': 'Urbana',
                'state': 'Illinois',
                'logo_url': ''
            },
        ]

        for data in colleges_data:
            college, created = College.objects.get_or_create(
                abbreviation=data['abbreviation'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  Created college: {college.college_name}')

    def create_majors(self):
        """Create sample majors for each college"""
        majors_data = [
            ('CS', 'Computer Science'),
            ('DS', 'Data Science'),
            ('EE', 'Electrical Engineering'),
            ('ME', 'Mechanical Engineering'),
            ('BA', 'Business Administration'),
            ('MATH', 'Mathematics'),
            ('PHYS', 'Physics'),
            ('BIO', 'Biology'),
        ]

        colleges = College.objects.all()
        for college in colleges:
            for code, name in majors_data:
                major, created = Major.objects.get_or_create(
                    college=college,
                    name=name,
                    defaults={'code': code}
                )
                if created:
                    self.stdout.write(f'  Created major: {name} at {college.abbreviation}')

    def create_courses(self):
        """Create sample courses"""
        # Get a CS major to link courses to
        cs_major = Major.objects.filter(name='Computer Science').first()
        math_major = Major.objects.filter(name='Mathematics').first()
        ee_major = Major.objects.filter(name='Electrical Engineering').first()

        if not cs_major or not math_major or not ee_major:
            self.stdout.write(self.style.WARNING('  Skipping courses - majors not found'))
            return

        courses_data = [
            {
                'subject': 'CS',
                'number': '101',
                'title': 'Introduction to Computer Science',
                'credits': 3,
                'description': 'Fundamental programming concepts',
                'major': cs_major
            },
            {
                'subject': 'CS',
                'number': '225',
                'title': 'Data Structures',
                'credits': 4,
                'description': 'Arrays, lists, trees, graphs',
                'major': cs_major
            },
            {
                'subject': 'CS',
                'number': '233',
                'title': 'Computer Architecture',
                'credits': 4,
                'description': 'Digital logic, processors, memory',
                'major': cs_major
            },
            {
                'subject': 'CS',
                'number': '374',
                'title': 'Algorithms',
                'credits': 4,
                'description': 'Design and analysis of algorithms',
                'major': cs_major
            },
            {
                'subject': 'MATH',
                'number': '221',
                'title': 'Calculus I',
                'credits': 4,
                'description': 'Limits, derivatives, integration',
                'major': math_major
            },
            {
                'subject': 'MATH',
                'number': '231',
                'title': 'Calculus II',
                'credits': 3,
                'description': 'Advanced integration techniques',
                'major': math_major
            },
            {
                'subject': 'EE',
                'number': '120',
                'title': 'Signals and Systems',
                'credits': 4,
                'description': 'Signal processing fundamentals',
                'major': ee_major
            },
        ]

        for data in courses_data:
            course, created = Course.objects.get_or_create(
                subject=data['subject'],
                number=data['number'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  Created course: {course.subject} {course.number}')

    def create_careers(self):
        """Create sample careers"""
        careers_data = [
            {
                'title': 'Software Engineer',
                'company': 'Tech Companies',
                'description': 'Design and develop software applications',
                'skills': ['Python', 'Java', 'Git', 'Algorithms', 'Data Structures'],
                'industries': ['Technology', 'Finance', 'Healthcare']
            },
            {
                'title': 'Data Scientist',
                'company': 'Various Industries',
                'description': 'Analyze data and build predictive models',
                'skills': ['Python', 'R', 'Machine Learning', 'Statistics', 'SQL'],
                'industries': ['Technology', 'Finance', 'E-commerce']
            },
            {
                'title': 'Product Manager',
                'company': 'Tech Companies',
                'description': 'Define product strategy and roadmap',
                'skills': ['Communication', 'Strategy', 'Data Analysis', 'User Research'],
                'industries': ['Technology', 'Consumer Goods']
            },
            {
                'title': 'UX Designer',
                'company': 'Design Studios',
                'description': 'Create user-centered digital experiences',
                'skills': ['Figma', 'User Research', 'Prototyping', 'Visual Design'],
                'industries': ['Technology', 'Design', 'Advertising']
            },
            {
                'title': 'Machine Learning Engineer',
                'company': 'AI Companies',
                'description': 'Build and deploy ML models at scale',
                'skills': ['Python', 'TensorFlow', 'PyTorch', 'Deep Learning', 'MLOps'],
                'industries': ['Technology', 'Research', 'Autonomous Vehicles']
            },
        ]

        for data in careers_data:
            career, created = Career.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  Created career: {career.title}')

    def create_clubs(self):
        """Create sample clubs"""
        club_categories = [
            ('Academic', 'ACM Student Chapter'),
            ('Academic', 'Data Science Club'),
            ('Tech', 'Robotics Team'),
            ('Cultural', 'International Students Association'),
            ('Sports', 'Intramural Sports'),
        ]

        colleges = College.objects.all()
        for college in colleges:
            for category, name in club_categories:
                club_name = f"{college.abbreviation} {name}"
                club, created = Club.objects.get_or_create(
                    name=club_name,
                    college=college,
                    defaults={
                        'category': category,
                        'description': f'{name} at {college.college_name}'
                    }
                )
                if created:
                    self.stdout.write(f'  Created club: {club_name}')

    def create_portfolio_items(self):
        """Create sample portfolio items"""
        portfolio_data = [
            {
                'title': 'Build a Full-Stack Web App',
                'item_type': 'PROJECT',
                'description': 'Create a complete web application with frontend and backend',
                'skills_gained': 'React, Node.js, MongoDB, REST APIs',
                'estimated_hours': 40,
                'difficulty_level': 'INTERMEDIATE',
                'resource_url': 'https://www.freecodecamp.org'
            },
            {
                'title': 'AWS Certified Solutions Architect',
                'item_type': 'CERT',
                'description': 'Industry-recognized cloud computing certification',
                'skills_gained': 'AWS, Cloud Architecture, DevOps',
                'estimated_hours': 80,
                'difficulty_level': 'ADVANCED',
                'resource_url': 'https://aws.amazon.com/certification/'
            },
            {
                'title': 'Contribute to Open Source',
                'item_type': 'MILESTONE',
                'description': 'Make your first open source contribution',
                'skills_gained': 'Git, GitHub, Collaboration',
                'estimated_hours': 10,
                'difficulty_level': 'BEGINNER',
                'resource_url': 'https://github.com'
            },
            {
                'title': 'Data Science Internship',
                'item_type': 'INTERNSHIP',
                'description': 'Summer internship at a tech company',
                'skills_gained': 'Python, Data Analysis, Machine Learning',
                'estimated_hours': 480,
                'difficulty_level': 'INTERMEDIATE',
                'resource_url': ''
            },
            {
                'title': 'Hackathon Participation',
                'item_type': 'COMPETITION',
                'description': 'Compete in a 24-hour hackathon',
                'skills_gained': 'Rapid Prototyping, Teamwork, Presentation',
                'estimated_hours': 24,
                'difficulty_level': 'INTERMEDIATE',
                'resource_url': 'https://mlh.io'
            },
            {
                'title': 'Machine Learning Portfolio Project',
                'item_type': 'PROJECT',
                'description': 'Build and deploy an ML model',
                'skills_gained': 'Python, TensorFlow, Model Deployment',
                'estimated_hours': 60,
                'difficulty_level': 'ADVANCED',
                'resource_url': ''
            },
        ]

        # Get some careers to link
        careers = list(Career.objects.all()[:3])

        for data in portfolio_data:
            item, created = PortfolioItem.objects.get_or_create(
                title=data['title'],
                defaults={
                    'item_type': data['item_type'],
                    'description': data['description'],
                    'skills_gained': data['skills_gained'],
                    'estimated_hours': data['estimated_hours'],
                    'difficulty_level': data['difficulty_level'],
                    'resource_url': data['resource_url'],
                }
            )
            if created:
                # Link to some careers
                if careers:
                    item.related_careers.set(careers[:2])
                self.stdout.write(f'  Created portfolio item: {item.title}')

    def create_demo_users(self):
        """Create demo users with profiles"""
        users_data = [
            {
                'username': 'demo_student',
                'email': 'demo@traject.edu',
                'password': 'demo123',
                'first_name': 'Demo',
                'last_name': 'Student',
                'abbreviation': 'UIUC',
                'major_name': 'Computer Science'
            },
            {
                'username': 'alice_cs',
                'email': 'alice@traject.edu',
                'password': 'alice123',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'abbreviation': 'MIT',
                'major_name': 'Data Science'
            },
        ]

        for data in users_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name']
                }
            )

            if created:
                user.set_password(data['password'])
                user.save()

                # Create profile
                college = College.objects.get(abbreviation=data['abbreviation'])
                major = Major.objects.get(college=college, name=data['major_name'])

                profile, _ = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'college': college,
                        'major': major,
                        'academic_year': 'Junior'
                    }
                )

                self.stdout.write(f'  Created user: {user.username}')