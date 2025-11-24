# accounts/admin.py
from django.contrib import admin
from .models import UserProfile, Course, Club, CareerPath, PortfolioItem, UserChecklist, CareerPlan, PlanItem


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


# =====================================================
#  🆕 NEW: CAREER PLAN ADMIN
# =====================================================

class PlanItemInline(admin.TabularInline):
    """Inline editor for plan items within a career plan."""
    model = PlanItem
    extra = 1
    fields = ('portfolio_item', 'course', 'custom_title', 'status', 'priority', 'target_semester')


@admin.register(CareerPlan)
class CareerPlanAdmin(admin.ModelAdmin):
    """
    Admin configuration for CareerPlan model.
    Allows users to create and manage multiple career plans.
    """
    list_display = (
        "name",
        "user_profile",
        "target_career",
        "is_primary",
        "is_active",
        "get_progress",
        "created_at"
    )

    list_filter = (
        "is_primary",
        "is_active",
        "target_career",
    )

    search_fields = (
        "name",
        "user_profile__user__username",
        "target_career__title",
        "description"
    )

    readonly_fields = ("created_at", "updated_at", "get_progress")

    ordering = ("-is_primary", "-is_active", "-created_at")

    fieldsets = (
        ("Plan Basics", {
            "fields": ("user_profile", "target_career", "name", "description")
        }),
        ("Timeline & Status", {
            "fields": ("target_date", "is_active", "is_primary")
        }),
        ("Progress", {
            "fields": ("get_progress",),
            "classes": ("collapse",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    inlines = [PlanItemInline]

    actions = ["set_as_primary", "mark_active", "mark_inactive"]

    def get_progress(self, obj):
        """Display progress percentage."""
        return f"{obj.get_progress_percentage()}%"

    get_progress.short_description = "Progress"

    def set_as_primary(self, request, queryset):
        """Set selected plan as primary."""
        if queryset.count() > 1:
            self.message_user(request, "Can only set one plan as primary at a time.", level='error')
            return
        plan = queryset.first()
        plan.set_as_primary()
        self.message_user(request, f"'{plan.name}' set as primary plan.")

    set_as_primary.short_description = "Set as Primary Plan"

    def mark_active(self, request, queryset):
        """Mark plans as active."""
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} plans marked as active.")

    mark_active.short_description = "Mark as Active"

    def mark_inactive(self, request, queryset):
        """Mark plans as inactive."""
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} plans marked as inactive.")

    mark_inactive.short_description = "Mark as Inactive"


@admin.register(PlanItem)
class PlanItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for PlanItem model.
    Individual milestones within career plans.
    """
    list_display = (
        "get_title",
        "career_plan",
        "status",
        "priority",
        "target_semester",
        "completed_at"
    )

    list_filter = (
        "status",
        "priority",
        "career_plan__target_career",
    )

    search_fields = (
        "custom_title",
        "portfolio_item__title",
        "course__title",
        "career_plan__name"
    )

    readonly_fields = ("added_at", "completed_at")

    ordering = ("-priority", "added_at")

    fieldsets = (
        ("Plan Item", {
            "fields": ("career_plan", "portfolio_item", "course")
        }),
        ("Custom Milestone", {
            "fields": ("custom_title", "custom_description"),
            "classes": ("collapse",)
        }),
        ("Status & Timeline", {
            "fields": ("status", "priority", "target_semester", "notes")
        }),
        ("Timestamps", {
            "fields": ("added_at", "completed_at"),
            "classes": ("collapse",)
        }),
    )

    actions = ["mark_completed", "mark_in_progress", "mark_planned"]

    def get_title(self, obj):
        """Get display title."""
        return obj.get_title()

    get_title.short_description = "Item"

    def mark_completed(self, request, queryset):
        """Mark items as completed."""
        for item in queryset:
            item.mark_completed()
        self.message_user(request, f"{queryset.count()} items marked as completed.")

    mark_completed.short_description = "Mark as Completed"

    def mark_in_progress(self, request, queryset):
        """Mark items as in progress."""
        queryset.update(status='IN_PROGRESS')
        self.message_user(request, f"{queryset.count()} items marked as in progress.")

    mark_in_progress.short_description = "Mark as In Progress"

    def mark_planned(self, request, queryset):
        """Mark items as planned."""
        queryset.update(status='PLANNED')
        self.message_user(request, f"{queryset.count()} items marked as planned.")

    mark_planned.short_description = "Mark as Planned"