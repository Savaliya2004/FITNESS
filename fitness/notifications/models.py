from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPES = [
        ('booking_confirmed', 'Booking Confirmed'),
        ('booking_cancelled', 'Booking Cancelled'),
        ('booking_reminder', 'Class Reminder'),
        ('payment_success', 'Payment Successful'),
        ('payment_failed', 'Payment Failed'),
        ('subscription_expiring', 'Subscription Expiring'),
        ('subscription_expired', 'Subscription Expired'),
        ('streak_milestone', 'Streak Milestone'),
        ('badge_earned', 'Badge Earned'),
        ('trainer_message', 'Trainer Message'),
        ('system', 'System Notification'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=30, choices=TYPES)
    title = models.CharField(max_length=200)
    body = models.TextField()
    data = models.JSONField(default=dict)

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.title}"


class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_prefs')

    email_booking = models.BooleanField(default=True)
    email_payment = models.BooleanField(default=True)
    email_reminder = models.BooleanField(default=True)
    email_marketing = models.BooleanField(default=False)

    push_booking = models.BooleanField(default=True)
    push_reminder = models.BooleanField(default=True)
    push_streak = models.BooleanField(default=True)

    reminder_minutes_before = models.PositiveIntegerField(default=30)

    class Meta:
        db_table = 'fitx_notification_prefs'

    def __str__(self):
        return f"Prefs for {self.user.username}"
