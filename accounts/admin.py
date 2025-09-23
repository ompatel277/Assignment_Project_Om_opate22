from django.contrib import admin
from .models import User, Userprofile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "email", "phone_number", "first_name", "last_name")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

@admin.register(Userprofile)
class UserprofileAdmin(admin.ModelAdmin):
    list_display = ("user", "major", "college", "graduation_year", "academic_year", "gpa")
    search_fields = ("user__username", "user__email", "major__name", "college__college_name")
    list_filter = ("academic_year", "graduation_year")
    ordering = ("user",)
