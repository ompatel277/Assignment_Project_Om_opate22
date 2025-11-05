# recommender/urls.py
from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    # Main recommendations dashboard
    path('', views.recommendations_dashboard, name='dashboard'),

    # Detailed recommendation views
    path('careers/', views.career_recommendations_view, name='careers'),
    path('portfolio/', views.portfolio_recommendations_view, name='portfolio'),

    # 🆕 Roadmap views (NEW)
    path('roadmap/', views.roadmap_view, name='roadmap'),
    path('roadmap/summary/', views.roadmap_summary_view, name='roadmap_summary'),
]