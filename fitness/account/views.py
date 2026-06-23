import json
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from .models import FitnessProfile, OTPVerification
from diet.models import UserProgress, MealPlan
from workout.models import WorkoutProgram, UserRoutine
from core.models import Challenge
from core.decorators import role_required

logger = logging.getLogger('fitx')


@login_required
def dashboard(request):
    progress_data = UserProgress.objects.filter(user=request.user).order_by('date')
    workouts = WorkoutProgram.objects.all()[:6]
    diet_plans = MealPlan.objects.filter(user=request.user)
    challenges = Challenge.objects.all()[:6]

    if not diet_plans.exists():
        diet_plans = None

    routines = UserRoutine.objects.filter(user=request.user).select_related('exercise')
    total_routine_calories = sum(r.exercise.calories_burned for r in routines)

    # ✅ FIX: Single combined query instead of 3 separate ones
    from django.db.models import Sum
    stats = UserProgress.objects.filter(user=request.user).aggregate(
        total_workouts=Sum('workouts_done'),
        total_calories=Sum('calories_burned'),
    )
    total_workouts = stats['total_workouts'] or 0
    total_calories = stats['total_calories'] or 0

    streak = progress_data.last().streak if progress_data.exists() else 0
    current_weight = request.user.weight or (progress_data.last().current_weight if progress_data.exists() else 0)

    # Prepare data for Chart.js
    labels = [p.date.strftime("%b %d") for p in progress_data]
    calories_chart = [p.calories_burned for p in progress_data]
    weights = [float(p.current_weight) for p in progress_data]

    target_weight = request.user.target_weight or 0
    weight_to_goal = current_weight - target_weight if target_weight else 0

    # Sessions this week
    from datetime import timedelta, date
    start_of_week = date.today() - timedelta(days=date.today().weekday())
    sessions_this_week = UserProgress.objects.filter(
        user=request.user, date__gte=start_of_week, workouts_done__gt=0
    ).count()
    session_goal = 5
    session_percent = min(100, int((sessions_this_week / session_goal) * 100)) if session_goal > 0 else 0

    calorie_goal = 2500
    calorie_percent = min(100, int((total_routine_calories / calorie_goal) * 100)) if calorie_goal > 0 else 0

    # ─── Gamification & Notifications ─────────────────────────────────────
    try:
        from gamification.models import UserBadge
        from notifications.models import Notification
        recent_badges = UserBadge.objects.filter(user=request.user).select_related('badge').order_by('-awarded_at')[:4]
        unread_notifs = Notification.objects.filter(user=request.user, is_read=False).count()
    except Exception:
        recent_badges = []
        unread_notifs = 0

    context = {
        'progress_json': json.dumps({
            'labels': labels,
            'calories': calories_chart,
            'weights': weights
        }, cls=DjangoJSONEncoder),
        'latest_progress': progress_data.last(),
        'total_workouts': total_workouts,
        'total_calories': total_calories,
        'streak': streak,
        'current_weight': current_weight,
        'target_weight': target_weight,
        'weight_to_goal': weight_to_goal,
        'sessions_this_week': sessions_this_week,
        'session_goal': session_goal,
        'session_percent': session_percent,
        'calorie_goal': calorie_goal,
        'calorie_percent': calorie_percent,
        'workouts': workouts,
        'diet_plans': diet_plans,
        'challenges': challenges,
        'routines': routines,
        'total_routine_calories': total_routine_calories,
        'recent_badges': recent_badges,
        'unread_notifs': unread_notifs,
    }
    return render(request, 'account/dashboard.html', context)


