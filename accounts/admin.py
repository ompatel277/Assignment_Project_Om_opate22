# accounts/admin.py
from django.contrib import admin
from .models import UserProfile, Course, Club, CareerPath, PortfolioItem, UserChecklist


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


# =====================================================
#  🆕 NEW: PORTFOLIO ITEM ADMIN
# =====================================================

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for PortfolioItem model.
    Allows easy management of projects, certifications, and milestones.
    """
    list_display = (
        "title",
        "item_type",
        "difficulty_level",
        "estimated_hours",
        "get_related_careers_count"
    )

    list_filter = (
        "item_type",
        "difficulty_level",
    )

    search_fields = (
        "title",
        "description",
        "skills_gained"
    )

    filter_horizontal = ("related_careers",)  # Nice UI for ManyToMany

    ordering = ("difficulty_level", "title")

    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "item_type", "description")
        }),
        ("Skills & Difficulty", {
            "fields": ("skills_gained", "difficulty_level", "estimated_hours")
        }),
        ("Career Connections", {
            "fields": ("related_careers",)
        }),
        ("Resources", {
            "fields": ("resource_url",)
        }),
    )

    def get_related_careers_count(self, obj):
        """Display count of related careers."""
        return obj.related_careers.count()

    get_related_careers_count.short_description = "Related Careers"


# =====================================================
#  🆕 NEW: USER CHECKLIST ADMIN
# =====================================================

@admin.register(UserChecklist)
class UserChecklistAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserChecklist model.
    Allows tracking and managing user progress on portfolio items.
    """
    list_display = (
        "user_profile",
        "portfolio_item",
        "status",
        "progress_percentage",
        "priority",
        "added_at",
        "completed_at"
    )

    list_filter = (
        "status",
        "priority",
        "portfolio_item__item_type",
        "portfolio_item__difficulty_level",
    )

    search_fields = (
        "user_profile__user__username",
        "portfolio_item__title",
        "notes"
    )

    readonly_fields = ("added_at", "started_at", "completed_at")

    ordering = ("-priority", "-added_at")

    fieldsets = (
        ("User & Item", {
            "fields": ("user_profile", "portfolio_item")
        }),
        ("Progress Tracking", {
            "fields": ("status", "progress_percentage", "priority")
        }),
        ("Notes", {
            "fields": ("notes",)
        }),
        ("Timestamps", {
            "fields": ("added_at", "started_at", "completed_at"),
            "classes": ("collapse",)  # Collapsible section
        }),
    )

    # Enable inline editing
    actions = ["mark_as_completed", "mark_as_in_progress", "mark_as_planned"]

    def mark_as_completed(self, request, queryset):
        """Bulk action to mark items as completed."""
        for item in queryset:
            item.mark_completed()
        self.message_user(request, f"{queryset.count()} items marked as completed.")

    mark_as_completed.short_description = "Mark selected items as Completed"

    def mark_as_in_progress(self, request, queryset):
        """Bulk action to mark items as in progress."""
        for item in queryset:
            item.mark_in_progress()
        self.message_user(request, f"{queryset.count()} items marked as In Progress.")

    mark_as_in_progress.short_description = "Mark selected items as In Progress"

    def mark_as_planned(self, request, queryset):
        """Bulk action to mark items as planned."""
        queryset.update(status='PLANNED')
        self.message_user(request, f"{queryset.count()} items marked as Planned.")

    mark_as_planned.short_description = "Mark selected items as Planned"