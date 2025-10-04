# colleges/urls.py
from django.urls import path
from .views import CollegeListView, CollegeGenericListView, CollegeDetailGenericView

app_name = "colleges"

urlpatterns = [
    path("list/", CollegeListView.as_view(), name="list"),
    path("generic/", CollegeGenericListView.as_view(), name="list_generic"),
    path("<int:pk>/", CollegeDetailGenericView.as_view(), name="detail"),
]
