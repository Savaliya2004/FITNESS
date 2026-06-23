import json
from django.shortcuts import render
from .models import WorkoutProgram, Trainer, Exercise
from django.contrib.auth.decorators import login_required

@login_required
def workout_list(request):
    exercises = Exercise.objects.all()
    
    # We need to build a JSON object matching workoutData structure
    # strength -> beginner/intermediate/advanced
    # yoga -> list
    # hiit -> core/fullbody
    # home -> basics/cardio
    
    data = {
        'strength': {'beginner': [], 'intermediate': [], 'advanced': []},
        'cardio': {'all': [], 'hiit': []},
        'hiit': {'core': [], 'fullbody': []},
        'yoga': {'all': [], 'vinyasa': []},
        'home': {'basics': [], 'cardio': []},
        'flexibility': {'all': [], 'mobility': []}
    }
    
    is_free = request.user.membership_type == 'free'
    counters = {cat: 0 for cat in data.keys()}
    
    for ex in exercises:
        ex_dict = {
            'id': str(ex.id),
            'name': ex.name,
            'img': ex.image_url if ex.image_url else 'https://images.unsplash.com/photo-1598971639058-fab3c043d34d?w=400&q=80',
            'video': ex.video_url,
            'reps': ex.reps_sets,
            'burn': f'{ex.calories_burned} kcal', 
            'difficulty': ex.difficulty,
            'steps': [s.strip() for s in ex.steps.split('\n') if s.strip()],
            'benefits': [b.strip() for b in ex.benefits.split('\n') if b.strip()],
            'mistakes': [m.strip() for m in ex.mistakes.split('\n') if m.strip()]
        }
        
        cat = ex.category
        if cat in data:
            if is_free and counters[cat] >= 5:
                continue
            
            # If sub-key doesn't exist, put in 'all' or first available
            sub_cat = ex.exercise_type
            if sub_cat in data[cat]:
                data[cat][sub_cat].append(ex_dict)
                counters[cat] += 1
            else:
                # Default to the first sub-key if type doesn't match
                first_key = list(data[cat].keys())[0]
                data[cat][first_key].append(ex_dict)
                counters[cat] += 1

    context = {
        'workout_data_json': json.dumps(data)
    }
    return render(request, 'workout/fitness.html', context)

def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'workout/coaches.html', {'trainers': trainers})

def sport(request):
    return render(request, 'workout/sport.html')

from django.contrib.auth.decorators import login_required
from .models import UserRoutine
from django.shortcuts import get_object_or_404, redirect

from core.decorators import membership_required

@membership_required()
def add_to_routine(request, exercise_id):
    from django.contrib import messages
    exercise = get_object_or_404(Exercise, id=exercise_id)
    UserRoutine.objects.get_or_create(user=request.user, exercise=exercise)
    messages.success(request, f"'{exercise.name}' added to your routine! 💪")
    return redirect('dashboard')

from core.decorators import membership_required

@membership_required()
def generate_routine(request):
    """
    Generate basic routine based on User weight & Fitness goal 
    (weight loss / gain / maintenance)
    """
    goal = getattr(request.user, 'fitness_goal', 'maintenance')
    
    # clear existing
    UserRoutine.objects.filter(user=request.user).delete()
    
    selected_exercises = []
    if goal == 'weight_loss':
        selected_exercises = list(Exercise.objects.filter(category='hiit')[:3]) + list(Exercise.objects.filter(category='home', exercise_type='cardio')[:2])
    elif goal == 'muscle_gain':
        selected_exercises = list(Exercise.objects.filter(category='strength')[:4])
    else:
        # maintenance
        selected_exercises = list(Exercise.objects.filter(category='yoga')[:2]) + list(Exercise.objects.filter(category='home', exercise_type='basics')[:2])
        
    for ex in selected_exercises:
        UserRoutine.objects.create(user=request.user, exercise=ex)
        
    return redirect('dashboard')
@login_required
def remove_from_routine(request, routine_id):
    routine = get_object_or_404(UserRoutine, id=routine_id, user=request.user)
    name = routine.exercise.name
    routine.delete()
    from django.contrib import messages
    messages.success(request, f"'{name}' removed from your routine.")
    return redirect('dashboard')
