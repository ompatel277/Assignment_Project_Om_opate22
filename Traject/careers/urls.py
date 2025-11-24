# careers/urls.py
from django.urls import path
from . import views

app_name = "careers"

urlpatterns = [
    path("", views.career_list_view, name="list"),
    path("<int:pk>/", views.career_detail_view, name="detail"),
    path("recommended/", views.recommended_careers_view, name="recommended"),
]
