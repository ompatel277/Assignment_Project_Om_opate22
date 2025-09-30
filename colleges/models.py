from django.db import models

# create the class name College and the column names
class College(models.Model):
    college_name = models.CharField(max_length=300) # full college name
    city = models.CharField(max_length=100) # full city name
    state = models.CharField(max_length=100) # full state name
    abbreviation = models.CharField(max_length=50, unique=True) # ex: UIUC
    logo_url = models.URLField(blank = True, null = True) # logo of college

    def __str__(self):
        return self.college_name or self.abbreviation

class Major(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="majors")
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, blank=True)  # optional, e.g., "CS"

# from chatGPT will change once I get more information about this
    class Meta:
        unique_together = ("college", "name")
        ordering = ["college__abbreviation", "name"]

    def __str__(self):
        return f"{self.name} ({self.college.abbreviation})"
from django.db import models

# create the class name College and the column names
class College(models.Model):
    college_name = models.CharField(max_length=300) # full college name
    city = models.CharField(max_length=100) # full city name
    state = models.CharField(max_length=100) # full state name
    abbreviation = models.CharField(max_length=50, unique=True) # ex: UIUC
    logo_url = models.URLField(blank = True, null = True) # logo of college

    def __str__(self):
        return self.college_name or self.abbreviation

class Major(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="majors")
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, blank=True)  # optional, e.g., "CS"

# from chatGPT will change once I get more information about this
    class Meta:
        unique_together = ("college", "name")
        ordering = ["college__abbreviation", "name"]

    def __str__(self):
        return f"{self.name} ({self.college.abbreviation})"
    def __str__(self):
        return self.college_name or self.abbreviation

class Major(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="majors")
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, blank=True)  # optional, e.g., "CS"

# from chatGPT will change once I get more information about this
    class Meta:
        unique_together = ("college", "name")
        ordering = ["college__abbreviation", "name"]

    def __str__(self):
        return f"{self.name} ({self.college.abbreviation})"
