from . import views
from django.urls import path


app_name = "colleges"
urlpatterns = [
    path("", views.CollegeListView.as_view(), name="list"),
    path("<int:pk>/", views.CollegeDetailView.as_view(), name="detail"),
    path("<int:college_id>/majors-json/", views.majors_json_view, name="majors_json"),
    path("chart/", views.college_chart, name="college_chart"),  # ✅ Matplotlib chart endpoint
]
