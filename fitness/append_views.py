import os

filepath = r"c:\Users\Dev\Desktop\FITNESS\env\fitness\account\views.py"

with open(filepath, 'a', encoding='utf-8') as f:
    f.write("""
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
""")

print("Successfully appended views.")
