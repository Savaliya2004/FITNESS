"""
Global context processor — makes notification count, roles, and membership
available in ALL templates without passing in every view.
"""


def global_context(request):
    context = {}

    if request.user.is_authenticated:
        try:
            from notifications.models import Notification
            context['unread_notifications'] = (
                Notification.objects.filter(user=request.user, is_read=False).count()
            )
        except Exception:
            context['unread_notifications'] = 0

        context['user_roles'] = getattr(request.user, '_cached_roles', set())
        context['is_trainer'] = getattr(request.user, 'is_trainer', False)
        context['is_admin_user'] = getattr(request.user, 'is_admin_user', False)
        context['membership_active'] = getattr(request.user, 'is_membership_active', False)
        context['membership_type'] = request.user.membership_type

    return context
