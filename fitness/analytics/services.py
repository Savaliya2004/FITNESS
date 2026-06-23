"""Analytics aggregation service for admin dashboard."""
from django.db.models import Sum, Count, Avg, Q, F
from django.db.models.functions import TruncDate, TruncWeek
from django.utils import timezone
from datetime import timedelta

from account.models import FitnessProfile


class AnalyticsService:

    @staticmethod
    def get_overview():
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        seven_days_ago = now - timedelta(days=7)

        total_users = FitnessProfile.objects.count()
        new_users_30d = FitnessProfile.objects.filter(date_joined__gte=thirty_days_ago).count()
        new_users_7d = FitnessProfile.objects.filter(date_joined__gte=seven_days_ago).count()
        active_users_7d = FitnessProfile.objects.filter(last_login__gte=seven_days_ago).count()

        # Revenue
        try:
            from store.models import Payment, Subscription
            total_revenue = Payment.objects.filter(
                status='success'
            ).aggregate(total=Sum('amount'))['total'] or 0
            revenue_30d = Payment.objects.filter(
                status='success', created_at__gte=thirty_days_ago
            ).aggregate(total=Sum('amount'))['total'] or 0
            active_subs = Subscription.objects.filter(status='active').count()
        except Exception:
            total_revenue = 0
            revenue_30d = 0
            active_subs = 0

        # Membership breakdown
        membership_dist = dict(
            FitnessProfile.objects.values_list('membership_type')
            .annotate(count=Count('id'))
            .values_list('membership_type', 'count')
        )

        # Bookings
        try:
            from booking.models import Booking
            total_bookings_30d = Booking.objects.filter(
                booked_at__gte=thirty_days_ago, status='confirmed'
            ).count()
        except Exception:
            total_bookings_30d = 0

        return {
            'total_users': total_users,
            'new_users_30d': new_users_30d,
            'new_users_7d': new_users_7d,
            'active_users_7d': active_users_7d,
            'dau_wau_ratio': round(active_users_7d / max(total_users, 1) * 100, 1),
            'total_revenue': float(total_revenue),
            'revenue_30d': float(revenue_30d),
            'membership_distribution': membership_dist,
            'active_subscriptions': active_subs,
            'bookings_30d': total_bookings_30d,
        }

    @staticmethod
    def get_revenue_chart(days=30):
        try:
            from store.models import Payment
            since = timezone.now() - timedelta(days=days)
            return list(
                Payment.objects.filter(
                    status='success', created_at__gte=since
                ).annotate(
                    day=TruncDate('created_at')
                ).values('day').annotate(
                    revenue=Sum('amount'), count=Count('id')
                ).order_by('day')
            )
        except Exception:
            return []

    @staticmethod
    def get_user_growth_chart(days=90):
        since = timezone.now() - timedelta(days=days)
        return list(
            FitnessProfile.objects.filter(
                date_joined__gte=since
            ).annotate(
                week=TruncWeek('date_joined')
            ).values('week').annotate(
                signups=Count('id')
            ).order_by('week')
        )
