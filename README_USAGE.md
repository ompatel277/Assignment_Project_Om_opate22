# Traject - Student Career Pathway Platform

A comprehensive Django web application for students to explore colleges, majors, careers, and plan their academic journey with AI-powered recommendations.

## Features

- **College & Major Explorer**: Browse and search 7+ colleges with 56+ majors
- **Career Recommendations**: AI-powered career matching based on skills and interests
- **Portfolio Tracking**: Track projects, certifications, internships, and milestones
- **Roadmap Generator**: Semester-by-semester academic and career planning
- **Data Visualization**: Charts and analytics for user insights
- **Export Functionality**: CSV and JSON export for courses and colleges
- **RESTful API**: JSON endpoints for integration

## Quick Start

### Prerequisites
- Python 3.11+
- pip package manager

### Installation

1. **Clone the repository**
```bash
cd Assignment_Project_Om_opate22
```

2. **Install dependencies**
```bash
pip install -r Assignment_Project_Om_opate22/requirements.txt
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Populate demo data**
```bash
python manage.py populate_demo_data
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Main site: http://127.0.0.1:8000
- Admin panel: http://127.0.0.1:8000/admin

## Demo Account

**Username**: demo_student
**Password**: demo123

## Application Structure

```
├── accounts/          # User profiles, authentication, portfolio
├── colleges/          # College and major management
├── careers/           # Career exploration and recommendations
├── catalog/           # Course catalog
├── recommender/       # AI recommendation engine and roadmap
├── templates/         # HTML templates
├── static/            # CSS, JavaScript, images
└── db.sqlite3         # SQLite database
```

## Key Features by App

### Accounts
- User signup/login with authentication
- Profile management (skills, interests, goals)
- Portfolio checklist with progress tracking
- Data export (CSV/JSON)
- Analytics charts

### Colleges
- Browse 7 universities (MIT, Stanford, CMU, etc.)
- 56+ majors across disciplines
- Search and filter functionality
- Matplotlib charts

### Careers
- 5 career paths with detailed information
- Skill-based recommendations
- Company and industry information

### Recommender
- AI-powered career matching (70%+ match scoring)
- Course recommendations by major
- Club recommendations by college
- 8-semester roadmap generation
- Portfolio item suggestions

## API Endpoints

- `GET /accounts/api/users/` - List all users
- `GET /accounts/api/colleges/users/` - Users per college
- `GET /accounts/export/courses.csv` - Export courses as CSV
- `GET /accounts/export/colleges.json` - Export colleges as JSON

## Technology Stack

- **Backend**: Django 5.2.6, Python 3.11
- **Database**: SQLite3
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Charts**: Matplotlib 3.9.2
- **API**: Django REST Framework 3.16.1

## Development

### Running Tests
```bash
python manage.py check
python manage.py test
```

### Accessing Admin Panel
1. Create superuser: `python manage.py createsuperuser`
2. Visit: http://127.0.0.1:8000/admin
3. Login with superuser credentials

## Production Deployment

Configure environment variables:
```bash
export DJANGO_SECRET_KEY=your-secret-key
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS=yourdomain.com
```

See `.env.example` for full configuration options.

## License

Academic project for educational purposes.

## Authors

Developed as part of CS course assignment.
