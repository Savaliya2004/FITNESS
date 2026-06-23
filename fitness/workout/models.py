from django.db import models
from django.conf import settings


class Trainer(models.Model):
    """Legacy compatible trainer model."""
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    bio = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    profile_image = models.ImageField(upload_to='trainers/', null=True, blank=True)

    def __str__(self):
        return self.name


class TrainerProfile(models.Model):
    """
    Extended trainer profile linked to a FitnessProfile user account.
    Trainers are users WITH the 'trainer' role.
    """
    SPECIALIZATIONS = [
        ('strength', 'Strength Training'),
        ('yoga', 'Yoga'),
        ('cardio', 'Cardio/HIIT'),
        ('pilates', 'Pilates'),
        ('crossfit', 'CrossFit'),
        ('martial_arts', 'Martial Arts'),
        ('dance', 'Dance Fitness'),
        ('nutrition', 'Nutrition Coaching'),
    ]
    VERIFICATION_STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trainer_profile'
    )
    display_name = models.CharField(max_length=100)
    specializations = models.JSONField(default=list)
    experience_years = models.PositiveIntegerField(default=0)
    certifications = models.JSONField(default=list)

    bio = models.TextField(max_length=1000)
    profile_image = models.ImageField(upload_to='trainers/', null=True, blank=True)
    intro_video_url = models.URLField(blank=True)

    # Ratings (denormalized)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    total_reviews = models.PositiveIntegerField(default=0)
    total_sessions_conducted = models.PositiveIntegerField(default=0)

    # Availability
    is_available = models.BooleanField(default=True)
    max_daily_sessions = models.PositiveIntegerField(default=8)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # Verification
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    verified_at = models.DateTimeField(null=True, blank=True)

    # Earnings
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pending_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'fitx_trainer_profiles'
        indexes = [
            models.Index(fields=['verification_status', 'is_available']),
            models.Index(fields=['average_rating']),
        ]

    def __str__(self):
        return self.display_name


class TrainerAvailability(models.Model):
    """Weekly recurring availability slots for trainers."""
    DAYS = [(i, d) for i, d in enumerate([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'
    ])]

    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'fitx_trainer_availability'
        unique_together = ('trainer', 'day_of_week', 'start_time')

    def __str__(self):
        return f"{self.trainer.display_name} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class WorkoutProgram(models.Model):
    CATEGORIES = [
        ('strength', 'Strength'),
        ('yoga', 'Yoga'),
        ('cardio', 'Cardio'),
        ('hiit', 'HIIT'),
        ('pilates', 'Pilates'),
    ]
    DIFFICULTIES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORIES)
    duration_weeks = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTIES)
    image = models.ImageField(upload_to='workouts/', null=True, blank=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='programs', null=True, blank=True)

    def __str__(self):
        return self.title


class Exercise(models.Model):
    EXERCISE_CATEGORIES = [
        ('strength', 'Strength Training'),
        ('cardio', 'Cardio'),
        ('hiit', 'HIIT'),
        ('yoga', 'Yoga'),
        ('home', 'Home Workout'),
        ('flexibility', 'Flexibility and mobility'),
    ]

    EXERCISE_TYPES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('core', 'Core'),
        ('fullbody', 'Full Body'),
        ('basics', 'Bodyweight Basics'),
        ('cardio', 'Cardio Blast'),
        ('all', 'All Levels'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=EXERCISE_CATEGORIES)
    exercise_type = models.CharField(max_length=50, choices=EXERCISE_TYPES)
    difficulty = models.CharField(max_length=50)
    reps_sets = models.CharField(max_length=100)
    calories_burned = models.PositiveIntegerField()
    video_url = models.URLField(blank=True, null=True, help_text="YouTube Embed URL")
    image_url = models.URLField(blank=True, null=True, help_text="Unsplash URL for placeholder")

    steps = models.TextField(help_text="Separate steps with newlines")
    benefits = models.TextField(help_text="Separate benefits with newlines")
    mistakes = models.TextField(help_text="Separate mistakes with newlines")

    def __str__(self):
        return f"{self.name} ({self.category} - {self.exercise_type})"


class UserRoutine(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='routines')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'exercise')

    def __str__(self):
        return f"{self.user.username}'s Routine: {self.exercise.name}"
