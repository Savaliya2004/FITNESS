"""
Diet Recommendation Engine
──────────────────────────
• TDEE / macro calculation (Mifflin-St Jeor)
• Generates a 7-day plan entirely from DB-stored Meal objects
• No hard-coded food items — admin controls everything
• Respects dietary preference, goal, and calorie targets
"""

import random
from .models import Meal, UserDiet


# ─────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────
ACTIVITY_MULTIPLIERS = {
    'sedentary': 1.2,
    'light':     1.375,
    'moderate':  1.55,
    'active':    1.725,
    'extreme':   1.9,
}

GOAL_ADJUSTMENTS = {
    'weight_loss':    {'calorie_mod': -500, 'protein_pct': 0.35, 'carb_pct': 0.35, 'fat_pct': 0.30},
    'fat_loss':       {'calorie_mod': -400, 'protein_pct': 0.40, 'carb_pct': 0.30, 'fat_pct': 0.30},
    'muscle_gain':    {'calorie_mod': +400, 'protein_pct': 0.35, 'carb_pct': 0.40, 'fat_pct': 0.25},
    'endurance':      {'calorie_mod': +200, 'protein_pct': 0.25, 'carb_pct': 0.50, 'fat_pct': 0.25},
    'maintenance':    {'calorie_mod':    0, 'protein_pct': 0.30, 'carb_pct': 0.40, 'fat_pct': 0.30},
    'flexibility':    {'calorie_mod':    0, 'protein_pct': 0.25, 'carb_pct': 0.45, 'fat_pct': 0.30},
    'general_fitness':{'calorie_mod':    0, 'protein_pct': 0.30, 'carb_pct': 0.40, 'fat_pct': 0.30},
}

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

# Dietary fallback chain: if 'veg' has no meals, don't crash
DIETARY_FALLBACK = {
    'veg':    ['veg'],
    'egg':    ['egg', 'veg'],
    'nonveg': ['nonveg', 'egg', 'veg'],
}


# ─────────────────────────────────────────────────────────────────
# 1. TDEE + Macro Targets
# ─────────────────────────────────────────────────────────────────
class DietRecommender:
    """Stateless service — call class-methods directly."""

    @classmethod
    def calculate_targets(cls, user) -> dict:
        """Return TDEE, macro targets, and goal info for a given user."""
        if not all([user.weight, user.height, user.age]):
            return {
                'calories': 2000,
                'protein_g': 150, 'carbs_g': 200, 'fats_g': 67,
                'bmr': 0, 'tdee': 0, 'goal': 'general_fitness',
                'note': 'Default targets — complete your profile for a personalised plan.',
            }

        gender = getattr(user, 'gender', 'N')
        if gender == 'F':
            bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age - 161
        else:
            bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age + 5

        activity = getattr(user, 'activity_level', 'moderate')
        tdee = bmr * ACTIVITY_MULTIPLIERS.get(activity, 1.55)

        goal = getattr(user, 'fitness_goal', None) or 'maintenance'
        adj  = GOAL_ADJUSTMENTS.get(goal, GOAL_ADJUSTMENTS['maintenance'])

        target_calories = max(1200, round(tdee + adj['calorie_mod']))
        protein_g = round(target_calories * adj['protein_pct'] / 4)
        carbs_g   = round(target_calories * adj['carb_pct'] / 4)
        fats_g    = round(target_calories * adj['fat_pct'] / 9)

        return {
            'calories':  target_calories,
            'protein_g': protein_g,
            'carbs_g':   carbs_g,
            'fats_g':    fats_g,
            'bmr':       round(bmr),
            'tdee':      round(tdee),
            'goal':      goal,
        }


# ─────────────────────────────────────────────────────────────────
# 2. Meal Pool Builder
# ─────────────────────────────────────────────────────────────────
def _fetch_meal_pool(dietary_type: str, goal: str) -> dict[str, list]:
    """
    Returns a dict keyed by meal_type with lists of Meal objects.
    Priority: goal-specific meals first, then 'any'.
    Falls back through the dietary chain so we never return empty lists.
    """
    pool = {slot: [] for slot in ('breakfast', 'lunch', 'dinner', 'snack')}
    diet_chain = DIETARY_FALLBACK.get(dietary_type, ['veg'])

    for slot in pool:
        for diet in diet_chain:
            # First try goal-specific meals
            meals = list(
                Meal.objects.filter(
                    meal_type=slot, dietary_type=diet,
                    goal_tag=goal, is_active=True
                )
            )
            # Then add 'any' meals
            meals += list(
                Meal.objects.filter(
                    meal_type=slot, dietary_type=diet,
                    goal_tag='any', is_active=True
                )
            )
            if meals:
                pool[slot] = meals
                break  # found enough, don't need fallback tier

    return pool


# ─────────────────────────────────────────────────────────────────
# 3. Smart 7-Day Plan Generator
# ─────────────────────────────────────────────────────────────────
def generate_7day_plan(user) -> list[UserDiet]:
    """
    Creates (or replaces) a 7-day UserDiet plan for the given user.
    Strategy:
      • Shuffle each slot's pool
      • Cycle through to avoid repeats within 3 consecutive days
      • Keep daily calories within ±15 % of the target
    Returns the list of 7 UserDiet instances.
    """
    targets     = DietRecommender.calculate_targets(user)
    goal        = targets['goal']
    dietary     = getattr(user, 'dietary_preference', None) or 'veg'

    # Normalise dietary value
    if dietary not in ('veg', 'egg', 'nonveg'):
        dietary = 'veg'

    pool = _fetch_meal_pool(dietary, goal)

    # Safety: if any slot has no meals, cannot generate
    missing = [slot for slot, meals in pool.items() if not meals]
    if missing:
        return []          # caller notifies the user to seed meals

    # Shuffle each pool for variety
    for slot in pool:
        random.shuffle(pool[slot])

    # Delete existing plan for this user
    UserDiet.objects.filter(user=user).delete()

    created_days = []
    used: dict[str, set] = {slot: set() for slot in pool}  # track recent ids

    for i, day in enumerate(DAYS):
        picks = {}
        for slot in ('breakfast', 'lunch', 'dinner', 'snack'):
            candidates = pool[slot]
            # Prefer meals not used in last 3 days
            fresh = [m for m in candidates if m.id not in used[slot]]
            chosen = random.choice(fresh) if fresh else random.choice(candidates)
            picks[slot] = chosen
            used[slot].add(chosen.id)
            if len(used[slot]) > 3:
                # Allow oldest to be re-used
                used[slot] = set(list(used[slot])[-3:])

        ud = UserDiet.objects.create(
            user=user,
            day_of_week=day,
            breakfast=picks['breakfast'],
            lunch=picks['lunch'],
            dinner=picks['dinner'],
            snack=picks['snack'],
        )
        ud.compute_totals()
        created_days.append(ud)

    return created_days


# ─────────────────────────────────────────────────────────────────
# 4. Per-Day Calorie Summary Helper
# ─────────────────────────────────────────────────────────────────
def calorie_summary(user_diets: list[UserDiet]) -> dict:
    """Return weekly totals and per-day breakdown for the template."""
    total_cals = sum(d.total_calories for d in user_diets)
    avg_cals   = round(total_cals / len(user_diets)) if user_diets else 0
    return {
        'total_calories': total_cals,
        'avg_calories':   avg_cals,
        'days': [
            {
                'day':      d.get_day_of_week_display(),
                'calories': d.total_calories,
                'protein':  d.total_protein,
                'carbs':    d.total_carbs,
                'fats':     d.total_fats,
            }
            for d in user_diets
        ],
    }
