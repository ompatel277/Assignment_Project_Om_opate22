from django.db import models


class Course(models.Model):
    """
    Represents a course in a college catalog.
    """
    subject = models.CharField(max_length=10)
    number = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    credits = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField(blank=True)
    college = models.ForeignKey(
        "colleges.College",
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["subject", "number"]
        unique_together = ("subject", "number", "college")

    def __str__(self):
        return f"{self.subject} {self.number} – {self.title}"


class DegreeCategory(models.Model):
    """
    Groups degree requirements (like Core Courses, Electives).
    """
    name = models.CharField(max_length=100)
    min_credits = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    major = models.ForeignKey(
        "colleges.Major",
        on_delete=models.CASCADE,
        related_name="categories"
    )

    def __str__(self):
        return f"{self.name} ({self.major.name})"


class DegreeRequirement(models.Model):
    """
    Connects specific courses to degree requirement categories.
    """
    category = models.ForeignKey(
        DegreeCategory,
        on_delete=models.CASCADE,
        related_name="items"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requirements"
    )
    note = models.TextField(blank=True)

    def __str__(self):
        if self.course:
            return f"{self.course.subject} {self.course.number} ({self.category.name})"
        return f"Note: {self.note[:30]}"
