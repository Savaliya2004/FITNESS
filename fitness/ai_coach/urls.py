from django.urls import path
from . import views

urlpatterns = [
    path('', views.coach_dashboard, name='ai_coach_dashboard'),
    path('generate/', views.generate_plan, name='ai_coach_generate'),
]
