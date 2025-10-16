from django.contrib import admin
from .models import Career

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "get_industries", "created_at")
    search_fields = ("title", "company", "description")
    ordering = ("title",)
    list_filter = ("company",)

    def get_industries(self, obj):
        return ", ".join(obj.industries) if obj.industries else "-"
    get_industries.short_description = "Industries"
