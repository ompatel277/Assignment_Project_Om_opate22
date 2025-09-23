from django.urls import path
from . import views

urlpatterns = [
    path("users/http/", views.user_list_http, name="user_list_http"),
    path("users/render/", views.user_list_render, name="user_list_render"),
    path("", views.user_list_render, name="home"),  # homepage → render view
]
