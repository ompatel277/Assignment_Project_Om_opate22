from io import BytesIO
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView, FormView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from .models import College, Major
from .forms import CollegeSearchForm, MajorForm
from accounts.models import UserProfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ====================================
# 🏫 College List View (Existing)
# ====================================
class CollegeListView(ListView):
    model = College
    template_name = "colleges/college_list.html"
    context_object_name = "colleges"

    def get_queryset(self):
        qs = College.objects.all().order_by("abbreviation")
        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(college_name__icontains=q)
                | Q(abbreviation__icontains=q)
                | Q(city__icontains=q)
                | Q(state__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = (self.request.GET.get("q") or "").strip()
        context["q"] = q

        if q:
            context["result_count"] = context["object_list"].count()

        # --- Analytics ---
        context["total_colleges"] = College.objects.count()
        context["total_majors"] = Major.objects.count()
        context["total_students"] = UserProfile.objects.filter(college__isnull=False).count()

        context["majors_per_college"] = (
            College.objects.annotate(major_count=Count("majors"))
            .values("id", "abbreviation", "college_name", "major_count")
            .order_by("abbreviation")
        )

        context["students_per_college"] = (
            UserProfile.objects.filter(college__isnull=False)
            .values("college__id", "college__abbreviation", "college__college_name")
            .annotate(student_count=Count("id"))
            .order_by("college__abbreviation")
        )

        return context


# ====================================
# 🎓 College Detail View (Existing)
# ====================================
class CollegeDetailView(DetailView):
    model = College
    template_name = "colleges/college_detail.html"
    context_object_name = "college"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        college = self.object
        context["majors"] = college.majors.all().order_by("name")
        context["student_count"] = UserProfile.objects.filter(college=college).count()
        return context


# ====================================
# 📊 JSON Endpoint for Majors (Existing)
# ====================================
def majors_json_view(request, college_id):
    """Return all majors for a given college in JSON format."""
    majors = (
        Major.objects.filter(college_id=college_id)
        .order_by("name")
        .values("id", "name", "code")
    )
    return JsonResponse({"majors": list(majors)})


# ====================================
# 📈 Matplotlib Chart View (Existing)
# ====================================
def college_chart(request):
    """Return a PNG bar chart showing number of majors per college."""
    data = (
        College.objects.annotate(num_majors=Count("majors"))
        .values_list("college_name", "num_majors")
        .order_by("-num_majors")
    )

    labels = [d[0] for d in data]
    counts = [d[1] for d in data]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(labels, counts, color="#3b82f6")
    ax.set_title("Majors per College", fontsize=14, weight="bold")
    ax.set_xlabel("College")
    ax.set_ylabel("Number of Majors")
    ax.tick_params(axis="x", rotation=25)

    for bar, c in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, c + 0.1, str(c),
                ha="center", va="bottom", fontsize=9)

    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type="image/png")


# ============================================================
# === A8: Demonstration Views (GET vs POST, FBV vs CBV) ======
# ============================================================

# -------------------------------
# 🧭 GET Example — College Search
# -------------------------------
def college_search_view(request):
    """
    Function-Based View demonstrating GET method.
    When user submits a search, the query (?q=...) appears in the URL.
    """
    form = CollegeSearchForm(request.GET or None)
    results = None

    if form.is_valid() and form.cleaned_data.get("q"):
        query = form.cleaned_data["q"]
        results = College.objects.filter(
            Q(college_name__icontains=query) | Q(abbreviation__icontains=query)
        )

    return render(request, "colleges/college_search.html", {
        "form": form,
        "results": results
    })


# -------------------------------------------
# 🧩 POST Example — Function-Based (FBV)
# -------------------------------------------
def add_major_fbv(request):
    """
    Function-Based View for handling a POST form submission.
    Demonstrates CSRF protection and validation logic.
    """
    if request.method == "POST":
        form = MajorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Major added successfully via FBV!")
            return redirect("colleges:major_add_fbv")
    else:
        form = MajorForm()

    return render(request, "colleges/add_major_fbv.html", {"form": form})


# -------------------------------------------
# 🧱 POST Example — Class-Based (CBV)
# -------------------------------------------
class AddMajorCBV(FormView):
    """
    Class-Based View demonstrating POST handling via FormView.
    Uses the same MajorForm as the FBV example.
    """
    template_name = "colleges/add_major_cbv.html"
    form_class = MajorForm
    success_url = reverse_lazy("colleges:major_add_cbv")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Major added successfully via CBV!")
        return super().form_valid(form)
