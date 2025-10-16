from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.course_list_view, name="courses"),
    path("course/<int:pk>/", views.course_detail_view, name="course_detail"),
    path("categories/", views.category_list_view, name="categories"),
    path("requirements/", views.requirement_list_view, name="requirements"),
]
