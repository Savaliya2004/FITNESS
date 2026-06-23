from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .services import AICoachService
from account.models import FitnessProfile
import os

@login_required
def coach_dashboard(request):
    """Render the AI Coach main UI."""
    return render(request, 'ai_coach/coach.html')

@login_required
def generate_plan(request):
    """API endpoint to generate AI plan via AJAX."""
    if request.method == 'POST':
        mood = request.POST.get('mood', 'normal')
        time_available = request.POST.get('time', '30')
        
        # Check if API key is configured
        if not os.getenv('GEMINI_API_KEY'):
            # Return a mock response so the user can see the UI without an API key
            return JsonResponse({
                'error': False,
                'data': {
                    'workout': 'Light Yoga (15 min) + Stretching\n\n1. Neck Rolls (10 reps)\n2. Cat-Cow Stretch (1 min)\n3. Child\'s Pose (2 mins)\n4. Deep Breathing (5 mins)',
                    'diet': 'Dal Tadka with Brown Rice and a side of Cucumber Raita. Keep it light and easy to digest today.',
                    'insight': 'I noticed you usually skip when you are feeling "tired". Your body might be asking for active recovery rather than high intensity.',
                    'habit': 'Drink a glass of water immediately upon waking up.',
                    'motivation': 'Consistency over intensity. Showing up on the tired days, even for 10 minutes, builds the habit loop!'
                }
            })

        user = request.user
        result = AICoachService.generate_fitness_plan(user, mood, time_available)
        
        if "error" in result:
            return JsonResponse({'error': True, 'message': result['error']})
            
        return JsonResponse({
            'error': False,
            'data': result
        })
        
    return JsonResponse({'error': True, 'message': 'Invalid request method'})