@login_required
def log_progress(request):
    from datetime import date
    if request.method == 'POST':
        weight = float(request.POST.get('weight', 0))
        target_weight = request.POST.get('target_weight')
        calories = int(request.POST.get('calories_burned', 0))
        workouts = int(request.POST.get('workouts_done', 1))

        user = request.user
        user.weight = weight
        if target_weight:
            user.target_weight = float(target_weight)
        user.save()

        progress = UserProgress.objects.filter(user=request.user, date=date.today()).first()
        if progress:
            progress.current_weight = weight
            progress.calories_burned += calories
            progress.workouts_done += workouts
            progress.save()
        else:
            UserProgress.objects.create(
                user=request.user,
                date=date.today(),
                current_weight=weight,
                calories_burned=calories,
                workouts_done=workouts,
                streak=1
            )
        messages.success(request, "Progress logged successfully!")
    return redirect('dashboard')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        referral_code = request.POST.get('referral_code', '').strip()

        # Validation
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'account/signup.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'account/signup.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'account/signup.html')

        if FitnessProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'account/signup.html')

        if email and FitnessProfile.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'account/signup.html')

        user = FitnessProfile.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Process referral
        if referral_code:
            try:
                referrer = FitnessProfile.objects.filter(referral_code=referral_code.upper()).first()
                if referrer and referrer != user:
                    user.referred_by = referrer
                    user.save(update_fields=['referred_by'])
            except Exception:
                pass

        # ✅ Send Verification OTP instead of immediate login
        otp_code = OTPVerification.generate_otp()
        OTPVerification.objects.filter(user=user).delete()
        OTPVerification.objects.create(
            user=user,
            otp_hash=OTPVerification.hash_otp(otp_code)
        )

        try:
            send_mail(
                'FitX Verification OTP',
                f'Your OTP for FitX signup verification is: {otp_code}\nThis OTP is valid for 5 minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Signup email failed for {user.username}: {e}")
            messages.error(request, "OTP system is currently unavailable or your email is invalid. Account created, but please contact admin for verification.")
            return render(request, 'account/signup.html')

        request.session['pre_otp_user_id'] = user.id
        messages.success(request, f'One last step! We sent a verification code to {email}.')
        return redirect('verify_otp')

    return render(request, 'account/signup.html')


def verify_otp(request):
    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        messages.error(request, 'No pending OTP verification.')
        return redirect('login')

    user = get_object_or_404(FitnessProfile, id=user_id)

    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()

        # ✅ Secure verification using hashed OTP
        verification = OTPVerification.objects.filter(user=user, is_used=False).last()

        if verification:
            success, msg = verification.verify(otp_entered)
            if success:
                # MARK AS VERIFIED
                user.is_email_verified = True
                user.save(update_fields=['is_email_verified'])
                
                login(request, user)
                del request.session['pre_otp_user_id']
                OTPVerification.objects.filter(user=user).delete()

                messages.success(request, f'Welcome back, {user.username}!')

                next_url = request.session.pop('post_login_next', '')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard')
            else:
                messages.error(request, msg)
        else:
            messages.error(request, 'No OTP found. Please login again.')
            del request.session['pre_otp_user_id']
            return redirect('login')

    return render(request, 'account/otp_verify.html', {'email': user.email})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.username == 'MaHeK':
            return redirect('admin_dashboard')
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            # ✅ Specific Admin Rule: Only this username goes to the dashboard
            if user.username == 'MaHeK':
                login(request, user)
                messages.success(request, f'Welcome back, Super Admin {user.username}! 🔐')
                return redirect('admin_dashboard')

            # ✅ Check if email is verified
            if user.is_email_verified:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_url = request.GET.get('next') or request.POST.get('next')
                return redirect(next_url if next_url else 'dashboard')
            else:
                # User exists but email not verified (maybe they closed the tab during signup)
                otp_code = OTPVerification.generate_otp()
                OTPVerification.objects.filter(user=user).delete()
                OTPVerification.objects.create(
                    user=user,
                    otp_hash=OTPVerification.hash_otp(otp_code)
                )
                try:
                    send_mail(
                        'FitX Verification OTP',
                        f'Your verification code is: {otp_code}\nPlease verify your email to continue.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    request.session['pre_otp_user_id'] = user.id
                    messages.info(request, "Your email is not verified. We've sent a new OTP to your email.")
                    return redirect('verify_otp')
                except Exception as e:
                    logger.error(f"Login OTP failed: {e}")
                    messages.error(request, "Failed to send verification email. Please try again later.")

        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.age = request.POST.get('age') or None
        user.height = request.POST.get('height') or None
        user.weight = request.POST.get('weight') or None
        user.fitness_goal = request.POST.get('fitness_goal', 'general_fitness')
        user.activity_level = request.POST.get('activity_level', 'moderate')
        user.gender = request.POST.get('gender', '')
        user.city = request.POST.get('city', '')

        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('dashboard')
    return redirect('dashboard')


# --- Admin Dashboard (RBAC-protected) ---

@login_required
@role_required('admin')
def admin_dashboard(request):
    """Custom admin dashboard -- proper RBAC, no hardcoded emails."""
    from store.models import Payment, MembershipPlan, Order
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
        chart_data = {
            'revenue_labels': '[]', 'revenue_data': '[]',
            'growth_labels': '[]', 'growth_data': '[]'
        }

    User = get_user_model()
    users = User.objects.all().order_by('-date_joined')
    meal_plans = MealPlan.objects.select_related('user').order_by('-id')[:50]
    workout_programs = WorkoutProgram.objects.all()
    payments = Payment.objects.select_related('user').order_by('-created_at')[:50]
    store_orders = Order.objects.select_related('user').order_by('-created_at')[:50]
    routines = UserRoutine.objects.select_related('user', 'exercise').order_by('-id')[:30]

    total_users = users.count()
    total_payments = payments.count()
    total_store_orders = store_orders.count()
    total_revenue = Payment.objects.filter(status='success').aggregate(Sum('amount'))['amount__sum'] or 0
    total_meal_plans = MealPlan.objects.count()

    premium_members = users.filter(membership_type='premium').count()
    elite_members = users.filter(membership_type='elite').count()
    free_members = users.filter(membership_type='free').count()

    from datetime import timedelta
    month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_signups_month = users.filter(date_joined__gte=month_start).count()
    week_ago = timezone.now() - timedelta(days=7)
    new_users_week = users.filter(date_joined__gte=week_ago).count()
    thirty_days_ago = timezone.now() - timedelta(days=30)
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

    membership_chart = json.dumps({
        'free': free_members,
        'premium': premium_members,
        'elite': elite_members,
    })

    context = {
        'users': users,
        'meal_plans': meal_plans,
        'workout_programs': workout_programs,
        'payments': payments,
        'store_orders': store_orders,
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
def admin_update_order_status(request, order_id):
    from store.models import Order
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = ['pending', 'shipped', 'delivered', 'cancelled']
        if new_status in valid_statuses:
            order.status = new_status
            order.save(update_fields=['status'])
            messages.success(request, f"Order #{order.id} status updated to '{new_status}'.")
        else:
            messages.error(request, "Invalid status value.")
    return redirect('admin_dashboard')


@login_required
@role_required('admin')
def admin_delete_order(request, order_id):
    from store.models import Order
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, f"Order #{order_id} deleted successfully.")
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


# ─── Forgot Password Flow ─────────────────────────────────────────────────────

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        user = FitnessProfile.objects.filter(email=email).first()
        
        if user:
            otp_code = OTPVerification.generate_otp()
            OTPVerification.objects.filter(user=user).delete()
            OTPVerification.objects.create(
                user=user,
                otp_hash=OTPVerification.hash_otp(otp_code)
            )
            
            try:
                send_mail(
                    'FitX Password Reset OTP',
                    f'Your OTP to reset your FitX password is: {otp_code}\nThis OTP is valid for 5 minutes.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                request.session['reset_email'] = email
                messages.success(request, f"We've sent a password reset OTP to {email}.")
                return redirect('verify_reset_otp')
            except Exception as e:
                logger.error(f"Reset OTP failed: {e}")
                messages.error(request, "Failed to send reset email. Please try again.")
        else:
            messages.error(request, "No account found with this email.")
            
    return render(request, 'account/forgot_password.html')


def verify_reset_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
        
    user = get_object_or_404(FitnessProfile, email=email)
    
    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()
        verification = OTPVerification.objects.filter(user=user, is_used=False).last()
        
        if verification:
            success, msg = verification.verify(otp_entered)
            if success:
                request.session['otp_verified_for_reset'] = True
                messages.success(request, "OTP verified. You can now reset your password.")
                return redirect('reset_password')
            else:
                messages.error(request, msg)
        else:
            messages.error(request, "No valid OTP found. Please try again.")
            return redirect('forgot_password')
            
    return render(request, 'account/otp_verify_reset.html', {'email': email})


def reset_password(request):
    if not request.session.get('otp_verified_for_reset'):
        messages.error(request, "Please verify your email first.")
        return redirect('forgot_password')
        
    email = request.session.get('reset_email')
    user = get_object_or_404(FitnessProfile, email=email)
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not password or len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user.set_password(password)
            user.is_email_verified = True # Since they verified OTP to get here
            user.save()
            
            # Clean up session
            del request.session['reset_email']
            del request.session['otp_verified_for_reset']
            
            messages.success(request, "Password reset successfully. You can now login.")
            return redirect('login')
            
    return render(request, 'account/reset_password.html')

# ─── Native Admin Form Handling ─────────────────────────────────────────────

from django.utils.text import slugify

@login_required
@role_required('admin')
def admin_add_exercise(request):
    if request.method == 'POST':
        from workout.models import Exercise
        name = request.POST.get('name')
        category = request.POST.get('category')
        exercise_type = request.POST.get('exercise_type')
        difficulty = request.POST.get('difficulty')
        reps_sets = request.POST.get('reps_sets')
        calories_burned = request.POST.get('calories_burned', 0)
        video_url = request.POST.get('video_url', '')
        steps = request.POST.get('steps', '')
        
        Exercise.objects.create(
            name=name, category=category, exercise_type=exercise_type,
            difficulty=difficulty, reps_sets=reps_sets,
            calories_burned=calories_burned, video_url=video_url,
            steps=steps
        )
        messages.success(request, f"Exercise '{name}' added successfully.")
    return redirect('admin_dashboard')

@login_required
@role_required('admin')
def admin_edit_exercise(request, id):
    if request.method == 'POST':
        from workout.models import Exercise
        ex = get_object_or_404(Exercise, id=id)
        ex.name = request.POST.get('name', ex.name)
        ex.category = request.POST.get('category', ex.category)
        ex.exercise_type = request.POST.get('exercise_type', ex.exercise_type)
        ex.difficulty = request.POST.get('difficulty', ex.difficulty)
        ex.reps_sets = request.POST.get('reps_sets', ex.reps_sets)
        ex.calories_burned = request.POST.get('calories_burned', ex.calories_burned)
        ex.video_url = request.POST.get('video_url', ex.video_url)
        ex.steps = request.POST.get('steps', ex.steps)
        ex.save()
        messages.success(request, f"Exercise '{ex.name}' updated successfully.")
    return redirect('admin_dashboard')

@login_required
@role_required('admin')
def admin_delete_exercise(request, id):
    from workout.models import Exercise
    ex = get_object_or_404(Exercise, id=id)
    name = ex.name
    ex.delete()
    messages.success(request, f"Exercise '{name}' deleted successfully.")
    return redirect('admin_dashboard')

@login_required
@role_required('admin')
def admin_add_blogpost(request):
    if request.method == 'POST':
        from core.models import BlogPost
        title = request.POST.get('title')
        content = request.POST.get('content')
        status = request.POST.get('status', 'draft')
        
        post = BlogPost(
            title=title,
            content=content,
            status=status,
            author=request.user
        )
        if not post.slug:
            post.slug = slugify(title)
        
        if status == 'published':
            post.published_at = timezone.now()
            
        post.save()
        messages.success(request, f"Blog post '{title}' created successfully.")
    return redirect('admin_dashboard')

@login_required
@role_required('admin')
def admin_edit_blogpost(request, id):
    if request.method == 'POST':
        from core.models import BlogPost
        post = get_object_or_404(BlogPost, id=id)
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)
        new_status = request.POST.get('status', post.status)
        
        if post.status != 'published' and new_status == 'published':
            post.published_at = timezone.now()
            
        post.status = new_status
        post.save()
        messages.success(request, f"Blog post '{post.title}' updated successfully.")
    return redirect('admin_dashboard')

@login_required
@role_required('admin')
def admin_delete_blogpost(request, id):
    from core.models import BlogPost
    post = get_object_or_404(BlogPost, id=id)
    title = post.title
    post.delete()
    messages.success(request, f"Blog post '{title}' deleted successfully.")
    return redirect('admin_dashboard')

@login_required
@role_required('admin')
def admin_add_challenge(request):
    if request.method == 'POST':
        from core.models import Challenge
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        difficulty = request.POST.get('difficulty')
        status = request.POST.get('status', 'upcoming')
        
        Challenge.objects.create(
            title=title, description=description,
            start_date=start_date, end_date=end_date,
            difficulty=difficulty, status=status,
            created_by=request.user
        )
        messages.success(request, f"Challenge '{title}' added successfully.")
    return redirect('admin_dashboard')

@login_required
@role_required('admin')
def admin_edit_challenge(request, id):
    if request.method == 'POST':
        from core.models import Challenge
        ch = get_object_or_404(Challenge, id=id)
        ch.title = request.POST.get('title', ch.title)
        ch.description = request.POST.get('description', ch.description)
        ch.start_date = request.POST.get('start_date', ch.start_date)
        ch.end_date = request.POST.get('end_date', ch.end_date)
        ch.difficulty = request.POST.get('difficulty', ch.difficulty)
        ch.status = request.POST.get('status', ch.status)
        ch.save()
        messages.success(request, f"Challenge '{ch.title}' updated successfully.")
    return redirect('admin_dashboard')

@login_required
@role_required('admin')
def admin_delete_challenge(request, id):
    from core.models import Challenge
    ch = get_object_or_404(Challenge, id=id)
    title = ch.title
    ch.delete()
    messages.success(request, f"Challenge '{title}' deleted successfully.")
    return redirect('admin_dashboard')

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
