from django.contrib import admin
from .models import Course, DegreeCategory, DegreeRequirement


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("subject", "number", "title", "credits", "college")
    search_fields = ("subject", "number", "title")
    list_filter = ("college", "subject")


@admin.register(DegreeCategory)
class DegreeCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "major", "min_credits")
    list_filter = ("major",)
    search_fields = ("name",)


@admin.register(DegreeRequirement)
class DegreeRequirementAdmin(admin.ModelAdmin):
    list_display = ("category", "course", "note")
    list_filter = ("category",)
