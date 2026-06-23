"""
Management command: ensure_admin
Creates or updates the default FitX administrator account.
Run: python manage.py ensure_admin
"""
from django.core.management.base import BaseCommand
from django.conf import settings


ADMIN_EMAIL = 'maheksavaliya3004@gmail.com'
ADMIN_PASSWORD = 'Mahek@123'
ADMIN_USERNAME = 'MaHeK'


class Command(BaseCommand):
    help = 'Creates or updates the default FitX administrator account and assigns the admin role.'

    def handle(self, *args, **options):
        from account.models import FitnessProfile, Role, UserRole

        # ── Ensure admin Role exists ──────────────────────────────────────────
        role, _ = Role.objects.get_or_create(
            name='admin',
            defaults={
                'description': 'Full system administrator with all permissions.',
                'permissions': {
                    'can_manage_users': True,
                    'can_manage_content': True,
                    'can_view_revenue': True,
                    'can_manage_memberships': True,
                    'can_moderate_community': True,
                    'can_manage_challenges': True,
                    'can_manage_bookings': True,
                    'can_view_analytics': True,
                }
            }
        )
        self.stdout.write(self.style.SUCCESS(f'[OK] Role "admin" ready.'))

        # ── Create or update admin user ───────────────────────────────────────
        user, created = FitnessProfile.objects.get_or_create(
            email=ADMIN_EMAIL,
            defaults={
                'username': ADMIN_USERNAME,
                'is_staff': True,
                'is_superuser': True,
                'is_email_verified': True,
                'membership_type': 'elite',
            }
        )

        # Always ensure superuser/staff flags are set
        if not user.is_staff or not user.is_superuser or user.username != ADMIN_USERNAME:
            user.is_staff = True
            user.is_superuser = True
            user.username = ADMIN_USERNAME
            user.save(update_fields=['is_staff', 'is_superuser', 'username'])

        user.set_password(ADMIN_PASSWORD)
        user.save(update_fields=['password'])

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(
            f'[OK] {action} admin user: {user.username} ({user.email})'
        ))

        # ── Assign admin role ─────────────────────────────────────────────────
        UserRole.objects.get_or_create(
            user=user,
            role=role,
            defaults={'is_active': True}
        )
        self.stdout.write(self.style.SUCCESS(f'[OK] Admin role assigned.'))
        self.stdout.write(self.style.SUCCESS(
            f'\nFitX Admin ready!\n'
            f'   Email:    {ADMIN_EMAIL}\n'
            f'   Password: {ADMIN_PASSWORD}\n'
            f'   URL:      /accounts/admin-panel/\n'
        ))
