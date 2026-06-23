from django.urls import path
from . import views

urlpatterns = [
    # Main diet page – shows 7-day plan
    path('', views.diet_home, name='diet'),



    # Download 7-day plan as HTML/PDF
    path('download/', views.diet_pdf_download, name='diet_pdf_download'),

    # Legacy JS-based save (backward-compat)
    path('save/', views.save_diet_plan, name='save_diet_plan'),
]
