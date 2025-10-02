from django.shortcuts import render, get_object_or_404
from .models import College, Major

def college_list_view(request):
    colleges = College.objects.all()
    return render(request, "colleges/college_list.html", {"colleges": colleges})

def college_detail_view(request, pk):
    college = get_object_or_404(College, pk=pk)
    majors = college.majors.all()
    return render(request, "colleges/college_detail.html", {
        "college": college,
        "majors": majors
    })
