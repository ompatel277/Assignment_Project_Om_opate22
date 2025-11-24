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

    def get_skills_list(self):
        """Return skills as a list."""
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def get_interests_list(self):
        """Return interests as a list."""
        if not self.personal_interests:
            return []
        return [i.strip() for i in self.personal_interests.split(',') if i.strip()]


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


# =====================================================
#  PORTFOLIO ITEM MODEL
# =====================================================

class PortfolioItem(models.Model):
    """
    Represents a suggested project, certification, or milestone
    that students can track for career preparation.
    """
    ITEM_TYPES = [
        ('PROJECT', 'Project'),
        ('CERT', 'Certification'),
        ('MILESTONE', 'Milestone'),
        ('INTERNSHIP', 'Internship'),
        ('COMPETITION', 'Competition'),
    ]

    title = models.CharField(max_length=200)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, default='PROJECT')
    description = models.TextField(blank=True)

    # Link to careers that benefit from this item
    related_careers = models.ManyToManyField(
        'careers.Career',
        blank=True,
        related_name='portfolio_items'
    )

    # Skills gained from completing this item
    skills_gained = models.TextField(
        blank=True,
        help_text="Comma-separated list of skills"
    )

    # Estimated time to complete
    estimated_hours = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Estimated hours to complete"
    )

    # Difficulty level
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('BEGINNER', 'Beginner'),
            ('INTERMEDIATE', 'Intermediate'),
            ('ADVANCED', 'Advanced'),
        ],
        default='BEGINNER'
    )

    # External resources
    resource_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['difficulty_level', 'title']
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"

    def __str__(self):
        return f"{self.title} ({self.get_item_type_display()})"

    def get_skills_list(self):
        """Return skills as a list."""
        if not self.skills_gained:
            return []
        return [s.strip() for s in self.skills_gained.split(',') if s.strip()]


# =====================================================
#  USER CHECKLIST MODEL
# =====================================================

class UserChecklist(models.Model):
    """
    Tracks a user's progress on portfolio items.
    Links users to portfolio items with status tracking.
    """
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ABANDONED', 'Abandoned'),
    ]

    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='checklist_items'
    )

    portfolio_item = models.ForeignKey(
        PortfolioItem,
        on_delete=models.CASCADE,
        related_name='user_checklists'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNED'
    )

    # User notes
    notes = models.TextField(blank=True)

    # Progress tracking
    progress_percentage = models.PositiveIntegerField(
        default=0,
        help_text="Percentage complete (0-100)"
    )

    # Timestamps
    added_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Priority level
    priority = models.CharField(
        max_length=10,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High'),
        ],
        default='MEDIUM'
    )

    class Meta:
        ordering = ['-priority', '-added_at']
        unique_together = ('user_profile', 'portfolio_item')
        verbose_name = "User Checklist Item"
        verbose_name_plural = "User Checklist Items"

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.portfolio_item.title} ({self.status})"

    def mark_completed(self):
        """Mark this item as completed and set completion timestamp."""
        from django.utils import timezone
        self.status = 'COMPLETED'
        self.progress_percentage = 100
        self.completed_at = timezone.now()
        self.save()

    def mark_in_progress(self):
        """Mark this item as in progress and set start timestamp."""
        from django.utils import timezone
        if not self.started_at:
            self.started_at = timezone.now()
        self.status = 'IN_PROGRESS'
        self.save()


# =====================================================
#  CAREER PLAN MODEL
# =====================================================

class CareerPlan(models.Model):
    """
    Allows users to create multiple career plans and roadmaps.
    Each plan is focused on a specific career goal.
    """
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='career_plans'
    )

    # Target career for this plan
    target_career = models.ForeignKey(
        'careers.Career',
        on_delete=models.CASCADE,
        related_name='user_plans'
    )

    # Plan details
    name = models.CharField(
        max_length=200,
        help_text="Name for this plan (e.g., 'Plan A: Software Engineer')"
    )

    description = models.TextField(
        blank=True,
        help_text="Why you're interested in this career path"
    )

    # Target timeline
    target_date = models.DateField(
        null=True,
        blank=True,
        help_text="When do you want to achieve this career goal?"
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Is this plan currently active?"
    )

    is_primary = models.BooleanField(
        default=False,
        help_text="Is this your primary career plan?"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_primary', '-is_active', '-created_at']
        verbose_name = "Career Plan"
        verbose_name_plural = "Career Plans"

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.name}"

    def set_as_primary(self):
        """Set this as the primary plan and unset others."""
        CareerPlan.objects.filter(
            user_profile=self.user_profile
        ).update(is_primary=False)
        self.is_primary = True
        self.save()

    def get_recommended_items(self):
        """Get portfolio items recommended for this career path."""
        from recommender.engine import RecommendationEngine
        engine = RecommendationEngine(self.user_profile)
        return engine.get_portfolio_recommendations(limit=10)

    def get_progress_percentage(self):
        """Calculate overall progress towards this career goal."""
        plan_items = self.plan_items.all()
        if not plan_items:
            return 0
        completed = plan_items.filter(status='COMPLETED').count()
        return int((completed / plan_items.count()) * 100)


class PlanItem(models.Model):
    """
    Individual items/milestones within a career plan.
    Can be portfolio items, courses, certifications, etc.
    """
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('SKIPPED', 'Skipped'),
    ]

    career_plan = models.ForeignKey(
        CareerPlan,
        on_delete=models.CASCADE,
        related_name='plan_items'
    )

    # What type of item is this?
    portfolio_item = models.ForeignKey(
        PortfolioItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Portfolio item (project, cert, etc.)"
    )

    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Course to take"
    )

    # Custom milestone (if not a portfolio item or course)
    custom_title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Custom milestone title"
    )

    custom_description = models.TextField(
        blank=True,
        help_text="Custom milestone description"
    )

    # Planning
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNED'
    )

    target_semester = models.CharField(
        max_length=20,
        blank=True,
        help_text="When to complete this (e.g., 'Fall 2025')"
    )

    priority = models.IntegerField(
        default=5,
        help_text="Priority 1-10, higher is more important"
    )

    notes = models.TextField(blank=True)

    # Timestamps
    added_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-priority', 'added_at']
        verbose_name = "Plan Item"
        verbose_name_plural = "Plan Items"

    def __str__(self):
        if self.portfolio_item:
            return f"{self.career_plan.name} - {self.portfolio_item.title}"
        elif self.course:
            return f"{self.career_plan.name} - {self.course.title}"
        else:
            return f"{self.career_plan.name} - {self.custom_title}"

    def get_title(self):
        """Get the display title for this item."""
        if self.portfolio_item:
            return self.portfolio_item.title
        elif self.course:
            return f"{self.course.subject} {self.course.number}: {self.course.title}"
        else:
            return self.custom_title

    def mark_completed(self):
        """Mark this plan item as completed."""
        from django.utils import timezone
        self.status = 'COMPLETED'
        self.completed_at = timezone.now()
        self.save()