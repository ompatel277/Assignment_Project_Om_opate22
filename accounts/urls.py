from django.urls import path
from . import views

urlpatterns = [
    path("users/http/", views.user_list_http, name="user_list_http"),
    path("users/render/", views.user_list_render, name="user_list_render"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]
