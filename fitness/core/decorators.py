"""
Decorators for restricting access based on roles and membership status.
Replaces all hardcoded email checks.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*required_roles):
    """
    Decorator that checks if user has ANY of the specified roles.

    Usage:
        @role_required('admin')
        @role_required('trainer', 'admin')
        @role_required('nutritionist', 'trainer', 'admin')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, '🔐 Please login first.')
                return redirect('login')

            # Specific Admin Rule: Only this email or username can ever have the 'admin' role
            if 'admin' in required_roles:
                if request.user.email != 'maheksavaliya3004@gmail.com' and request.user.username != 'MaHeK':
                    messages.error(request, '⛔ You do not have permission to access the admin dashboard.')
                    return redirect('dashboard')
                return view_func(request, *args, **kwargs)

            # Superuser bypasses all role checks
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_roles = set(
                request.user.user_roles
                .filter(is_active=True)
                .values_list('role__name', flat=True)
            )

            if not user_roles.intersection(set(required_roles)):
                messages.error(request, '⛔ You do not have permission to access this page.')
                return redirect('dashboard')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def permission_required(permission_name):
    """
    Checks a specific granular permission from the user's role(s).

    Usage:
        @permission_required('can_manage_users')
        @permission_required('can_view_revenue')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            active_roles = request.user.user_roles.filter(
                is_active=True
            ).select_related('role')

            has_perm = any(
                ur.role.permissions.get(permission_name, False)
                for ur in active_roles
            )

            if not has_perm:
                messages.error(request, '⛔ Insufficient permissions.')
                return redirect('dashboard')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def membership_required(membership_type=None):
    """
    Decorator to restrict view access based on membership type.

    Usage:
        @membership_required()           # Requires any paid membership
        @membership_required('premium')  # Requires premium or higher
        @membership_required('elite')    # Requires elite membership
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, '🔐 Please login first to access this feature.')
                return redirect('login')

            user_membership = request.user.membership_type

            if membership_type is None:
                if user_membership == 'free':
                    messages.info(request, '💳 Upgrade your membership to unlock premium features!')
                    return redirect('/#membership-plans')
                return view_func(request, *args, **kwargs)

            membership_hierarchy = {'free': 0, 'premium': 1, 'elite': 2}
            user_level = membership_hierarchy.get(user_membership, 0)
            required_level = membership_hierarchy.get(membership_type, 1)

            if user_level < required_level:
                messages.warning(request, f'⚠️ This feature requires {membership_type.upper()} membership. Upgrade now!')
                return redirect('/#membership-plans')

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
