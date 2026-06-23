from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'fitx_blog_categories'
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name


class BlogTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'fitx_blog_tags'

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(BlogTag, blank=True)

    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Engagement
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)

    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fitx_blog_posts'
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt and self.content:
            self.excerpt = self.content[:497] + '...'
        super().save(*args, **kwargs)


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_blog_comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Challenge(models.Model):
    """Multi-day fitness challenges with daily tasks and progress tracking."""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField(blank=True)

    start_date = models.DateField()
    end_date = models.DateField()

    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')

    reward = models.CharField(max_length=200, blank=True)
    reward_xp = models.PositiveIntegerField(default=100)

    image = models.ImageField(upload_to='challenges/', null=True, blank=True)
    max_participants = models.PositiveIntegerField(default=0)  # 0 = unlimited
    current_participants = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='created_challenges'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'fitx_challenges'
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def is_joinable(self):
        from django.utils import timezone
        today = timezone.now().date()
        if self.status not in ('upcoming', 'active'):
            return False
        if today > self.end_date:
            return False
        if self.max_participants and self.current_participants >= self.max_participants:
            return False
        return True


class ChallengeTask(models.Model):
    """Daily tasks within a challenge."""
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='tasks')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_value = models.FloatField(default=1)
    target_unit = models.CharField(max_length=20, default='reps')

    class Meta:
        db_table = 'fitx_challenge_tasks'
        ordering = ['day_number']
        unique_together = ('challenge', 'day_number')

    def __str__(self):
        return f"Day {self.day_number}: {self.title}"


class ChallengeEnrollment(models.Model):
    """Tracks user's participation in a challenge."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped Out'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='challenge_enrollments')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    days_completed = models.PositiveIntegerField(default=0)
    total_days = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'fitx_challenge_enrollments'
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.username} in {self.challenge.title}"


class ChallengeProgress(models.Model):
    """Daily progress within a challenge."""
    enrollment = models.ForeignKey(ChallengeEnrollment, on_delete=models.CASCADE, related_name='daily_progress')
    task = models.ForeignKey(ChallengeTask, on_delete=models.CASCADE)
    completed_value = models.FloatField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'fitx_challenge_progress'
        unique_together = ('enrollment', 'task')

    def __str__(self):
        return f"{self.enrollment.user.username} - {self.task.title}"


class Testimonial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.user.username}"


class SuccessStory(models.Model):
    name = models.CharField(max_length=100)
    result_stat = models.CharField(max_length=100)
    image = models.ImageField(upload_to='stories/', null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    before_image = models.ImageField(upload_to='stories/before/', null=True, blank=True)
    after_image = models.ImageField(upload_to='stories/after/', null=True, blank=True)
    brief = models.TextField()
    full_story = models.TextField(blank=True, default='')
    is_gain = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    topic = models.CharField(max_length=100)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.topic}"
