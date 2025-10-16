from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, DegreeCategory, DegreeRequirement


@login_required
def course_list_view(request):
    courses = Course.objects.all().order_by("subject", "number")
    return render(request, "catalog/course_list.html", {"courses": courses})


@login_required
def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, "catalog/course_detail.html", {"course": course})


@login_required
def category_list_view(request):
    categories = DegreeCategory.objects.all().select_related("major")
    return render(request, "catalog/category_list.html", {"categories": categories})


@login_required
def requirement_list_view(request):
    requirements = DegreeRequirement.objects.select_related("category", "course")
    return render(request, "catalog/requirement_list.html", {"requirements": requirements})
