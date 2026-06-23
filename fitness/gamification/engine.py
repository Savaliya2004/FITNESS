"""
Gamification engine — XP, badges, levels, streaks.
"""
from datetime import timedelta
from django.utils import timezone

from .models import Badge, UserBadge


class GamificationEngine:
    XP_REWARDS = {
        'workout_completed': 50,
        'class_attended': 75,
        'progress_logged': 25,
        'streak_day': 10,
        'post_created': 15,
        'review_written': 20,
        'challenge_completed': 200,
        'referral_signup': 100,
    }

    LEVEL_THRESHOLDS = [
        (0, 1, 'Beginner'),
        (100, 2, 'Starter'),
        (300, 3, 'Regular'),
        (600, 4, 'Active'),
        (1000, 5, 'Committed'),
        (1500, 6, 'Dedicated'),
        (2500, 7, 'Warrior'),
        (4000, 8, 'Champion'),
        (6000, 9, 'Legend'),
        (10000, 10, 'FitX Master'),
    ]

    @classmethod
    def award_xp(cls, user, action, multiplier=1):
        base_xp = cls.XP_REWARDS.get(action, 0)
        xp = base_xp * multiplier

        user.xp_points += xp
        old_level = user.level

        new_level = 1
        for threshold, level, _ in cls.LEVEL_THRESHOLDS:
            if user.xp_points >= threshold:
                new_level = level

        user.level = new_level
        user.save(update_fields=['xp_points', 'level'])

        leveled_up = new_level > old_level
        if leveled_up:
            level_name = next(
                (name for t, l, name in cls.LEVEL_THRESHOLDS if l == new_level),
                'Unknown'
            )
            try:
                from notifications.services import NotificationService
                NotificationService.send(user, 'badge_earned', {
                    'badge_name': f'Level {new_level}: {level_name}',
                    'xp': xp,
                })
            except Exception:
                pass

        return xp, new_level if leveled_up else None

    @classmethod
    def evaluate_badges(cls, user):
        already_earned = set(
            UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
        )
        all_badges = Badge.objects.exclude(id__in=already_earned)
        newly_earned = []

        for badge in all_badges:
            if cls._check_criteria(user, badge.criteria):
                UserBadge.objects.create(user=user, badge=badge)
                user.xp_points += badge.xp_reward
                newly_earned.append(badge)

                try:
                    from notifications.services import NotificationService
                    NotificationService.send(user, 'badge_earned', {
                        'badge_name': badge.name,
                        'xp': badge.xp_reward,
                    })
                except Exception:
                    pass

        if newly_earned:
            user.save(update_fields=['xp_points'])

        return newly_earned

    @classmethod
    def _check_criteria(cls, user, criteria):
        if not criteria:
            return False
        ctype = criteria.get('type')
        value = criteria.get('value', 0)

        if ctype == 'streak':
            return user.longest_streak >= value
        elif ctype == 'workouts_completed':
            return user.total_workouts_completed >= value
        elif ctype == 'calories_burned':
            from django.db.models import Sum
            from diet.models import UserProgress
            total = UserProgress.objects.filter(user=user).aggregate(
                total=Sum('calories_burned')
            )['total'] or 0
            return total >= value
        elif ctype == 'level':
            return user.level >= value
        elif ctype == 'classes_attended':
            try:
                from booking.models import Booking
                return Booking.objects.filter(user=user, status='attended').count() >= value
            except Exception:
                return False
        elif ctype == 'posts_created':
            try:
                from community.models import CommunityPost
                return CommunityPost.objects.filter(author=user).count() >= value
            except Exception:
                return False
        elif ctype == 'referrals':
            return user.referrals.count() >= value

        return False

    @classmethod
    def update_streak(cls, user):
        from diet.models import UserProgress
        from datetime import date
        today = date.today()

        yesterday_log = UserProgress.objects.filter(
            user=user, date=today - timedelta(days=1)
        ).exists()

        today_log = UserProgress.objects.filter(user=user, date=today).first()

        if today_log:
            if yesterday_log:
                yesterday = UserProgress.objects.filter(
                    user=user, date=today - timedelta(days=1)
                ).first()
                today_log.streak = (yesterday.streak if yesterday else 0) + 1
            else:
                today_log.streak = 1

            today_log.save(update_fields=['streak'])

            if today_log.streak > user.longest_streak:
                user.longest_streak = today_log.streak
                user.save(update_fields=['longest_streak'])

            cls.award_xp(user, 'streak_day')

            milestones = [7, 14, 30, 60, 100, 200, 365]
            if today_log.streak in milestones:
                try:
                    from notifications.services import NotificationService
                    NotificationService.send(user, 'streak_milestone', {
                        'streak_days': today_log.streak,
                    })
                except Exception:
                    pass

        return today_log
