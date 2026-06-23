"""
Diet Views
──────────
• diet_home         — show existing 7-day plan or prompt generation
• generate_diet     — (POST) create/regenerate 7-day plan from DB meals
• regenerate_diet   — convenience alias for regeneration
• diet_pdf_download — serve a PDF of the 7-day plan
• save_diet_plan    — legacy fallback (kept for backward-compat)
"""

import io
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from .models import UserDiet, Meal, MealPlan
from .recommender import DietRecommender, generate_7day_plan, calorie_summary
from core.decorators import membership_required


# ─────────────────────────────────────────────────────────────────
# DIET HOME  – show existing plan or landing card
# ─────────────────────────────────────────────────────────────────
@login_required
def diet_home(request):
    user         = request.user
    targets      = DietRecommender.calculate_targets(user)
    user_diets   = list(UserDiet.objects.filter(user=user).select_related(
                       'breakfast', 'lunch', 'dinner', 'snack').order_by('id'))
    summary      = calorie_summary(user_diets) if user_diets else None
    has_meals_db = Meal.objects.filter(is_active=True).exists()

    context = {
        'user_diets':    user_diets,
        'targets':       targets,
        'summary':       summary,
        'has_meals_db':  has_meals_db,
        'is_trial':      not user_diets and user.membership_type == 'free',
        'dietary_label': _diet_label(user),
    }
    return render(request, 'diet/diet.html', context)





