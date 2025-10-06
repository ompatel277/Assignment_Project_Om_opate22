# colleges/views.py
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView
from .models import College, Major
from accounts.models import UserProfile


class CollegeListView(ListView):
    model = College
    template_name = "colleges/college_list.html"
    context_object_name = "colleges"

    # Filtering
    def get_queryset(self):
        qs = College.objects.all().order_by("abbreviation")
        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(college_name__icontains=q) |
                Q(abbreviation__icontains=q) |
                Q(city__icontains=q) |
                Q(state__icontains=q)
            )
        return qs

    # Aggregations
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = (self.request.GET.get("q") or "").strip()
        context["q"] = q
        if q:
            context["result_count"] = context["object_list"].count()

        # Totals
        context["total_colleges"] = College.objects.count()
        context["total_majors"] = Major.objects.count()
        context["total_students"] = UserProfile.objects.filter(college__isnull=False).count()

        # Grouped: majors per college (includes 0 using annotate on College)
        context["majors_per_college"] = (
            College.objects
            .annotate(major_count=Count("majors"))
            .values("id", "abbreviation", "college_name", "major_count")
            .order_by("abbreviation")
        )

        # Grouped: students per college (only rows that have a college)
        context["students_per_college"] = (
            UserProfile.objects
            .filter(college__isnull=False)
            .values("college__id", "college__abbreviation", "college__college_name")
            .annotate(student_count=Count("id"))
            .order_by("college__abbreviation")
        )

        return context


class CollegeDetailView(DetailView):
    model = College
    template_name = "colleges/college_detail.html"
    context_object_name = "college"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["majors"] = Major.objects.filter(college=self.object).order_by("name")
        context["student_count"] = UserProfile.objects.filter(college=self.object).count()
        return context
