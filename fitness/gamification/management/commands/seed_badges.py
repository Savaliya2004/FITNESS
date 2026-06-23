"""Seed badge definitions."""
from django.core.management.base import BaseCommand
from gamification.models import Badge


class Command(BaseCommand):
    help = 'Seed initial badge definitions'

    def handle(self, *args, **options):
        badges = [
            {'name': 'Week Warrior', 'description': '7-day workout streak',
             'category': 'streak', 'xp_reward': 100, 'criteria': {'type': 'streak', 'value': 7}},
            {'name': 'Fortnight Fighter', 'description': '14-day workout streak',
             'category': 'streak', 'xp_reward': 200, 'criteria': {'type': 'streak', 'value': 14}},
            {'name': 'Monthly Machine', 'description': '30-day workout streak',
             'category': 'streak', 'xp_reward': 500, 'criteria': {'type': 'streak', 'value': 30}},
            {'name': 'Century Slayer', 'description': '100-day workout streak',
             'category': 'streak', 'xp_reward': 2000, 'criteria': {'type': 'streak', 'value': 100}},
            {'name': 'First Steps', 'description': 'Complete your first workout',
             'category': 'workout', 'xp_reward': 25, 'criteria': {'type': 'workouts_completed', 'value': 1}},
            {'name': 'Getting Serious', 'description': 'Complete 10 workouts',
             'category': 'workout', 'xp_reward': 100, 'criteria': {'type': 'workouts_completed', 'value': 10}},
            {'name': 'Half Century', 'description': 'Complete 50 workouts',
             'category': 'workout', 'xp_reward': 300, 'criteria': {'type': 'workouts_completed', 'value': 50}},
            {'name': 'Iron Will', 'description': 'Complete 100 workouts',
             'category': 'workout', 'xp_reward': 500, 'criteria': {'type': 'workouts_completed', 'value': 100}},
            {'name': 'Calorie Crusher', 'description': 'Burn 10,000 total calories',
             'category': 'milestone', 'xp_reward': 200, 'criteria': {'type': 'calories_burned', 'value': 10000}},
            {'name': 'Inferno', 'description': 'Burn 50,000 total calories',
             'category': 'milestone', 'xp_reward': 1000, 'criteria': {'type': 'calories_burned', 'value': 50000}},
            {'name': 'Community Builder', 'description': 'Create 5 community posts',
             'category': 'social', 'xp_reward': 75, 'criteria': {'type': 'posts_created', 'value': 5}},
            {'name': 'Influencer', 'description': 'Refer 5 friends who sign up',
             'category': 'social', 'xp_reward': 500, 'criteria': {'type': 'referrals', 'value': 5}},
            {'name': 'Rising Star', 'description': 'Reach Level 5',
             'category': 'level', 'xp_reward': 150, 'criteria': {'type': 'level', 'value': 5}},
            {'name': 'Elite Athlete', 'description': 'Reach Level 10',
             'category': 'level', 'xp_reward': 1000, 'criteria': {'type': 'level', 'value': 10}},
        ]

        created = 0
        for b in badges:
            _, was_created = Badge.objects.get_or_create(name=b['name'], defaults=b)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'[SUCCESS] Seeded {created} new badges'))
