from django.db import models


class College(models.Model):
    college_name = models.CharField(max_length=300)  # full college name
    city = models.CharField(max_length=100)          # city name
    state = models.CharField(max_length=100)         # state name
    abbreviation = models.CharField(max_length=50, unique=True)  # ex: UIUC
    logo_url = models.URLField(blank=True, null=True)  # optional logo

    def __str__(self):
        return f"{self.abbreviation} - {self.college_name}"


class Major(models.Model):
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name="majors"
    )
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, blank=True)  # optional, e.g., "CS"

    class Meta:
        unique_together = ("college", "name")  # no duplicate majors in same college
        ordering = ["college__abbreviation", "name"]

    def __str__(self):
        return f"{self.name} ({self.college.abbreviation})"
