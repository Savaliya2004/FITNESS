"""
URL configuration for fitness project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from fitness import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('account.urls')),
    path('training/', include('workout.urls')),
    path('nutrition/', include('diet.urls')),
    path('shop/', include('store.urls')),
    path('classes/', include('booking.urls')),
    path('community/', include('community.urls')),
    path('chat/', include('chat.urls')),
    path('coach/', include('ai_coach.urls')),
    
    # Allauth URLs
    path('accounts/', include('allauth.urls')),

    # ─── REST API endpoints ───────────────────────────────────────────────────
    path('api/', api_views.api_root, name='api_root'),
    path('api/users/', api_views.UserListCreateAPI.as_view(), name='api_users'),
    path('api/workouts/', api_views.WorkoutListAPI.as_view(), name='api_workouts'),
    path('api/exercises/', api_views.ExerciseListAPI.as_view(), name='api_exercises'),
    path('api/exercises/<int:pk>/', api_views.ExerciseDetailAPI.as_view(), name='api_exercise_detail'),
    path('api/diet/', api_views.MealPlanListCreateAPI.as_view(), name='api_diet'),
    path('api/diet/<int:pk>/', api_views.MealPlanDetailAPI.as_view(), name='api_diet_detail'),
    path('api/progress/', api_views.UserProgressListAPI.as_view(), name='api_progress'),
    path('api/memberships/', api_views.MembershipPlanListAPI.as_view(), name='api_memberships'),
    path('api/my-payments/', api_views.MyPaymentsAPI.as_view(), name='api_my_payments'),

    # ─── Webhooks ────────────────────────────────────────────────────────────
    path('webhooks/razorpay/', include([
        path('', __import__('store.webhooks', fromlist=['razorpay_webhook']).razorpay_webhook, name='razorpay_webhook'),
    ])),

    # ─── DRF Browsable API auth ───────────────────────────────────────────────
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
