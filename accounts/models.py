from django.db import models
from django.contrib.auth.models import AbstractUser
from colleges.models import College, Major


class User(AbstractUser):
    email = models.EmailField("email address", unique=True)
    phone_number = models.CharField(max_length=25, unique=True, blank=True, null=True)

    USERNAME_FIELD = "email"            # login with email
    REQUIRED_FIELDS = ["username"]      # still keep username

    def __str__(self):
        return self.username or self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, blank=True, null=True, related_name="profiles")
    college = models.ForeignKey(College, on_delete=models.CASCADE, blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)

    academic_year = models.CharField(
        max_length=20,
        choices=[
            ('highschool_freshman', 'Highschool Freshman'),
            ('highschool_sophomore', 'Highschool Sophomore'),
            ('highschool_junior', 'Highschool Junior'),
            ('highschool_senior', 'Highschool Senior'),
            ('college_freshman', 'College Freshman'),
            ('college_sophomore', 'College Sophomore'),
            ('college_junior', 'College Junior'),
            ('college_senior', 'College Senior'),
            ('graduate', 'Graduate Student'),
            ('alumni', 'Alumni'),
        ],
        blank=True,
        null=True
    )
    gpa = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2)

    personal_interests = models.JSONField(default=list, blank=True)
    career_goals = models.TextField(blank=True)
    clubs_interest = models.JSONField(default=list, blank=True)
    clubs_user_is_a_part_of = models.JSONField(default=list, blank=True)

    skills = models.JSONField(default=list, blank=True)
    work_experience = models.TextField(blank=True)

    preferred_industries = models.JSONField(default=list, blank=True)
    preferred_locations = models.JSONField(default=list, blank=True)
    preferred_positions = models.JSONField(default=list, blank=True)
    preferred_skills = models.JSONField(default=list, blank=True)
    preferred_title = models.JSONField(default=list, blank=True)
    preferred_company = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
