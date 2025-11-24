from django.contrib import admin
from .models import College, Major


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("college_name", "abbreviation", "city", "state")
    search_fields = ("college_name", "abbreviation", "city", "state")
    list_filter = ("state",)
    ordering = ("college_name",)


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "college")
    search_fields = ("name", "code", "college__college_name", "college__abbreviation")
    list_filter = ("college",)
    ordering = ("name",)
