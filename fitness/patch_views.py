"""
Script to patch account/views.py with enhanced admin views.
"""
import os

views_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'account', 'views.py')

with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = 'Admin Dashboard (RBAC'
start_idx = content.find(start_marker)
if start_idx == -1:
    raise SystemExit("ERROR: Start marker not found")
while start_idx > 0 and content[start_idx-1] != '\n':
    start_idx -= 1

forgot_marker = 'Forgot Password Flow'
end_idx = content.find(forgot_marker)
if end_idx == -1:
    raise SystemExit("ERROR: End marker not found")
while end_idx > 0 and content[end_idx-1] != '\n':
    end_idx -= 1

before = content[:start_idx]
after = content[end_idx:]

NEW_ADMIN_SECTION = '''# --- Admin Dashboard (RBAC-protected) ---

@login_required
@role_required('admin')
def admin_dashboard(request):
    """Custom admin dashboard -- proper RBAC, no hardcoded emails."""
    from store.models import Payment, MembershipPlan
    from django.db.models import Sum, Count

    try:
        import json
        from analytics.services import AnalyticsService
        overview = AnalyticsService.get_overview()
        rev = AnalyticsService.get_revenue_chart()
        growth = AnalyticsService.get_user_growth_chart()
        revenue_labels = [r['day'].strftime('%b %d') for r in rev] if rev else []
        revenue_data = [float(r['revenue']) for r in rev] if rev else []
        growth_labels = [g['week'].strftime('%b %d') for g in growth] if growth else []
        growth_data = [g['signups'] for g in growth] if growth else []
        chart_data = {
            'revenue_labels': json.dumps(revenue_labels),
            'revenue_data': json.dumps(revenue_data),
            'growth_labels': json.dumps(growth_labels),
            'growth_data': json.dumps(growth_data),
        }
    except Exception:
        overview = {}
        chart_data = {}

    import json as _json
    from datetime import timedelta
    from django.utils import timezone as _tz

    users = FitnessProfile.objects.all().order_by('-date_joined')
    meal_plans = MealPlan.objects.select_related('user').order_by('-id')[:50]
    workout_programs = WorkoutProgram.objects.all()
    payments = Payment.objects.select_related('user').order_by('-created_at')[:50]
    routines = UserRoutine.objects.select_related('user', 'exercise').order_by('-id')[:30]

    total_users = users.count()
    total_payments = payments.count()
    total_revenue = Payment.objects.filter(status='success').aggregate(Sum('amount'))['amount__sum'] or 0
    total_meal_plans = MealPlan.objects.count()

    premium_members = users.filter(membership_type='premium').count()
    elite_members = users.filter(membership_type='elite').count()
    free_members = users.filter(membership_type='free').count()

    month_start = _tz.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_signups_month = users.filter(date_joined__gte=month_start).count()
    week_ago = _tz.now() - timedelta(days=7)
    new_users_week = users.filter(date_joined__gte=week_ago).count()
    thirty_days_ago = _tz.now() - timedelta(days=30)
    active_users = users.filter(last_login__gte=thirty_days_ago).count()

    try:
        from community.models import CommunityPost, Comment
        total_posts = CommunityPost.objects.count()
        flagged_posts = CommunityPost.objects.filter(is_flagged=True).count()
        total_comments = Comment.objects.count()
        community_posts = CommunityPost.objects.select_related('author').order_by('-created_at')[:30]
    except Exception:
        total_posts = 0
        flagged_posts = 0
        total_comments = 0
        community_posts = []

    try:
        from core.models import BlogPost, Challenge, ChallengeEnrollment, ContactMessage
        total_blogs = BlogPost.objects.count()
        published_blogs = BlogPost.objects.filter(status='published').count()
        draft_blogs = BlogPost.objects.filter(status='draft').count()
        blog_posts = BlogPost.objects.select_related('author', 'category').order_by('-created_at')[:30]
        total_challenges = Challenge.objects.count()
        active_challenges = Challenge.objects.filter(status='active').count()
        total_enrollments = ChallengeEnrollment.objects.count()
        challenges = Challenge.objects.all().order_by('-created_at')[:30]
        total_contacts = ContactMessage.objects.count()
        unresolved_contacts = ContactMessage.objects.filter(is_resolved=False).count()
        contact_messages = ContactMessage.objects.all().order_by('-created_at')[:50]
    except Exception:
        total_blogs = published_blogs = draft_blogs = 0
        blog_posts = []
        total_challenges = active_challenges = total_enrollments = 0
        challenges = []
        total_contacts = unresolved_contacts = 0
        contact_messages = []

    try:
        from booking.models import ClassBooking
        total_bookings = ClassBooking.objects.count()
        upcoming_bookings = ClassBooking.objects.filter(status='booked').count()
        bookings = ClassBooking.objects.select_related('user').order_by('-created_at')[:30]
    except Exception:
        total_bookings = 0
        upcoming_bookings = 0
        bookings = []

    premium_revenue = Payment.objects.filter(status='success', plan='premium').aggregate(Sum('amount'))['amount__sum'] or 0
    elite_revenue = Payment.objects.filter(status='success', plan='elite').aggregate(Sum('amount'))['amount__sum'] or 0
    membership_plans = MembershipPlan.objects.all()

    try:
        from workout.models import Exercise
        total_exercises = Exercise.objects.count()
        exercises = Exercise.objects.all().order_by('name')[:50]
        exercise_categories = list(Exercise.objects.values('category').annotate(count=Count('id')).order_by('-count')[:5])
    except Exception:
        total_exercises = 0
        exercises = []
        exercise_categories = []

    membership_chart = _json.dumps({
        'free': free_members,
        'premium': premium_members,
        'elite': elite_members,
    })

    context = {
        'users': users,
        'meal_plans': meal_plans,
        'workout_programs': workout_programs,
        'payments': payments,
        'routines': routines,
        'membership_plans': membership_plans,
        'community_posts': community_posts,
        'blog_posts': blog_posts,
        'challenges': challenges,
        'contact_messages': contact_messages,
        'bookings': bookings,
        'exercises': exercises,
        'total_users': total_users,
        'active_users': active_users,
        'premium_members': premium_members,
        'elite_members': elite_members,
        'free_members': free_members,
        'new_signups_month': new_signups_month,
        'new_users_week': new_users_week,
        'total_payments': total_payments,
        'total_revenue': total_revenue,
        'premium_revenue': premium_revenue,
        'elite_revenue': elite_revenue,
        'total_meal_plans': total_meal_plans,
        'total_exercises': total_exercises,
        'exercise_categories': exercise_categories,
        'total_posts': total_posts,
        'flagged_posts': flagged_posts,
        'total_comments': total_comments,
        'total_blogs': total_blogs,
        'published_blogs': published_blogs,
        'draft_blogs': draft_blogs,
        'total_challenges': total_challenges,
        'active_challenges': active_challenges,
        'total_enrollments': total_enrollments,
        'total_bookings': total_bookings,
        'upcoming_bookings': upcoming_bookings,
        'total_contacts': total_contacts,
        'unresolved_contacts': unresolved_contacts,
        'membership_chart': membership_chart,
        'overview': overview,
        **chart_data,
    }
    return render(request, 'account/admin_dashboard.html', context)


@login_required
@role_required('admin')
def admin_delete_user(request, user_id):
    user = get_object_or_404(FitnessProfile, id=user_id)
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('admin_dashboard')
    username = user.username
    user.delete()
    messages.success(request, f"User '{username}' deleted successfully.")
    return redirect('admin_dashboard')


@login_required
@role_required('admin')
def admin_toggle_staff(request, user_id):
    user = get_object_or_404(FitnessProfile, id=user_id)
    user.is_staff = not user.is_staff
    user.save()
    status = "granted staff" if user.is_staff else "revoked staff from"
    messages.success(request, f"Successfully {status} user '{user.username}'.")
    return redirect('admin_dashboard')


@login_required
@role_required('admin')
def admin_delete_meal_plan(request, plan_id):
    plan = get_object_or_404(MealPlan, id=plan_id)
    plan.delete()
    messages.success(request, "Meal plan deleted.")
    return redirect('admin_dashboard')


@login_required
@role_required('admin')
def admin_delete_payment(request, payment_id):
    from store.models import Payment
    payment = get_object_or_404(Payment, id=payment_id)
    payment.delete()
    messages.success(request, "Payment record deleted.")
    return redirect('admin_dashboard')


@login_required
@role_required('admin')
def admin_resolve_contact(request, contact_id):
    from core.models import ContactMessage
    msg = get_object_or_404(ContactMessage, id=contact_id)
    msg.is_resolved = True
    msg.save(update_fields=['is_resolved'])
    messages.success(request, f"Contact message #{contact_id} marked as resolved.")
    return redirect('admin_dashboard')


@login_required
@role_required('admin')
def admin_flag_post(request, post_id):
    from community.models import CommunityPost
    post = get_object_or_404(CommunityPost, id=post_id)
    post.is_flagged = not post.is_flagged
    post.save(update_fields=['is_flagged'])
    messages.success(request, f"Post #{post_id} flag status updated.")
    return redirect('admin_dashboard')


'''

new_content = before + NEW_ADMIN_SECTION + after

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

with open('patch_result.txt', 'w') as f:
    f.write(f"SUCCESS: views.py updated. New size: {len(new_content)} chars\n")
    f.write(f"Replaced chars {start_idx}-{end_idx}\n")
