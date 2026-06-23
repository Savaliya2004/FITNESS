import json
import logging
from django.conf import settings
import google.generativeai as genai

logger = logging.getLogger('fitx')

# Initialize Gemini API if key is available
GEMINI_API_KEY = getattr(settings, 'GEMINI_API_KEY', None)
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    # We will try to fetch it from environment if not in settings
    import os
    env_key = os.getenv('GEMINI_API_KEY')
    if env_key:
        genai.configure(api_key=env_key)

class AICoachService:
    @staticmethod
    def _get_model():
        # Use gemini-1.5-pro or gemini-1.5-flash
        try:
            return genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            logger.error(f"Failed to load Gemini model: {e}")
            return None

    @staticmethod
    def generate_fitness_plan(user_profile, mood, time_available):
        model = AICoachService._get_model()
        if not model:
            return {"error": "AI service is currently unavailable."}

        height_cm = user_profile.height or 170
        weight_kg = user_profile.weight or 70
        goal = user_profile.fitness_goal or "general_fitness"
        diet_pref = user_profile.dietary_preference or "Any"
        age = user_profile.age or 30
        gender = getattr(user_profile, 'gender', 'Not specified')

        prompt = f"""
You are an AI fitness coach + behavioral psychologist.

User details:
* Age: {age}
* Gender: {gender}
* Weight: {weight_kg} kg
* Height: {height_cm} cm
* Goal: {goal}
* Mood: {mood}
* Streak: {user_profile.longest_streak} days
* Time Available: {time_available} minutes
* Diet Preference: {diet_pref}

Task:
Create a daily fitness plan AND improve user consistency.

Instructions:
1. Give workout plan based on mood (tired=light, normal=moderate, energetic=intense, stressed=relaxing)
2. Give diet (Indian friendly)
3. Analyze consistency behavior (streak: {user_profile.longest_streak})
4. Suggest 1 small habit to improve
5. Give short motivation

Keep everything simple, realistic, and actionable.

Please return the response as valid JSON with the following keys exactly:
"workout" (string), "diet" (string), "insight" (string), "habit" (string), "motivation" (string)

Do NOT wrap the response in markdown blocks like ```json ... ```, just pure JSON.
"""
        try:
            response = model.generate_content(prompt)
            # Try to parse the response as JSON
            text = response.text
            # Clean up potential markdown formatting
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            result = json.loads(text.strip())
            return result
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return {"error": "Failed to generate plan. Please try again later.", "details": str(e)}
