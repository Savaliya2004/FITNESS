import hashlib
import secrets
import uuid
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class FitnessProfile(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('N', 'Prefer not to say'),
    ]
    FITNESS_GOALS = [
        ('muscle_gain', 'Muscle Gain'),
        ('fat_loss', 'Fat Loss'),
        ('weight_loss', 'Weight Loss'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
        ('maintenance', 'Maintenance'),
        ('general_fitness', 'General Fitness'),
    ]
    MEMBERSHIP_TYPES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('elite', 'Elite'),
    ]
    ACTIVITY_LEVELS = [
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly Active'),
        ('moderate', 'Moderately Active'),
        ('active', 'Very Active'),
        ('extreme', 'Extremely Active'),
    ]

    # === Core Info ===
    phone = models.CharField(max_length=15, blank=True, db_index=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    # === Body Metrics ===
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight = models.FloatField(null=True, blank=True, help_text="Current Weight in kg")
    target_weight = models.FloatField(null=True, blank=True)
    body_fat_percentage = models.FloatField(null=True, blank=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVELS, default='moderate')

    # === Fitness Config ===
    fitness_goal = models.CharField(max_length=50, choices=FITNESS_GOALS, default='general_fitness')
    dietary_preference = models.CharField(max_length=30, blank=True)
    allergies = models.TextField(blank=True, help_text="Comma-separated allergens")
    medical_conditions = models.TextField(blank=True)

    # === Membership ===
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES, default='free')
    membership_expires_at = models.DateTimeField(null=True, blank=True)

    # === Profile ===
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    # === Location ===
    city = models.CharField(max_length=100, blank=True)

    # === Emergency ===
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)

    # === Gamification ===
    xp_points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    total_workouts_completed = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)

    # === Referrals ===
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='referrals'
    )

    class Meta:
        db_table = 'fitx_users'
        indexes = [
            models.Index(fields=['membership_type', 'membership_expires_at']),
            models.Index(fields=['city']),
            models.Index(fields=['fitness_goal']),
        ]

    def __str__(self):
        return self.username

    @property
    def bmi(self):
        if self.height and self.weight:
            h_m = self.height / 100
            return round(self.weight / (h_m * h_m), 1)
        return None

    @property
    def is_membership_active(self):
        if self.membership_type == 'free':
            return True
        if self.membership_expires_at:
            return self.membership_expires_at > timezone.now()
        return False

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)


class Role(models.Model):
    """Defines available roles in the system."""
    ROLE_CHOICES = [
        ('user', 'Regular User'),
        ('trainer', 'Trainer'),
        ('nutritionist', 'Nutritionist'),
        ('admin', 'Administrator'),
        ('support', 'Support Staff'),
        ('content_manager', 'Content Manager'),
    ]

    name = models.CharField(max_length=30, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=dict, help_text="Granular permissions map")

    class Meta:
        db_table = 'fitx_roles'

    def __str__(self):
        return self.get_name_display()


class UserRole(models.Model):
    """M2M through table: assigns roles to users with multi-role support."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_roles'
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='roles_assigned'
    )

    class Meta:
        db_table = 'fitx_user_roles'
        unique_together = ('user', 'role')
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.role.name}"


class OTPVerification(models.Model):
    """Secure OTP with hashing, expiry, and attempt limiting."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp_hash = models.CharField(max_length=64, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.PositiveIntegerField(default=0)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'fitx_otp'

    def __str__(self):
        return f"OTP for {self.user.email}"

    @staticmethod
    def generate_otp():
        """Generate a cryptographically secure 6-digit OTP."""
        return f"{secrets.randbelow(900000) + 100000}"

    @staticmethod
    def hash_otp(otp):
        return hashlib.sha256(otp.encode()).hexdigest()

    def verify(self, otp_input):
        """Verify OTP with expiry and attempt limits."""
        if self.is_used:
            return False, "OTP already used."
        if self.attempts >= 3:
            return False, "Too many attempts. Request a new OTP."
        if timezone.now() - self.created_at > timedelta(minutes=5):
            return False, "OTP expired."

        self.attempts += 1
        self.save(update_fields=['attempts'])

        if self.otp_hash == self.hash_otp(otp_input):
            self.is_used = True
            self.save(update_fields=['is_used'])
            return True, "Verified."
        return False, "Invalid OTP."
