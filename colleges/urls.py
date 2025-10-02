from django.urls import path
from . import views

urlpatterns = [
    path("", views.college_list_view, name="college_list"),
    path("<int:pk>/", views.college_detail_view, name="college_detail"),
]
