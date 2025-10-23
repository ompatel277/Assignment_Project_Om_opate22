from django.urls import path
from . import views

app_name = "colleges"

urlpatterns = [
    # ====================================
    # Existing Traject routes (keep these)
    # ====================================
    path("", views.CollegeListView.as_view(), name="list"),
    path("<int:pk>/", views.CollegeDetailView.as_view(), name="detail"),
    path("<int:college_id>/majors-json/", views.majors_json_view, name="majors_json"),
    path("chart/", views.college_chart, name="college_chart"),  # ✅ Matplotlib chart endpoint

    # ====================================
    # A8 Demonstration routes (GET vs POST)
    # ====================================
    path("search/", views.college_search_view, name="college_search"),  # GET example
    path("add-major-fbv/", views.add_major_fbv, name="major_add_fbv"),  # POST FBV example
    path("add-major-cbv/", views.AddMajorCBV.as_view(), name="major_add_cbv"),  # POST CBV example
]
