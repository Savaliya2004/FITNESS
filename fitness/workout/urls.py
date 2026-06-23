from django.urls import path
from . import views

urlpatterns = [
    path('workouts/', views.workout_list, name='workouts'),
    path('trainers/', views.trainer_list, name='trainers'),
    path('sport/', views.sport, name='sport'),
    path('routine/add/<int:exercise_id>/', views.add_to_routine, name='add_to_routine'),
    path('routine/remove/<int:routine_id>/', views.remove_from_routine, name='remove_from_routine'),
    path('routine/generate/', views.generate_routine, name='generate_routine'),
]
