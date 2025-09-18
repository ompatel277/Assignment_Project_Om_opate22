from django.db import models
from colleges.models import College, Major

# main login/ sign up page
class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return f"{self.username}"



# user profile like
class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # user major and college info
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, blank=True, null=True, related_name="profiles")
    college = models.ForeignKey(College, on_delete=models.CASCADE, blank=True, null=True, max_length=100)
    graduation_year = models.IntegerField(blank=True, null=True)

    # user personal info for school
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
    gpa = models.DecimalField(blank=True, null=True, max_digits = 3, decimal_places = 2)

    # User interests and goals
    personal_interests = models.JSONField(default=list, blank=True, help_text="List of your personal interests")
    career_goals = models.TextField(blank=True, help_text="What are your career aspirations?")
    clubs_interest = models.JSONField(default=list, blank=True, help_text="List of your clubs you want to join")
    clubs_user_is_a_part_of = models.JSONField(default=list, blank=True, help_text="List of your clubs you are a part of or were a part of")

    # User skills and experience
    skills = models.JSONField(default=list, blank=True, help_text="Your current skills")
    work_experience = models.TextField(blank=True, help_text="Brief description of work experience")

    # User preferences
    preferred_industries = models.JSONField(default=list, blank=True)
    preferred_locations = models.JSONField(default=list, blank=True)
    preferred_positions = models.JSONField(default=list, blank=True)
    preferred_skills = models.JSONField(default=list, blank=True)
    preferred_title = models.JSONField(default=list, blank=True)
    preferred_company = models.JSONField(default=list, blank=True)





