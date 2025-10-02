from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    ACADEMIC_YEARS = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    ]

    # Link to Django's built-in user
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # College & Major (from colleges app)
    college = models.ForeignKey(
        "colleges.College",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
    )
    major = models.ForeignKey(
        "colleges.Major",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
    )

    # GPA
    gpa = models.DecimalField(
        max_digits=4,  # allows values like 4.00 safely
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
        null=True,
        blank=True
    )

    academic_year = models.CharField(
        max_length=2,
        choices=ACADEMIC_YEARS,
        default='FR',
    )

    # Profile details
    personal_interests = models.JSONField(default=list, blank=True)
    career_goals = models.TextField(blank=True)
    clubs_interest = models.JSONField(default=list, blank=True)
    clubs_user_is_a_part_of = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    work_experience = models.TextField(blank=True)

    # Preferences
    preferred_industries = models.JSONField(default=list, blank=True)
    preferred_locations = models.JSONField(default=list, blank=True)
    preferred_positions = models.JSONField(default=list, blank=True)
    preferred_skills = models.JSONField(default=list, blank=True)
    preferred_title = models.JSONField(default=list, blank=True)
    preferred_company = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'major'], name="unique_user_major"),
            models.CheckConstraint(
                check=models.Q(gpa__gte=0.0) & models.Q(gpa__lte=4.0),
                name="gpa_range"
            ),
        ]
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} ({self.get_academic_year_display()})"
