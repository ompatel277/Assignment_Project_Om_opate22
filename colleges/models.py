from django.db import models


# ====================================
# 🏫 College Model
# ====================================
class College(models.Model):
    college_name = models.CharField(max_length=300)  # Full college name
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=50, unique=True)  # e.g. UIUC
    logo_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["college_name"]

    def __str__(self):
        return f"{self.abbreviation} — {self.college_name}"


# ====================================
# 🎓 Major Model
# ====================================
class Major(models.Model):
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name="majors"
    )
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, blank=True)  # e.g., CS, ECE, etc.

    class Meta:
        unique_together = ("college", "name")  # Prevent duplicates within same college
        ordering = ["college__abbreviation", "name"]

    def __str__(self):
        return f"{self.name} ({self.college.abbreviation})"


# ====================================
# 📚 Course Model
# ====================================
class Course(models.Model):
    subject = models.CharField(max_length=10)  # e.g. "CS"
    number = models.CharField(max_length=10)  # e.g. "225"
    title = models.CharField(max_length=255)
    credits = models.DecimalField(max_digits=4, decimal_places=1, default=3.0)

    # Optional — link to a specific Major (helpful for recommendations)
    major = models.ForeignKey(
        Major,
        on_delete=models.SET_NULL,
        related_name="courses",
        blank=True,
        null=True,
        help_text="Optional link to a related major"
    )

    class Meta:
        unique_together = ("subject", "number")
        ordering = ["subject", "number"]

    def __str__(self):
        return f"{self.subject} {self.number} — {self.title}"


# ====================================
# 📖 Degree Requirement Category
# ====================================
class DegreeRequirementCategory(models.Model):
    major = models.ForeignKey(
        Major,
        on_delete=models.CASCADE,
        related_name="requirement_categories"
    )
    name = models.CharField(max_length=255)  # e.g., "Core Courses", "Gen Ed"
    min_credits = models.PositiveSmallIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["major__name", "name"]

    def __str__(self):
        return f"{self.major.name} — {self.name}"


# ====================================
# ✅ Degree Requirement Item
# ====================================
class DegreeRequirementItem(models.Model):
    category = models.ForeignKey(
        DegreeRequirementCategory,
        on_delete=models.CASCADE,
        related_name="items"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="degree_requirements"
    )
    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if self.course:
            return f"{self.course.subject} {self.course.number}"
        return self.note or "(Requirement)"
