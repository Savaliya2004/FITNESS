from django.contrib import admin
from .models import WorkoutProgram, Trainer

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'rating')
    search_fields = ('name', 'specialty')

@admin.register(WorkoutProgram)
class WorkoutProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'duration_weeks')
    list_filter = ('category', 'difficulty')
    search_fields = ('title', 'description')

from .models import Exercise, UserRoutine

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'exercise_type', 'difficulty', 'calories_burned')
    list_filter = ('category', 'exercise_type', 'difficulty')
    search_fields = ('name',)

@admin.register(UserRoutine)
class UserRoutineAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'added_on')
    search_fields = ('user__username', 'exercise__name')
