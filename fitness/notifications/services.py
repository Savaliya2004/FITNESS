"""
NotificationService — central dispatcher for all notifications.
"""


class NotificationService:
    TEMPLATES = {
        'booking_confirmed': {
            'title': '✅ Booking Confirmed — {class_name}',
            'body': 'Your spot in {class_name} on {date} at {time} is confirmed!',
        },
        'booking_cancelled': {
            'title': '❌ Booking Cancelled',
            'body': 'Your booking for {class_name} has been cancelled.',
        },
        'booking_reminder': {
            'title': '⏰ Class Reminder — {class_name}',
            'body': 'Your {class_name} class starts in {minutes} minutes!',
        },
        'payment_success': {
            'title': '💳 Payment Successful',
            'body': '₹{amount} payment for {plan_name} membership received.',
        },
        'subscription_expiring': {
            'title': '⚠️ Membership Expiring Soon',
            'body': 'Your {plan_name} membership expires on {date}. Renew now!',
        },
        'badge_earned': {
            'title': '🏆 New Badge Earned!',
            'body': 'You earned the "{badge_name}" badge! +{xp} XP',
        },
        'streak_milestone': {
            'title': '🔥 Streak Milestone!',
            'body': '{streak_days}-day streak! Keep going!',
        },
        'system': {
            'title': '{title}',
            'body': '{body}',
        },
    }

    @classmethod
    def send(cls, user, notification_type, context_data=None):
        """
        Create in-app notification.
        Email dispatch can be added via Celery tasks later.
        """
        context_data = context_data or {}
        template = cls.TEMPLATES.get(notification_type, cls.TEMPLATES['system'])

        try:
            title = template.get('title', 'Notification').format(**context_data)
        except KeyError:
            title = template.get('title', 'Notification')

        try:
            body = template.get('body', '').format(**context_data)
        except KeyError:
            body = template.get('body', '')

        from .models import Notification
        notification = Notification.objects.create(
            user=user,
            type=notification_type,
            title=title,
            body=body,
            data=context_data,
        )

        return notification
