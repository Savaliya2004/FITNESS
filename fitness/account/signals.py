"""Auto-trigger gamification on key user actions."""
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='diet.UserProgress')
def on_progress_logged(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user

    try:
        from gamification.engine import GamificationEngine
        GamificationEngine.update_streak(user)
        GamificationEngine.award_xp(user, 'progress_logged')

        if instance.workouts_done > 0:
            user.total_workouts_completed += instance.workouts_done
            user.save(update_fields=['total_workouts_completed'])
            GamificationEngine.award_xp(user, 'workout_completed', multiplier=instance.workouts_done)

        GamificationEngine.evaluate_badges(user)
    except Exception:
        pass  # Don't break progress logging if gamification tables don't exist yet
