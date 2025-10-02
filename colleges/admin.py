from django.contrib import admin
from .models import College, Major


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("abbreviation", "college_name", "city", "state")
    search_fields = ("college_name", "abbreviation", "city", "state")
    ordering = ("abbreviation",)


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "college")
    search_fields = ("name", "code", "college__abbreviation")
    list_filter = ("college",)
