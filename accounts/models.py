from django.db import models
from django.contrib.auth.models import User


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=100, blank=True)
    college= models.CharField(max_length=100, blank=True)
    personal_interest = models.CharField(max_length=100, blank=True)
    clubs_joined = models.DateField(null=True, blank=True)
    career_interests = models.CharField(max_length=100, blank=True)
    grade_user_is_in = models.CharField(max_length=100, blank=True)


