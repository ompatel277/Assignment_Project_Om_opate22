from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from .models import College, Major


# Base CBV: manually write get()
class CollegeListView(View):
    def get(self, request):
        colleges = College.objects.all()
        context = {"colleges": colleges}
        return render(request, "colleges/college_list_view.html", context)


# Generic CBV: let Django handle most of it
class CollegeGenericListView(ListView):
    model = College
    context_object_name = "colleges"
    template_name = "colleges/college_list_generic.html"


# Generic Detail View
class CollegeDetailGenericView(DetailView):
    model = College
    context_object_name = "college"
    template_name = "colleges/college_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add related majors for the selected college
        context["majors"] = Major.objects.filter(college=self.object)
        return context
