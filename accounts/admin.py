# accounts/admin.py
from django.contrib import admin
from .models import UserProfile, Course, Club, CareerPath


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.
    Displays key academic fields and enables searching/filtering by user and college.
    """
    list_display = ("user", "college", "major", "academic_year", "gpa")
    list_filter = ("college", "academic_year")
    search_fields = (
        "user__username",
        "college__college_name",
        "major__name",
    )
    ordering = ("user__username",)  # optional: keeps list ordered alphabetically by user


# Simple registration for additional models
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("subject", "number", "title", "credits")
    search_fields = ("subject", "number", "title")
    ordering = ("subject", "number")


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "college", "category")
    search_fields = ("name", "college__college_name")
    list_filter = ("college", "category")
    ordering = ("name",)


@admin.register(CareerPath)
class CareerPathAdmin(admin.ModelAdmin):
    list_display = ("title", "related_major", "salary_range")
    search_fields = ("title", "related_major__name")
    list_filter = ("related_major",)
    ordering = ("title",)
