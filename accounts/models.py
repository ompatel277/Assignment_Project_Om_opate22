# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# =====================================================
#  USER PROFILE MODEL
# =====================================================

class UserProfile(models.Model):
    ACADEMIC_YEARS = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )

    # --- Academic Associations ---
    college = models.ForeignKey(
        "colleges.College",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='students'
    )
    major = models.ForeignKey(
        "colleges.Major",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='major_students'
    )
    minors = models.ManyToManyField(
        "colleges.Major",
        blank=True,
        related_name='minor_students',
        help_text="Optional secondary areas of study."
    )

    gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
        null=True, blank=True,
        help_text="GPA on a 4.0 scale."
    )

    academic_year = models.CharField(
        max_length=2,
        choices=ACADEMIC_YEARS,
        default='FR'
    )

    # --- Personal & Career Information ---
    personal_interests = models.TextField(blank=True)
    career_goals = models.TextField(blank=True)
    clubs_interest = models.TextField(blank=True)
    clubs_user_is_a_part_of = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)

    # --- Preferences ---
    preferred_industries = models.TextField(blank=True)
    preferred_locations = models.TextField(blank=True)
    preferred_positions = models.TextField(blank=True)
    preferred_company = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user__username']
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username} ({self.get_academic_year_display()})"


# =====================================================
#  COURSE MODEL
# =====================================================

class Course(models.Model):
    subject = models.CharField(max_length=20)
    number = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    credits = models.DecimalField(
        max_digits=3, decimal_places=1,
        validators=[MinValueValidator(0.5), MaxValueValidator(10.0)]
    )
    major = models.ForeignKey(
        "colleges.Major",
        on_delete=models.CASCADE,
        related_name="recommended_courses"
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject} {self.number} – {self.title}"


# =====================================================
#  CLUB MODEL
# =====================================================

class Club(models.Model):
    name = models.CharField(max_length=150)
    category = models.CharField(
        max_length=100, blank=True,
        help_text="e.g. Academic, Sports, Cultural, Tech, etc."
    )
    college = models.ForeignKey(
        "colleges.College",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="clubs"
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# =====================================================
#  CAREER PATH MODEL
# =====================================================

class CareerPath(models.Model):
    title = models.CharField(max_length=200)
    related_major = models.ForeignKey(
        "colleges.Major",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="career_paths"
    )
    salary_range = models.CharField(
        max_length=100, blank=True,
        help_text="Example: $60k–$90k/year"
    )
    relevant_skills = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
