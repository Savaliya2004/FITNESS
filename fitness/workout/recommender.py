"""Workout recommendation engine — rule-based, ML-ready."""
from typing import List, Dict
from workout.models import Exercise, UserRoutine


class WorkoutRecommender:
    GOAL_CATEGORY_MAP = {
        'muscle_gain': {'primary': ['strength'], 'secondary': ['hiit'], 'intensity': 'high'},
        'fat_loss': {'primary': ['hiit', 'cardio'], 'secondary': ['strength'], 'intensity': 'high'},
        'weight_loss': {'primary': ['cardio', 'hiit'], 'secondary': ['yoga', 'home'], 'intensity': 'moderate'},
        'endurance': {'primary': ['cardio'], 'secondary': ['hiit', 'strength'], 'intensity': 'moderate'},
        'flexibility': {'primary': ['yoga', 'flexibility'], 'secondary': ['home'], 'intensity': 'low'},
        'maintenance': {'primary': ['home', 'yoga'], 'secondary': ['cardio', 'strength'], 'intensity': 'moderate'},
        'general_fitness': {'primary': ['cardio', 'strength'], 'secondary': ['yoga', 'hiit'], 'intensity': 'moderate'},
    }

    BMI_ADJUSTMENTS = {
        'underweight': {'avoid': ['hiit'], 'prefer': ['strength'], 'intensity_mod': -1},
        'normal': {'avoid': [], 'prefer': [], 'intensity_mod': 0},
        'overweight': {'avoid': [], 'prefer': ['cardio', 'hiit'], 'intensity_mod': 0},
        'obese': {'avoid': ['hiit'], 'prefer': ['cardio', 'yoga'], 'intensity_mod': -1},
    }

    DIFFICULTY_MAP = {
        'low': ['beginner', 'basics', 'all'],
        'moderate': ['beginner', 'intermediate', 'all'],
        'high': ['intermediate', 'advanced', 'all'],
    }

    @classmethod
    def recommend(cls, user, limit=6) -> List[Dict]:
        goal = user.fitness_goal or 'maintenance'
        bmi = user.bmi
        bmi_category = cls._get_bmi_category(bmi)

        config = cls.GOAL_CATEGORY_MAP.get(goal, cls.GOAL_CATEGORY_MAP['maintenance'])
        bmi_adj = cls.BMI_ADJUSTMENTS.get(bmi_category, cls.BMI_ADJUSTMENTS['normal'])

        done_exercise_ids = set(
            UserRoutine.objects.filter(user=user).values_list('exercise_id', flat=True)
        )

        all_exercises = Exercise.objects.all()
        scored = []

        for exercise in all_exercises:
            score = 0
            if exercise.category in config['primary']:
                score += 10
            elif exercise.category in config['secondary']:
                score += 5
            if exercise.category in bmi_adj.get('prefer', []):
                score += 3
            if exercise.category in bmi_adj.get('avoid', []):
                score -= 8
            allowed = cls.DIFFICULTY_MAP.get(config['intensity'], ['beginner', 'intermediate'])
            if exercise.exercise_type.lower() in allowed:
                score += 4
            else:
                score -= 2
            if exercise.id not in done_exercise_ids:
                score += 3

            if score > 0:
                scored.append({
                    'exercise': exercise,
                    'score': score,
                    'reason': cls._generate_reason(exercise, goal),
                })

        scored.sort(key=lambda x: x['score'], reverse=True)
        return scored[:limit]

    @staticmethod
    def _get_bmi_category(bmi):
        if bmi is None:
            return 'normal'
        if bmi < 18.5:
            return 'underweight'
        if bmi < 25:
            return 'normal'
        if bmi < 30:
            return 'overweight'
        return 'obese'

    @staticmethod
    def _generate_reason(exercise, goal):
        reasons = {
            'muscle_gain': f"Great for building muscle — {exercise.reps_sets}",
            'fat_loss': f"High calorie burn: {exercise.calories_burned} kcal",
            'weight_loss': f"Effective for weight management",
            'endurance': f"Builds stamina and cardiovascular strength",
            'flexibility': f"Improves flexibility and mobility",
        }
        return reasons.get(goal, "Recommended based on your profile")
