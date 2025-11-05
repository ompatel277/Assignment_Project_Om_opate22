"""
Management command to seed the database with sample data for Traject.
Usage: python manage.py seed_data
       python manage.py seed_data --clear  (to clear existing data first)
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from colleges.models import College, Major
from careers.models import Career
from accounts.models import UserProfile, Club, CareerPath, PortfolioItem, UserChecklist, Course
from catalog.models import Course as CatalogCourse, DegreeCategory, DegreeRequirement


class Command(BaseCommand):
    help = 'Seeds the database with sample colleges, majors, courses, careers, and portfolio items'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding (keeps superusers)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('⚠️  Clearing existing data...'))
            self.clear_data()

        self.stdout.write(self.style.SUCCESS('🌱 Starting data seeding...'))

        # Seed in order of dependencies
        colleges = self.seed_colleges()
        majors = self.seed_majors(colleges)
        courses = self.seed_courses(colleges, majors)
        careers = self.seed_careers()
        portfolio_items = self.seed_portfolio_items(careers)
        clubs = self.seed_clubs(colleges)
        users = self.seed_users(colleges, majors)
        self.seed_user_checklists(users, portfolio_items)

        self.stdout.write(self.style.SUCCESS('\n✅ Data seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now login with:'))
        self.stdout.write(self.style.SUCCESS('  Username: alice_cs | Password: testpass123'))
        self.stdout.write(self.style.SUCCESS('  Username: bob_data | Password: testpass123'))
        self.stdout.write(self.style.SUCCESS('  Username: charlie_ml | Password: testpass123'))

    def clear_data(self):
        """Clear existing data (excluding superusers)."""
        UserChecklist.objects.all().delete()
        PortfolioItem.objects.all().delete()
        Club.objects.all().delete()
        CareerPath.objects.all().delete()
        Course.objects.all().delete()
        Major.objects.all().delete()
        College.objects.all().delete()
        Career.objects.all().delete()
        CatalogCourse.objects.all().delete()

        # Delete non-superuser test users
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.SUCCESS('  ✓ Cleared existing data'))

    def seed_colleges(self):
        """Create sample colleges."""
        self.stdout.write('\n📚 Seeding colleges...')

        colleges_data = [
            {
                'college_name': 'University of Illinois Urbana-Champaign',
                'abbreviation': 'UIUC',
                'city': 'Urbana',
                'state': 'Illinois',
                'logo_url': 'https://illinois.edu/assets/img/brand/Illinois-logo.png'
            },
            {
                'college_name': 'Massachusetts Institute of Technology',
                'abbreviation': 'MIT',
                'city': 'Cambridge',
                'state': 'Massachusetts',
                'logo_url': ''
            },
            {
                'college_name': 'Stanford University',
                'abbreviation': 'Stanford',
                'city': 'Stanford',
                'state': 'California',
                'logo_url': ''
            },
            {
                'college_name': 'University of California, Berkeley',
                'abbreviation': 'UC Berkeley',
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
        ]

        colleges = []
        for data in colleges_data:
            college, created = College.objects.get_or_create(
                abbreviation=data['abbreviation'],
                defaults=data
            )
            colleges.append(college)
            if created:
                self.stdout.write(f'  ✓ Created {college.abbreviation}')
            else:
                self.stdout.write(f'  → {college.abbreviation} already exists')

        return colleges

    def seed_majors(self, colleges):
        """Create sample majors for each college."""
        self.stdout.write('\n🎓 Seeding majors...')

        majors_data = [
            {'name': 'Computer Science', 'code': 'CS'},
            {'name': 'Electrical Engineering', 'code': 'ECE'},
            {'name': 'Mechanical Engineering', 'code': 'ME'},
            {'name': 'Business Administration', 'code': 'BUS'},
            {'name': 'Mathematics', 'code': 'MATH'},
            {'name': 'Psychology', 'code': 'PSYCH'},
            {'name': 'Data Science', 'code': 'DS'},
            {'name': 'Information Science', 'code': 'IS'},
        ]

        majors = []
        for college in colleges[:3]:  # Apply to first 3 colleges
            for major_data in majors_data:
                major, created = Major.objects.get_or_create(
                    college=college,
                    name=major_data['name'],
                    defaults={'code': major_data['code']}
                )
                majors.append(major)
                if created:
                    self.stdout.write(f'  ✓ Created {major.name} at {college.abbreviation}')

        return majors

    def seed_courses(self, colleges, majors):
        """Create sample courses."""
        self.stdout.write('\n📖 Seeding courses...')

        # Get CS major from UIUC
        cs_major = majors[0] if majors else None

        courses_data = [
            {'subject': 'CS', 'number': '125', 'title': 'Introduction to Computer Science', 'credits': 4.0},
            {'subject': 'CS', 'number': '173', 'title': 'Discrete Structures', 'credits': 3.0},
            {'subject': 'CS', 'number': '225', 'title': 'Data Structures', 'credits': 4.0},
            {'subject': 'CS', 'number': '233', 'title': 'Computer Architecture', 'credits': 4.0},
            {'subject': 'CS', 'number': '340', 'title': 'Introduction to Computer Systems', 'credits': 3.0},
            {'subject': 'CS', 'number': '374', 'title': 'Algorithms & Models of Computation', 'credits': 4.0},
            {'subject': 'CS', 'number': '411', 'title': 'Database Systems', 'credits': 3.0},
            {'subject': 'CS', 'number': '421', 'title': 'Programming Languages & Compilers', 'credits': 3.0},
            {'subject': 'CS', 'number': '440', 'title': 'Artificial Intelligence', 'credits': 3.0},
            {'subject': 'MATH', 'number': '220', 'title': 'Calculus I', 'credits': 5.0},
            {'subject': 'MATH', 'number': '221', 'title': 'Calculus II', 'credits': 5.0},
            {'subject': 'MATH', 'number': '241', 'title': 'Calculus III', 'credits': 4.0},
            {'subject': 'MATH', 'number': '415', 'title': 'Linear Algebra', 'credits': 3.0},
            {'subject': 'STAT', 'number': '400', 'title': 'Statistics & Probability', 'credits': 4.0},
        ]

        courses = []
        if cs_major:
            for course_data in courses_data:
                course, created = Course.objects.get_or_create(
                    major=cs_major,
                    subject=course_data['subject'],
                    number=course_data['number'],
                    defaults={
                        'title': course_data['title'],
                        'credits': course_data['credits'],
                        'description': f'Core course for {cs_major.name}'
                    }
                )
                courses.append(course)
                if created:
                    self.stdout.write(f'  ✓ Created {course.subject} {course.number}')

        return courses

    def seed_careers(self):
        """Create sample career paths."""
        self.stdout.write('\n💼 Seeding careers...')

        careers_data = [
            {
                'title': 'Software Engineer',
                'company': 'Various Tech Companies',
                'industries': ['Technology', 'Software', 'SaaS'],
                'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'Git'],
                'description': 'Design, develop, and maintain software applications. Work on frontend, backend, or full-stack development.'
            },
            {
                'title': 'Data Scientist',
                'company': 'Various Companies',
                'industries': ['Technology', 'Finance', 'Healthcare'],
                'skills': ['Python', 'R', 'Machine Learning', 'Statistics', 'SQL', 'Tableau'],
                'description': 'Analyze complex data sets to extract insights and build predictive models.'
            },
            {
                'title': 'Machine Learning Engineer',
                'company': 'AI/ML Companies',
                'industries': ['AI', 'Technology', 'Research'],
                'skills': ['Python', 'TensorFlow', 'PyTorch', 'Deep Learning', 'NLP', 'Computer Vision'],
                'description': 'Build and deploy machine learning models at scale.'
            },
            {
                'title': 'Product Manager',
                'company': 'Tech Companies',
                'industries': ['Technology', 'Product', 'SaaS'],
                'skills': ['Product Strategy', 'User Research', 'Agile', 'SQL', 'Communication', 'Roadmapping'],
                'description': 'Define product vision, strategy, and roadmap. Work with engineering, design, and stakeholders.'
            },
            {
                'title': 'UX/UI Designer',
                'company': 'Design Studios / Tech',
                'industries': ['Design', 'Technology', 'Consulting'],
                'skills': ['Figma', 'Sketch', 'User Research', 'Prototyping', 'Visual Design', 'HTML/CSS'],
                'description': 'Create user-centered designs and interfaces for digital products.'
            },
            {
                'title': 'DevOps Engineer',
                'company': 'Cloud/Tech Companies',
                'industries': ['Technology', 'Cloud', 'Infrastructure'],
                'skills': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Linux', 'Terraform'],
                'description': 'Manage infrastructure, automate deployments, and ensure system reliability.'
            },
            {
                'title': 'Cybersecurity Analyst',
                'company': 'Security Firms',
                'industries': ['Security', 'Technology', 'Finance'],
                'skills': ['Network Security', 'Penetration Testing', 'SIEM', 'Python', 'Cryptography'],
                'description': 'Protect organizations from cyber threats and security breaches.'
            },
        ]

        careers = []
        for data in careers_data:
            career, created = Career.objects.get_or_create(
                title=data['title'],
                defaults={
                    'company': data['company'],
                    'industries': data['industries'],
                    'skills': data['skills'],
                    'description': data['description']
                }
            )
            careers.append(career)
            if created:
                self.stdout.write(f'  ✓ Created {career.title}')

        return careers

    def seed_portfolio_items(self, careers):
        """Create sample portfolio items."""
        self.stdout.write('\n📁 Seeding portfolio items...')

        items_data = [
            {
                'title': 'Build a Personal Portfolio Website',
                'item_type': 'PROJECT',
                'description': 'Create a responsive portfolio website showcasing your projects, skills, and experience.',
                'skills_gained': 'HTML, CSS, JavaScript, Responsive Design, Git',
                'estimated_hours': 20,
                'difficulty_level': 'BEGINNER',
                'resource_url': 'https://www.freecodecamp.org/'
            },
            {
                'title': 'AWS Certified Solutions Architect',
                'item_type': 'CERT',
                'description': 'Industry-recognized certification for cloud architecture and AWS services.',
                'skills_gained': 'AWS, Cloud Architecture, S3, EC2, Lambda',
                'estimated_hours': 80,
                'difficulty_level': 'INTERMEDIATE',
                'resource_url': 'https://aws.amazon.com/certification/'
            },
            {
                'title': 'Complete a Machine Learning Project',
                'item_type': 'PROJECT',
                'description': 'Build an end-to-end ML project with data collection, model training, and deployment.',
                'skills_gained': 'Python, Scikit-learn, TensorFlow, Data Analysis, Model Deployment',
                'estimated_hours': 40,
                'difficulty_level': 'INTERMEDIATE',
                'resource_url': ''
            },
            {
                'title': 'Contribute to Open Source',
                'item_type': 'MILESTONE',
                'description': 'Make meaningful contributions to open-source projects on GitHub.',
                'skills_gained': 'Git, Collaboration, Code Review, Documentation',
                'estimated_hours': 10,
                'difficulty_level': 'BEGINNER',
                'resource_url': 'https://github.com/'
            },
            {
                'title': 'Google Data Analytics Professional Certificate',
                'item_type': 'CERT',
                'description': 'Learn data analysis skills with SQL, R, and Tableau.',
                'skills_gained': 'SQL, R, Data Visualization, Tableau, Statistics',
                'estimated_hours': 120,
                'difficulty_level': 'BEGINNER',
                'resource_url': 'https://www.coursera.org/google-certificates/data-analytics-certificate'
            },
            {
                'title': 'Build a Full-Stack Web Application',
                'item_type': 'PROJECT',
                'description': 'Create a complete web app with frontend, backend, database, and deployment.',
                'skills_gained': 'React, Node.js, Express, PostgreSQL, REST APIs, Deployment',
                'estimated_hours': 60,
                'difficulty_level': 'ADVANCED',
                'resource_url': ''
            },
            {
                'title': 'Participate in a Hackathon',
                'item_type': 'COMPETITION',
                'description': 'Join a hackathon to build projects under time constraints and network with peers.',
                'skills_gained': 'Rapid Prototyping, Teamwork, Presentation, Problem Solving',
                'estimated_hours': 24,
                'difficulty_level': 'INTERMEDIATE',
                'resource_url': 'https://mlh.io/'
            },
            {
                'title': 'Complete a Software Engineering Internship',
                'item_type': 'INTERNSHIP',
                'description': 'Gain real-world experience working on production codebases.',
                'skills_gained': 'Professional Development, Code Review, Agile, Real-world Projects',
                'estimated_hours': 400,
                'difficulty_level': 'INTERMEDIATE',
                'resource_url': ''
            },
        ]

        portfolio_items = []
        for data in items_data:
            item, created = PortfolioItem.objects.get_or_create(
                title=data['title'],
                defaults={
                    'item_type': data['item_type'],
                    'description': data['description'],
                    'skills_gained': data['skills_gained'],
                    'estimated_hours': data['estimated_hours'],
                    'difficulty_level': data['difficulty_level'],
                    'resource_url': data['resource_url']
                }
            )
            portfolio_items.append(item)

            # Link to relevant careers
            if 'Software' in item.title or 'Web' in item.title or 'Full-Stack' in item.title:
                item.related_careers.add(*[c for c in careers if 'Software' in c.title or 'DevOps' in c.title])
            if 'Data' in item.title or 'Machine Learning' in item.title:
                item.related_careers.add(*[c for c in careers if 'Data' in c.title or 'Machine Learning' in c.title])

            if created:
                self.stdout.write(f'  ✓ Created {item.title}')

        return portfolio_items

    def seed_clubs(self, colleges):
        """Create sample clubs."""
        self.stdout.write('\n🏫 Seeding clubs...')

        clubs_data = [
            {'name': 'ACM (Association for Computing Machinery)', 'category': 'Tech'},
            {'name': 'Women in Computer Science', 'category': 'Tech'},
            {'name': 'Robotics Club', 'category': 'Engineering'},
            {'name': 'Data Science Club', 'category': 'Tech'},
            {'name': 'Entrepreneurship Club', 'category': 'Business'},
            {'name': 'Debate Team', 'category': 'Academic'},
            {'name': 'Chess Club', 'category': 'Recreation'},
        ]

        clubs = []
        for college in colleges[:2]:  # Add to first 2 colleges
            for club_data in clubs_data:
                club, created = Club.objects.get_or_create(
                    name=club_data['name'],
                    college=college,
                    defaults={
                        'category': club_data['category'],
                        'description': f'Student organization at {college.abbreviation}'
                    }
                )
                clubs.append(club)
                if created:
                    self.stdout.write(f'  ✓ Created {club.name} at {college.abbreviation}')

        return clubs

    def seed_users(self, colleges, majors):
        """Create sample users with profiles."""
        self.stdout.write('\n👥 Seeding users...')

        users_data = [
            {
                'username': 'alice_cs',
                'email': 'alice@example.com',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'password': 'testpass123',
                'profile': {
                    'college': colleges[0] if colleges else None,
                    'major': majors[0] if majors else None,
                    'academic_year': 'JR',
                    'gpa': 3.75,
                    'skills': 'Python, Java, React, SQL, Git',
                    'personal_interests': 'Web Development, AI, Open Source',
                    'career_goals': 'Software Engineer at a top tech company',
                }
            },
            {
                'username': 'bob_data',
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Smith',
                'password': 'testpass123',
                'profile': {
                    'college': colleges[0] if colleges else None,
                    'major': majors[6] if len(majors) > 6 else majors[0],  # Data Science
                    'academic_year': 'SO',
                    'gpa': 3.50,
                    'skills': 'Python, R, SQL, Pandas, Matplotlib',
                    'personal_interests': 'Data Analysis, Statistics, Visualization',
                    'career_goals': 'Data Scientist in healthcare or finance',
                }
            },
            {
                'username': 'charlie_ml',
                'email': 'charlie@example.com',
                'first_name': 'Charlie',
                'last_name': 'Brown',
                'password': 'testpass123',
                'profile': {
                    'college': colleges[1] if len(colleges) > 1 else colleges[0],
                    'major': majors[0] if majors else None,
                    'academic_year': 'SR',
                    'gpa': 3.90,
                    'skills': 'Python, TensorFlow, PyTorch, C++, CUDA',
                    'personal_interests': 'Machine Learning, Computer Vision, Research',
                    'career_goals': 'Machine Learning Researcher or ML Engineer',
                }
            },
        ]

        users = []
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
                self.stdout.write(f'  ✓ Created user {user.username}')

            # Create or update profile
            profile, p_created = UserProfile.objects.get_or_create(
                user=user,
                defaults=data['profile']
            )
            users.append((user, profile))

        return users

    def seed_user_checklists(self, users, portfolio_items):
        """Create sample checklist items for users."""
        self.stdout.write('\n✅ Seeding user checklists...')

        if not users or not portfolio_items:
            return

        # Alice's checklist (Junior, focused on web dev)
        alice_profile = users[0][1]
        alice_items = [
            (portfolio_items[0], 'COMPLETED', 100),  # Portfolio website
            (portfolio_items[3], 'COMPLETED', 100),  # Open source
            (portfolio_items[5], 'IN_PROGRESS', 60),  # Full-stack app
            (portfolio_items[6], 'PLANNED', 0),  # Hackathon
        ]

        for item, status, progress in alice_items:
            checklist, created = UserChecklist.objects.get_or_create(
                user_profile=alice_profile,
                portfolio_item=item,
                defaults={
                    'status': status,
                    'progress_percentage': progress,
                    'priority': 'HIGH' if status == 'IN_PROGRESS' else 'MEDIUM'
                }
            )
            if created:
                self.stdout.write(f'  ✓ Added checklist item for alice_cs')

        # Bob's checklist (Sophomore, focused on data science)
        if len(users) > 1:
            bob_profile = users[1][1]
            bob_items = [
                (portfolio_items[4], 'IN_PROGRESS', 40),  # Google Data Analytics
                (portfolio_items[2], 'PLANNED', 0),  # ML project
            ]

            for item, status, progress in bob_items:
                checklist, created = UserChecklist.objects.get_or_create(
                    user_profile=bob_profile,
                    portfolio_item=item,
                    defaults={
                        'status': status,
                        'progress_percentage': progress,
                        'priority': 'HIGH'
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Added checklist item for bob_data')

        self.stdout.write(self.style.SUCCESS('  User checklists seeded'))