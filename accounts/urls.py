# accounts/urls.py
# Updated for A9 Assignment - JSON APIs + Chart Integration + Portfolio Checklist

from django.urls import path
from . import views
from . import portfolio_views  # 🆕 Import new portfolio views
from .views import (
    UsersAPI,
    UsersChartPage,
    AcademicYearChartPage,
    users_per_college_chart_png,
    users_per_year_chart_png,
)

app_name = "accounts"

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

    # =====================================================
    #  JSON API ENDPOINTS (Week 9)
    # =====================================================

    # --- HttpResponse vs JsonResponse Demo ---
    path("api/ping-httpresponse/", views.api_ping_httpresponse, name="api_ping_httpresponse"),
    path("api/ping-json/", views.api_ping_jsonresponse, name="api_ping_json"),

    # --- Function-Based API Views ---
    path("api/users/", views.api_users, name="api_users"),
    path("api/colleges/users/", views.api_users_per_college, name="api_users_per_college"),
    path("api/users/academic-year/", views.api_users_per_academic_year, name="api_users_per_academic_year"),
    path("api/courses/per-major/", views.api_courses_per_major, name="api_courses_per_major"),
    path("api/clubs/per-college/", views.api_clubs_per_college, name="api_clubs_per_college"),

    # --- Class-Based API Views ---
    path("api/class-users/", UsersAPI.as_view(), name="api_class_users"),

    # =====================================================
    #  CHART ENDPOINTS (Week 9)
    # =====================================================

    # --- Chart PNG Images (Server-Generated) ---
    path("charts/users-per-college.png", users_per_college_chart_png, name="chart_users_per_college_png"),
    path("charts/users-per-year.png", users_per_year_chart_png, name="chart_users_per_year_png"),

    # --- Chart Pages (Templates that display the charts) ---
    path("charts/users-per-college/", UsersChartPage.as_view(), name="chart_users_per_college_page"),
    path("charts/academic-year/", AcademicYearChartPage.as_view(), name="chart_academic_year_page"),

    # =====================================================
    #  🆕 PORTFOLIO CHECKLIST (NEW)
    # =====================================================

    # Main checklist view
    path("portfolio/checklist/", portfolio_views.portfolio_checklist_view, name="portfolio_checklist"),

    # Browse all portfolio items
    path("portfolio/browse/", portfolio_views.browse_portfolio_items, name="browse_portfolio"),

    # Portfolio item detail
    path("portfolio/item/<int:item_id>/", portfolio_views.portfolio_item_detail, name="portfolio_item_detail"),

    # Add to checklist
    path("portfolio/add/<int:item_id>/", portfolio_views.add_to_checklist, name="add_to_checklist"),

    # Update checklist item
    path("portfolio/update-status/<int:checklist_id>/", portfolio_views.update_checklist_status,
         name="update_checklist_status"),
    path("portfolio/update-progress/<int:checklist_id>/", portfolio_views.update_progress, name="update_progress"),
    path("portfolio/update-priority/<int:checklist_id>/", portfolio_views.update_priority, name="update_priority"),

    # Remove from checklist
    path("portfolio/remove/<int:checklist_id>/", portfolio_views.remove_from_checklist, name="remove_from_checklist"),
]