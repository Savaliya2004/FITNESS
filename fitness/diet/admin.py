from django.contrib import admin
from django.utils.html import format_html
from .models import Meal, DietPlan, UserDiet, MealPlan, UserProgress, BodyMeasurement, ProgressPhoto, GoalMilestone


# ─────────────────────────────────────────────────────────────────
# MEAL ADMIN  (the heart of the admin-driven diet system)
# ─────────────────────────────────────────────────────────────────
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display  = ('name', 'meal_type_badge', 'dietary_badge', 'goal_tag',
                     'calories', 'protein_g', 'carbs_g', 'fats_g', 'is_active')
    list_filter   = ('meal_type', 'dietary_type', 'goal_tag', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    ordering      = ('meal_type', 'dietary_type', 'name')
    list_per_page = 30

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'meal_type', 'dietary_type', 'goal_tag', 'is_active')
        }),
        ('Nutritional Values (per serving)', {
            'fields': (('calories', 'protein', 'carbs', 'fats', 'fiber'),)
        }),
    )

    @admin.display(description='Type')
    def meal_type_badge(self, obj):
        color_map = {
            'breakfast': '#f59e0b', 'lunch': '#22c55e',
            'dinner': '#3b82f6', 'snack': '#ec4899',
        }
        color = color_map.get(obj.meal_type, '#888')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600">{}</span>',
            color, obj.get_meal_type_display()
        )

    @admin.display(description='Diet')
    def dietary_badge(self, obj):
        color_map = {'veg': '#22c55e', 'egg': '#f59e0b', 'nonveg': '#ef4444'}
        color = color_map.get(obj.dietary_type, '#888')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600">{}</span>',
            color, obj.get_dietary_type_display()
        )

    @admin.display(description='Protein (g)')
    def protein_g(self, obj):
        return f"{obj.protein}g"

    @admin.display(description='Carbs (g)')
    def carbs_g(self, obj):
        return f"{obj.carbs}g"

    @admin.display(description='Fats (g)')
    def fats_g(self, obj):
        return f"{obj.fats}g"


# ─────────────────────────────────────────────────────────────────
# DIET PLAN TEMPLATE ADMIN
# ─────────────────────────────────────────────────────────────────
@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display  = ('name', 'goal_type', 'dietary_type',
                     'target_calories_min', 'target_calories_max', 'is_active')
    list_filter   = ('goal_type', 'dietary_type', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)


# ─────────────────────────────────────────────────────────────────
# USER DIET ADMIN  (read-only view of generated 7-day plans)
# ─────────────────────────────────────────────────────────────────
@admin.register(UserDiet)
class UserDietAdmin(admin.ModelAdmin):
    list_display  = ('user', 'day_of_week', 'breakfast', 'lunch', 'dinner', 'snack',
                     'total_calories', 'total_protein', 'generated_at')
    list_filter   = ('day_of_week', 'generated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('generated_at', 'total_calories', 'total_protein',
                       'total_carbs', 'total_fats')
    ordering      = ('-generated_at', 'user', 'day_of_week')
    list_per_page = 25




# ─────────────────────────────────────────────────────────────────
# LEGACY MODELS
# ─────────────────────────────────────────────────────────────────
@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display  = ('user', 'day_of_week', 'meal_name', 'calories')
    list_filter   = ('day_of_week',)
    search_fields = ('user__username', 'meal_name')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display  = ('user', 'date', 'current_weight', 'calories_burned')
    list_filter   = ('date',)
    search_fields = ('user__username',)


@admin.register(BodyMeasurement)
class BodyMeasurementAdmin(admin.ModelAdmin):
    list_display  = ('user', 'date', 'weight', 'body_fat_percentage', 'waist')
    list_filter   = ('date',)
    search_fields = ('user__username',)


@admin.register(ProgressPhoto)
class ProgressPhotoAdmin(admin.ModelAdmin):
    list_display  = ('user', 'date', 'angle', 'is_public')
    list_filter   = ('angle', 'is_public', 'date')
    search_fields = ('user__username',)


@admin.register(GoalMilestone)
class GoalMilestoneAdmin(admin.ModelAdmin):
    list_display  = ('user', 'title', 'milestone_type', 'target_value',
                     'current_value', 'achieved')
    list_filter   = ('milestone_type', 'achieved')
    search_fields = ('user__username', 'title')
