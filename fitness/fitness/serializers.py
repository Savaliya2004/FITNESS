from rest_framework import serializers
from workout.models import WorkoutProgram, Exercise, Trainer
from diet.models import MealPlan, UserProgress
from store.models import MembershipPlan, Payment
from account.models import FitnessProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessProfile
        fields = ['id', 'username', 'email', 'membership_type', 'fitness_goal', 'is_staff']


# ─── Workout Serializers ──────────────────────────────────────────────────────

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ['id', 'name', 'specialty', 'bio', 'rating']


class WorkoutProgramSerializer(serializers.ModelSerializer):
    trainer_name = serializers.SerializerMethodField()

    class Meta:
        model = WorkoutProgram
        fields = ['id', 'title', 'description', 'category', 'duration_weeks', 'difficulty', 'trainer_name']

    def get_trainer_name(self, obj):
        return obj.trainer.name if obj.trainer else None


class ExerciseSerializer(serializers.ModelSerializer):
    steps_list = serializers.SerializerMethodField()
    benefits_list = serializers.SerializerMethodField()
    mistakes_list = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = [
            'id', 'name', 'category', 'exercise_type', 'difficulty',
            'reps_sets', 'calories_burned', 'video_url', 'image_url',
            'steps_list', 'benefits_list', 'mistakes_list'
        ]

    def get_steps_list(self, obj):
        return [s.strip() for s in obj.steps.split('\n') if s.strip()]

    def get_benefits_list(self, obj):
        return [b.strip() for b in obj.benefits.split('\n') if b.strip()]

    def get_mistakes_list(self, obj):
        return [m.strip() for m in obj.mistakes.split('\n') if m.strip()]


# ─── Diet / Meal Plan Serializers ────────────────────────────────────────────

class MealPlanSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MealPlan
        fields = [
            'id', 'user', 'day_of_week', 'meal_name',
            'breakfast', 'lunch', 'dinner', 'snacks',
            'calories', 'protein', 'carbs', 'fats'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        # Auto-assign user from request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserProgressSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserProgress
        fields = ['id', 'user', 'date', 'calories_burned', 'workouts_done', 'current_weight', 'streak']
        read_only_fields = ['user', 'date']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


# ─── Membership / Payment Serializers ────────────────────────────────────────

class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = ['id', 'name', 'plan_type', 'price', 'duration_days', 'features']


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'razorpay_order_id', 'razorpay_payment_id', 'amount', 'plan', 'status', 'created_at']
        read_only_fields = ['user', 'razorpay_order_id', 'razorpay_payment_id', 'status', 'created_at']
