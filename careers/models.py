from django.db import models

class Career(models.Model):
    position = models.CharField(max_length=100)
   #skill_sets = ###
    title = models.CharField(max_length=100)
    industries = models.CharField(max_length=100)
    description = models.TextField()
    company = models.CharField(max_length=100)