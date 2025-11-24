from django.db import models

class Career(models.Model):
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=100, blank=True, null=True)
    industries = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Career"
        verbose_name_plural = "Careers"

    def __str__(self):
        return f"{self.title} ({self.company or 'Independent'})"