# ─────────────────────────────────────────────────────────────────
# PDF DOWNLOAD  – pure-Python PDF without reportlab dependency
# ─────────────────────────────────────────────────────────────────
@login_required
def diet_pdf_download(request):
    """
    Generates a clean HTML page and sends it with a
    Content-Disposition: attachment header so the browser downloads it.
    The browser's native print-to-PDF can convert it perfectly.
    No external PDF library required.
    """
    user       = request.user
    user_diets = list(UserDiet.objects.filter(user=user).select_related(
                      'breakfast', 'lunch', 'dinner', 'snack').order_by('id'))
    targets    = DietRecommender.calculate_targets(user)
    summary    = calorie_summary(user_diets)

    html = _build_pdf_html(user, user_diets, targets, summary)
    response = HttpResponse(html, content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="FitX_Diet_Plan.html"'
    return response


# ─────────────────────────────────────────────────────────────────
# LEGACY SAVE  – kept for backward-compat with old JS post
# ─────────────────────────────────────────────────────────────────
@membership_required()
def save_diet_plan(request):
    if request.method == 'POST':
        calories = int(float(request.POST.get('calories', 2000)))
        MealPlan.objects.filter(user=request.user).delete()
        breakfast = request.POST.get('breakfast', 'Oats')
        lunch     = request.POST.get('lunch', 'Rice')
        dinner    = request.POST.get('dinner', 'Salad')
        snacks    = request.POST.get('snacks', 'Nuts')
        days      = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for day in days:
            MealPlan.objects.create(
                user=request.user, day_of_week=day,
                meal_name=f"{breakfast[:30]} | {lunch[:30]} | {dinner[:30]}",
                breakfast=breakfast, lunch=lunch, dinner=dinner, snacks=snacks,
                calories=calories,
                protein=round(calories * 0.3 / 4),
                carbs=round(calories * 0.4 / 4),
                fats=round(calories * 0.3 / 9),
            )
        return redirect('dashboard')
    return redirect('diet')


# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
def _diet_label(user) -> str:
    pref = getattr(user, 'dietary_preference', '') or ''
    mapping = {'veg': 'Vegetarian', 'egg': 'Eggetarian', 'nonveg': 'Non-Vegetarian'}
    return mapping.get(pref, 'Not set')


def _build_pdf_html(user, user_diets, targets, summary) -> str:
    """Build a self-contained HTML string for PDF download."""
    rows = ''
    day_colors = {
        'Monday': '#c44dff', 'Tuesday': '#3b82f6', 'Wednesday': '#22c55e',
        'Thursday': '#f59e0b', 'Friday': '#ef4444', 'Saturday': '#06b6d4',
        'Sunday': '#ec4899',
    }
    for ud in user_diets:
        day  = ud.get_day_of_week_display()
        col  = day_colors.get(day, '#888')
        bf   = ud.breakfast.name if ud.breakfast else '—'
        lu   = ud.lunch.name if ud.lunch else '—'
        dn   = ud.dinner.name if ud.dinner else '—'
        sn   = ud.snack.name if ud.snack else '—'
        rows += f"""
        <tr>
          <td style="background:{col};color:#fff;font-weight:700;padding:12px 16px;border-radius:8px;">{day}</td>
          <td>{bf}<br><small style="color:#888">{ud.breakfast.calories if ud.breakfast else 0} kcal</small></td>
          <td>{lu}<br><small style="color:#888">{ud.lunch.calories if ud.lunch else 0} kcal</small></td>
          <td>{dn}<br><small style="color:#888">{ud.dinner.calories if ud.dinner else 0} kcal</small></td>
          <td>{sn}<br><small style="color:#888">{ud.snack.calories if ud.snack else 0} kcal</small></td>
          <td style="font-weight:700;color:{col}">{ud.total_calories} kcal</td>
        </tr>"""

    avg = summary['avg_calories'] if summary else 0
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>FitX — 7-Day Diet Plan — {user.get_full_name() or user.username}</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; background:#fff; color:#111; padding:40px; }}
  h1   {{ color:#c44dff; font-size:28pt; margin:0; }}
  h2   {{ color:#333; margin-top:30px; font-size:14pt; border-bottom:2px solid #c44dff; padding-bottom:6px; }}
  .meta {{ color:#555; margin:8px 0 30px; font-size:12pt; }}
  .stat-row {{ display:flex; gap:30px; margin-bottom:30px; flex-wrap:wrap; }}
  .stat {{ background:#f8f0ff; border-left:4px solid #c44dff; padding:12px 20px; border-radius:8px; min-width:140px; }}
  .stat h3 {{ margin:0; font-size:22pt; color:#c44dff; }}
  .stat p  {{ margin:4px 0 0; color:#555; font-size:9pt; }}
  table {{ width:100%; border-collapse:collapse; font-size:10pt; }}
  th    {{ background:#1a1a2e; color:#fff; padding:10px 14px; text-align:left; }}
  td    {{ border-bottom:1px solid #eee; padding:10px 14px; vertical-align:top; }}
  tr:hover td {{ background:#faf5ff; }}
  .footer {{ margin-top:50px; font-size:9pt; color:#aaa; text-align:center; border-top:1px solid #eee; padding-top:12px; }}
</style>
</head>
<body>
  <h1>🏋️ FitX — Personalised Diet Plan</h1>
  <p class="meta">Generated for: <strong>{user.get_full_name() or user.username}</strong> &nbsp;|&nbsp;
     Goal: <strong>{targets.get('goal','').replace('_',' ').title()}</strong> &nbsp;|&nbsp;
     Target: <strong>{targets.get('calories', 0)} kcal/day</strong></p>

  <div class="stat-row">
    <div class="stat"><h3>{targets.get('calories',0)}</h3><p>Daily Target (kcal)</p></div>
    <div class="stat"><h3>{targets.get('protein_g',0)}g</h3><p>Daily Protein</p></div>
    <div class="stat"><h3>{targets.get('carbs_g',0)}g</h3><p>Daily Carbs</p></div>
    <div class="stat"><h3>{targets.get('fats_g',0)}g</h3><p>Daily Fats</p></div>
    <div class="stat"><h3>{avg}</h3><p>Avg Daily (kcal)</p></div>
  </div>

  <h2>7-Day Meal Schedule</h2>
  <table>
    <thead>
      <tr><th>Day</th><th>🍳 Breakfast</th><th>🥗 Lunch</th><th>🍲 Dinner</th><th>🍎 Snack</th><th>Total</th></tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>

  <div class="footer">Stay consistent. Drink 2–3 L of water daily. &nbsp;|&nbsp; FitX Nutrition — {user.username}</div>
</body>
</html>"""
