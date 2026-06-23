from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    """Chat room between two users (trainer ↔ user) or support tickets."""
    ROOM_TYPES = [
        ('trainer_user', 'Trainer-User Chat'),
        ('support', 'Support Ticket'),
        ('group', 'Group Chat'),
    ]

    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='trainer_user')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')
    name = models.CharField(max_length=200, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_message_text = models.CharField(max_length=200, blank=True)
    last_message_at = models.DateTimeField(null=True, blank=True)
    last_message_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    class Meta:
        db_table = 'fitx_chat_rooms'
        ordering = ['-last_message_at']

    def __str__(self):
        return self.name or f"Chat Room #{self.id}"


class ChatMessage(models.Model):
    """Individual message within a chat room."""
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
        ('system', 'System Message'),
    ]

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    content = models.TextField()
    file = models.FileField(upload_to='chat/files/', null=True, blank=True)

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitx_chat_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['room', 'created_at']),
        ]

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"


class SupportTicket(models.Model):
    """Support ticket linked to a chat room."""
    PRIORITY_CHOICES = [
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'), ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'), ('closed', 'Closed'),
    ]
    CATEGORIES = [
        ('billing', 'Billing Issue'),
        ('booking', 'Booking Issue'),
        ('technical', 'Technical Problem'),
        ('trainer', 'Trainer Complaint'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='support_tickets')
    chat_room = models.OneToOneField(ChatRoom, on_delete=models.CASCADE, related_name='ticket')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='assigned_tickets'
    )

    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='other')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'fitx_support_tickets'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'priority', '-created_at']),
        ]

    def __str__(self):
        return f"Ticket: {self.subject} ({self.status})"
