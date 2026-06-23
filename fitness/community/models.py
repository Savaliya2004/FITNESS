from django.db import models
from django.conf import settings


class UserFollow(models.Model):
    """User-to-user follow relationship."""
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_follows'
        unique_together = ('follower', 'following')
        indexes = [
            models.Index(fields=['follower', '-created_at']),
            models.Index(fields=['following', '-created_at']),
        ]

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.follower == self.following:
            raise ValidationError("Users cannot follow themselves.")


class CommunityPost(models.Model):
    """User-generated content: progress updates, questions, tips."""
    POST_TYPES = [
        ('progress', 'Progress Update'),
        ('question', 'Question'),
        ('tip', 'Fitness Tip'),
        ('achievement', 'Achievement'),
        ('discussion', 'Discussion'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_posts'
    )
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='discussion')
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='community/posts/', null=True, blank=True)

    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    is_pinned = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fitx_community_posts'
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['post_type', '-created_at']),
        ]

    def __str__(self):
        return f"{self.author.username}: {self.title or self.content[:50]}"


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_post_likes'
        unique_together = ('user', 'post')


class Comment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )
    likes_count = models.PositiveIntegerField(default=0)
    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} on {self.post}"


class FitnessGroup(models.Model):
    """Groups for specific interests: 'Keto Warriors', '5AM Club', etc."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='community/groups/', null=True, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='GroupMembership', related_name='fitness_groups'
    )
    is_private = models.BooleanField(default=False)
    max_members = models.PositiveIntegerField(default=500)
    members_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_groups'

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    ROLE_CHOICES = [('member', 'Member'), ('moderator', 'Moderator'), ('admin', 'Admin')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(FitnessGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_group_memberships'
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


class ActivityFeedItem(models.Model):
    """Denormalized activity feed for fast retrieval."""
    ACTIVITY_TYPES = [
        ('workout_completed', 'Completed a Workout'),
        ('badge_earned', 'Earned a Badge'),
        ('streak_milestone', 'Streak Milestone'),
        ('post_created', 'Created a Post'),
        ('challenge_joined', 'Joined a Challenge'),
        ('progress_logged', 'Logged Progress'),
        ('class_attended', 'Attended a Class'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities'
    )
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_activity_feed'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.title}"
