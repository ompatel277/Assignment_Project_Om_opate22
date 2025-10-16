# accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"  # ✅ Helps with reverse() & namespacing in templates

urlpatterns = [
    # =====================================================
    #  AUTHENTICATION
    # =====================================================
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # =====================================================
    #  DASHBOARD & ONBOARDING
    # =====================================================
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("choose-college/", views.choose_college_view, name="choose_college"),

    # =====================================================
    #  PROFILE MANAGEMENT
    # =====================================================
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile_view, name="edit_profile"),
    path("profile/<str:username>/", views.profile_view, name="profile_other"),

    # =====================================================
    #  USER LIST & COLLEGE ACTIONS
    # =====================================================
    path("users/http/", views.user_list_http, name="user_list_http"),
    path("set-college/<int:college_id>/", views.set_college, name="set_college"),
]
