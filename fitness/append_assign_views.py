import os

filepath = r"c:\Users\Dev\Desktop\FITNESS\env\fitness\account\views.py"

views_code = """
# ─── Assigning Plans (Diet & Exercise) ──────────────────────────────────────

@login_required
@role_required('admin')
def admin_assign_exercise(request, user_id):
    if request.method == 'POST':
        from workout.models import UserRoutine, Exercise
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        target_user = get_object_or_404(User, id=user_id)
        exercise_id = request.POST.get('exercise_id')
        
        if exercise_id:
            exercise = get_object_or_404(Exercise, id=exercise_id)
            UserRoutine.objects.get_or_create(user=target_user, exercise=exercise)
            messages.success(request, f"Exercise '{exercise.name}' assigned to {target_user.username}.")
        else:
            messages.error(request, "No exercise selected.")
            
    return redirect('admin_dashboard')

@login_required
@role_required('admin')
def admin_assign_meal_plan(request, user_id):
    if request.method == 'POST':
        from diet.models import MealPlan
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        target_user = get_object_or_404(User, id=user_id)
        
        day_of_week = request.POST.get('day_of_week')
        meal_name = request.POST.get('meal_name', 'Daily Plan')
        breakfast = request.POST.get('breakfast', '')
        lunch = request.POST.get('lunch', '')
        dinner = request.POST.get('dinner', '')
        snacks = request.POST.get('snacks', '')
        calories = int(request.POST.get('calories', 0))
        protein = float(request.POST.get('protein', 0))
        carbs = float(request.POST.get('carbs', 0))
        fats = float(request.POST.get('fats', 0))
        
        MealPlan.objects.create(
            user=target_user,
            day_of_week=day_of_week,
            meal_name=meal_name,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            snacks=snacks,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats
        )
        
        messages.success(request, f"Meal Plan for {day_of_week} assigned to {target_user.username}.")
        
    return redirect('admin_dashboard')
"""

with open(filepath, 'a', encoding='utf-8') as f:
    f.write(views_code)

print("Views successfully appended.")
