"""Template tags for role-based rendering in templates."""
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def has_role(context, role_name):
    """
    Usage:
        {% load role_tags %}
        {% has_role 'admin' as is_admin %}
        {% if is_admin %}...{% endif %}
    """
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False
    roles = getattr(request.user, '_cached_roles', set())
    return role_name in roles


@register.filter
def can_access(user, minimum_membership):
    """Usage: {% if user|can_access:"premium" %}...{% endif %}"""
    hierarchy = {'free': 0, 'premium': 1, 'elite': 2}
    user_level = hierarchy.get(getattr(user, 'membership_type', 'free'), 0)
    required_level = hierarchy.get(minimum_membership, 1)
    return user_level >= required_level
