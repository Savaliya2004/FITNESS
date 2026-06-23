from django.db import models
from django.conf import settings


class FitnessCenter(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100, db_index=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    phone = models.CharField(max_length=15)
    amenities = models.JSONField(default=list)
    images = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    opening_time = models.TimeField(default='05:00')
    closing_time = models.TimeField(default='23:00')

    class Meta:
        db_table = 'fitx_centers'
        indexes = [models.Index(fields=['city', 'is_active'])]

    def __str__(self):
        return f"{self.name} - {self.city}"


class ClassType(models.Model):
    """Defines a type of class (e.g., 'Power Yoga', 'HIIT Burn')."""
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(default=60)
    calories_burn_estimate = models.PositiveIntegerField(default=300)
    difficulty = models.CharField(max_length=20)
    image = models.ImageField(upload_to='class_types/', null=True, blank=True)
    equipment_needed = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'fitx_class_types'

    def __str__(self):
        return f"{self.name} ({self.category})"


class ClassSchedule(models.Model):
    """A specific scheduled class instance."""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE, related_name='schedules')
    trainer = models.ForeignKey(
        'workout.TrainerProfile', on_delete=models.CASCADE, related_name='scheduled_classes'
    )
    center = models.ForeignKey(FitnessCenter, on_delete=models.CASCADE, related_name='scheduled_classes')

    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    max_capacity = models.PositiveIntegerField(default=30)
    current_bookings = models.PositiveIntegerField(default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    is_online = models.BooleanField(default=False)
    meeting_url = models.URLField(blank=True)

    price_override = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'fitx_class_schedules'
        indexes = [
            models.Index(fields=['date', 'start_time', 'status']),
            models.Index(fields=['center', 'date']),
            models.Index(fields=['trainer', 'date']),
        ]
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.class_type.name} - {self.date} {self.start_time}"

    @property
    def available_seats(self):
        return max(0, self.max_capacity - self.current_bookings)

    @property
    def is_full(self):
        return self.current_bookings >= self.max_capacity


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('waitlisted', 'Waitlisted'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='bookings')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booked_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    waitlist_position = models.PositiveIntegerField(null=True, blank=True)

    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    payment_ref = models.ForeignKey(
        'store.Payment', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='bookings'
    )

    refund_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    cancellation_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'fitx_bookings'
        unique_together = ('user', 'class_schedule')
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['class_schedule', 'status']),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.class_schedule} ({self.status})"


class Waitlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='waitlist')
    position = models.PositiveIntegerField()
    joined_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    class Meta:
        db_table = 'fitx_waitlist'
        unique_together = ('user', 'class_schedule')
        ordering = ['position']

    def __str__(self):
        return f"#{self.position} - {self.user.username}"
