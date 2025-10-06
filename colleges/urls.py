from django.urls import path
from .views import CollegeListView, CollegeDetailView
# from .views import CollegeGenericListView, CollegeDetailGenericView  # old imports

app_name = "colleges"

urlpatterns = [
    # Old routes (HW5)
    # path("list/", CollegeGenericListView.as_view(), name="list_generic"),
    # path("<int:pk>/", CollegeDetailGenericView.as_view(), name="detail_generic"),

    # Active routes (HW6)
    path("list/", CollegeListView.as_view(), name="list"),
    path("<int:pk>/", CollegeDetailView.as_view(), name="detail"),
]
