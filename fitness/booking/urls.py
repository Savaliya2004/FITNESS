from django.urls import path
from . import views

urlpatterns = [
    path('', views.class_schedule, name='schedule'),
    path('book/<int:schedule_id>/', views.book_class, name='book_class'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
