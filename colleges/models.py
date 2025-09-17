from django.db import models

# create the class name College and the column names
class College(models.Model):
    college_name = models.CharField(max_length=300) # full college name
    city = models.CharField(max_length=100) # full city name
    state = models.CharField(max_length=100) # full state name
    abbreviation = models.CharField(max_length=50, unique=True) # ex: UIUC
    logo_url = models.URLField(blank = True, null = True) # logo of college

