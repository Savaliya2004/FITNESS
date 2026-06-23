"""Input validators for security."""
import re
from django.core.exceptions import ValidationError


def validate_phone(value):
    if not re.match(r'^\+?[1-9]\d{7,14}$', value):
        raise ValidationError('Enter a valid phone number.')


def validate_no_script(value):
    """Prevent XSS in text fields."""
    dangerous = ['<script', 'javascript:', 'onerror=', 'onload=', 'onclick=']
    lower = value.lower()
    for d in dangerous:
        if d in lower:
            raise ValidationError('Input contains potentially unsafe content.')


def validate_image_size(image):
    """Limit upload size to 5MB."""
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError('Image file too large. Maximum size is 5MB.')
