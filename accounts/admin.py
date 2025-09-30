from django.contrib import admin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "first_name", "last_name")
    search_fields = ("email", "username")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "college", "major", "graduation_year", "academic_year", "gpa")
    search_fields = ("user__username", "college__name", "major__name")
