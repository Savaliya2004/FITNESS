"""
Custom middleware for role caching and rate limiting.
"""
import logging
from django.core.cache import cache
from django.http import JsonResponse

logger = logging.getLogger('fitx')


class RoleMiddleware:
    """
    Attaches active roles and permissions to request.user for
    easy access in views and templates.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                roles = list(
                    request.user.user_roles
                    .filter(is_active=True)
                    .values_list('role__name', flat=True)
                )
                request.user._cached_roles = set(roles)

                # Aggregate permissions from all active roles
                perms = {}
                for ur in request.user.user_roles.filter(is_active=True).select_related('role'):
                    if ur.role.permissions:
                        for key, val in ur.role.permissions.items():
                            if val:
                                perms[key] = True
                request.user._cached_permissions = perms

                # Convenience attributes
                request.user.has_role = lambda r: r in request.user._cached_roles
                request.user.has_perm_custom = lambda p: request.user._cached_permissions.get(p, False)
                request.user.is_trainer = 'trainer' in request.user._cached_roles
                request.user.is_nutritionist = 'nutritionist' in request.user._cached_roles
                request.user.is_admin_user = 'admin' in request.user._cached_roles or request.user.is_superuser
            except Exception:
                # Graceful fallback if role tables don't exist yet (during migrations)
                request.user._cached_roles = set()
                request.user._cached_permissions = {}
                request.user.has_role = lambda r: False
                request.user.has_perm_custom = lambda p: False
                request.user.is_trainer = False
                request.user.is_nutritionist = False
                request.user.is_admin_user = request.user.is_superuser

        return self.get_response(request)


class RateLimitMiddleware:
    """
    Global rate limiting middleware using Django's cache framework.
    Falls back gracefully if no cache backend is configured.
    """

    RATE_LIMITS = {
        '/accounts/login/': {'limit': 10, 'window': 900},
        '/accounts/verify-otp/': {'limit': 10, 'window': 300},
        '/accounts/signup/': {'limit': 5, 'window': 3600},
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self._get_client_ip(request)
        path = request.path

        for prefix, config in self.RATE_LIMITS.items():
            if path.startswith(prefix) and request.method == 'POST':
                try:
                    cache_key = f"ratelimit:{ip}:{prefix}"
                    hits = cache.get(cache_key, 0)

                    if hits >= config['limit']:
                        if request.headers.get('Accept', '').startswith('application/json'):
                            return JsonResponse(
                                {'error': 'Rate limit exceeded. Please try again later.'},
                                status=429
                            )
                        from django.contrib import messages
                        messages.error(request, '⏳ Too many attempts. Please try again later.')

                    cache.set(cache_key, hits + 1, timeout=config['window'])
                except Exception:
                    pass  # Don't block requests if cache is unavailable
                break

        return self.get_response(request)

    @staticmethod
    def _get_client_ip(request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
