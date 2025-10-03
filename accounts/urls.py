from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),

    # Profiles
    path("profile/edit/", views.edit_profile_view, name="edit_profile"),  # put this first
    path("profile/", views.profile_view, name="profile"),
    path("profile/<str:username>/", views.profile_view, name="profile_other"),

    # Users list
    path("users/http/", views.user_list_http, name="user_list_http"),
]
