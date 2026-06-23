"""
API Views for FitX Fitness Application
Provides REST API endpoints for Workouts, Diet Plans, and Memberships.
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes

from workout.models import WorkoutProgram, Exercise, Trainer
from diet.models import MealPlan, UserProgress
from store.models import MembershipPlan, Payment
from .serializers import (
    WorkoutProgramSerializer, ExerciseSerializer, TrainerSerializer,
    MealPlanSerializer, UserProgressSerializer,
    MembershipPlanSerializer, PaymentSerializer, UserSerializer
)
from account.models import FitnessProfile
from rest_framework.permissions import IsAdminUser

class UserListCreateAPI(generics.ListCreateAPIView):
    """GET/POST /api/users/"""
    queryset = FitnessProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


# ─── Workout API Views ───────────────────────────────────────────────────────

class WorkoutListAPI(generics.ListAPIView):
    """GET /api/workouts/ — list all workout programs"""
    queryset = WorkoutProgram.objects.all()
    serializer_class = WorkoutProgramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ExerciseListAPI(generics.ListAPIView):
    """GET /api/exercises/ — list all exercises, supports ?category= and ?type= filters"""
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Exercise.objects.all()
        category = self.request.GET.get('category')
        etype = self.request.GET.get('type')
        if category:
            qs = qs.filter(category=category)
        if etype:
            qs = qs.filter(exercise_type=etype)
        return qs


class ExerciseDetailAPI(generics.RetrieveAPIView):
    """GET /api/exercises/<id>/ — single exercise detail"""
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ─── Diet Plan API Views ──────────────────────────────────────────────────────

class MealPlanListCreateAPI(generics.ListCreateAPIView):
    """
    GET  /api/diet/   — list current user's meal plans
    POST /api/diet/   — create a new meal plan for current user
    """
    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealPlanDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/diet/<id>/"""
    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user)


class UserProgressListAPI(generics.ListCreateAPIView):
    """GET/POST /api/progress/"""
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─── Membership API Views ──────────────────────────────────────────────────────

class MembershipPlanListAPI(generics.ListCreateAPIView):
    """GET/POST /api/memberships/ — list and create available plans"""
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MyPaymentsAPI(generics.ListCreateAPIView):
    """GET /api/my-payments/ — list current user's payments & POST create"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─── API Root Info ────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def api_root(request):
    """API root — lists available endpoints."""
    return Response({
        'users': request.build_absolute_uri('/api/users/'),
        'workouts': request.build_absolute_uri('/api/workouts/'),
        'exercises': request.build_absolute_uri('/api/exercises/'),
        'diet_plans': request.build_absolute_uri('/api/diet/'),
        'progress': request.build_absolute_uri('/api/progress/'),
        'memberships': request.build_absolute_uri('/api/memberships/'),
        'my_payments': request.build_absolute_uri('/api/my-payments/'),
    })
