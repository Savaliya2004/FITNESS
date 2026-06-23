from django.db import models
from django.conf import settings


class Badge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', null=True, blank=True)
    category = models.CharField(max_length=50)
    xp_reward = models.PositiveIntegerField(default=50)
    criteria = models.JSONField(help_text='Example: {"type": "streak", "value": 7}')

    class Meta:
        db_table = 'fitx_badges'

    def __str__(self):
        return f"🏆 {self.name}"


class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_user_badges'
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} earned {self.badge.name}"


class Leaderboard(models.Model):
    PERIOD_CHOICES = [('weekly', 'Weekly'), ('monthly', 'Monthly'), ('all_time', 'All Time')]
    METRIC_CHOICES = [
        ('xp', 'XP Points'),
        ('workouts', 'Workouts Completed'),
        ('calories', 'Calories Burned'),
        ('streak', 'Longest Streak'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    metric = models.CharField(max_length=20, choices=METRIC_CHOICES)
    value = models.FloatField(default=0)
    rank = models.PositiveIntegerField()
    computed_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fitx_leaderboard'
        indexes = [
            models.Index(fields=['period', 'metric', 'rank']),
        ]
        unique_together = ('user', 'period', 'metric')

    def __str__(self):
        return f"#{self.rank} {self.user.username} ({self.metric} - {self.period})"
