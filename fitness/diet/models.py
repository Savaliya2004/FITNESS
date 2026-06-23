from django.db import models
from django.conf import settings
import json


# ─────────────────────────────────────────────────────────────────
# MEAL  (admin-managed, the source of truth for all food items)
# ─────────────────────────────────────────────────────────────────
class Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    DIETARY_CHOICES = [
        ('veg', 'Vegetarian'),
        ('egg', 'Eggetarian'),
        ('nonveg', 'Non-Vegetarian'),
    ]
    GOAL_CHOICES = [
        ('any', 'Any Goal'),
        ('weight_loss', 'Weight Loss'),
        ('fat_loss', 'Fat Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('maintenance', 'Maintenance'),
        ('endurance', 'Endurance'),
        ('general_fitness', 'General Fitness'),
    ]

    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Brief description of the meal")
    meal_type   = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    dietary_type = models.CharField(max_length=10, choices=DIETARY_CHOICES, default='veg')
    goal_tag    = models.CharField(max_length=30, choices=GOAL_CHOICES, default='any',
                                   help_text="Which fitness goal this meal suits best")

    # Nutrition per serving
    calories    = models.PositiveIntegerField(help_text="kcal per serving")
    protein     = models.FloatField(help_text="grams")
    carbs       = models.FloatField(help_text="grams")
    fats        = models.FloatField(help_text="grams")
    fiber       = models.FloatField(default=0, help_text="grams")

    is_active   = models.BooleanField(default=True, help_text="Uncheck to exclude from recommendations")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fitx_meals'
        ordering = ['meal_type', 'name']
        indexes = [
            models.Index(fields=['meal_type', 'dietary_type']),
            models.Index(fields=['goal_tag']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_meal_type_display()} | {self.calories} kcal)"


# ─────────────────────────────────────────────────────────────────
# DIET PLAN TEMPLATE  (optional grouping concept — admin-managed)
# ─────────────────────────────────────────────────────────────────
class DietPlan(models.Model):
    GOAL_CHOICES = Meal.GOAL_CHOICES

    name        = models.CharField(max_length=200)
    goal_type   = models.CharField(max_length=30, choices=GOAL_CHOICES, default='any')
    description = models.TextField(blank=True)
    dietary_type = models.CharField(max_length=10, choices=Meal.DIETARY_CHOICES, default='veg')
    target_calories_min = models.PositiveIntegerField(default=1200)
    target_calories_max = models.PositiveIntegerField(default=3500)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_diet_plans'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_goal_type_display()})"


# ─────────────────────────────────────────────────────────────────
# USER DIET  (the generated 7-day plan stored per-user)
# ─────────────────────────────────────────────────────────────────
class UserDiet(models.Model):
    DAYS = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='user_diets')
    day_of_week = models.CharField(max_length=15, choices=DAYS)
    generated_at = models.DateTimeField(auto_now_add=True)

    # Each slot holds a FK to a Meal
    breakfast   = models.ForeignKey(Meal, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='diet_breakfasts')
    lunch       = models.ForeignKey(Meal, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='diet_lunches')
    dinner      = models.ForeignKey(Meal, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='diet_dinners')
    snack       = models.ForeignKey(Meal, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='diet_snacks')

    # Computed daily totals (denormalised for fast reads)
    total_calories = models.PositiveIntegerField(default=0)
    total_protein  = models.FloatField(default=0)
    total_carbs    = models.FloatField(default=0)
    total_fats     = models.FloatField(default=0)

    class Meta:
        db_table = 'fitx_user_diets'
        ordering = ['id']
        # Only one plan per user-day at a time; regeneration deletes old ones
        unique_together = ('user', 'day_of_week', 'generated_at')

    def __str__(self):
        return f"{self.user.username} – {self.day_of_week}"

    def compute_totals(self):
        """Recalculate and save cumulative daily macros."""
        meals = [self.breakfast, self.lunch, self.dinner, self.snack]
        self.total_calories = sum(m.calories for m in meals if m)
        self.total_protein  = round(sum(m.protein for m in meals if m), 1)
        self.total_carbs    = round(sum(m.carbs for m in meals if m), 1)
        self.total_fats     = round(sum(m.fats for m in meals if m), 1)
        self.save(update_fields=['total_calories', 'total_protein', 'total_carbs', 'total_fats'])


# ─────────────────────────────────────────────────────────────────
# LEGACY / PROGRESS MODELS  (kept untouched, still used by admin)
# ─────────────────────────────────────────────────────────────────
class MealPlan(models.Model):
    """Legacy per-user daily plan stored as text strings. Kept for backward-compat."""
    DAYS = [
        ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='meal_plans')
    day_of_week = models.CharField(max_length=15, choices=DAYS)
    meal_name   = models.CharField(max_length=200, default="Daily Plan")
    breakfast   = models.CharField(max_length=200, blank=True, null=True)
    lunch       = models.CharField(max_length=200, blank=True, null=True)
    dinner      = models.CharField(max_length=200, blank=True, null=True)
    snacks      = models.CharField(max_length=200, blank=True, null=True)
    calories    = models.PositiveIntegerField()
    protein     = models.FloatField(help_text="in grams")
    carbs       = models.FloatField(help_text="in grams")
    fats        = models.FloatField(help_text="in grams")

    def __str__(self):
        return f"{self.user.username} - {self.day_of_week} - {self.meal_name}"


class UserProgress(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        related_name='progress_logs')
    date            = models.DateField(auto_now_add=True)
    calories_burned = models.PositiveIntegerField(default=0)
    workouts_done   = models.PositiveIntegerField(default=0)
    current_weight  = models.FloatField(help_text="in kg")
    streak          = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s progress on {self.date}"


class BodyMeasurement(models.Model):
    user               = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                           related_name='measurements')
    date               = models.DateField()
    weight             = models.FloatField(help_text="kg")
    body_fat_percentage = models.FloatField(null=True, blank=True)
    chest              = models.FloatField(null=True, blank=True, help_text="cm")
    waist              = models.FloatField(null=True, blank=True, help_text="cm")
    hips               = models.FloatField(null=True, blank=True, help_text="cm")
    biceps             = models.FloatField(null=True, blank=True, help_text="cm")
    thighs             = models.FloatField(null=True, blank=True, help_text="cm")
    notes              = models.TextField(blank=True)

    class Meta:
        db_table      = 'fitx_body_measurements'
        unique_together = ('user', 'date')
        ordering      = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.weight}kg"


class ProgressPhoto(models.Model):
    ANGLE_CHOICES = [('front', 'Front'), ('side', 'Side'), ('back', 'Back')]
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='progress_photos')
    date     = models.DateField()
    angle    = models.CharField(max_length=10, choices=ANGLE_CHOICES, default='front')
    image    = models.ImageField(upload_to='progress_photos/%Y/%m/')
    notes    = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        db_table = 'fitx_progress_photos'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.angle}"


class GoalMilestone(models.Model):
    MILESTONE_TYPES = [
        ('weight', 'Weight Goal'), ('workout', 'Workout Count'),
        ('streak', 'Streak'), ('custom', 'Custom Goal'),
    ]
    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='milestones')
    milestone_type = models.CharField(max_length=20, choices=MILESTONE_TYPES)
    title         = models.CharField(max_length=200)
    target_value  = models.FloatField()
    current_value = models.FloatField(default=0)
    achieved      = models.BooleanField(default=False)
    achieved_at   = models.DateTimeField(null=True, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_goal_milestones'

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.progress_percentage}%)"

    @property
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        return min(100, round(self.current_value / self.target_value * 100, 1))
