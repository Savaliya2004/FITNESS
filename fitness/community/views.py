from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CommunityPost, PostLike
from core.models import Challenge
from account.models import FitnessProfile

def community_feed(request):
    """View to load the community social feed."""
    posts = CommunityPost.objects.select_related('author').prefetch_related('likes').order_by('-is_pinned', '-created_at')[:50]
    challenges = Challenge.objects.filter(status='active')[:5]
    
    # Calculate top users
    top_users = FitnessProfile.objects.order_by('-xp_points')[:5]

    context = {
        'posts': posts,
        'challenges': challenges,
        'top_users': top_users,
    }
    return render(request, 'core/community.html', context)


@login_required
def create_post(request):
    """Endpoint to create a new community post."""
    if request.method == 'POST':
        content = request.POST.get('content')
        post_type = request.POST.get('post_type', 'discussion')
        if content:
            CommunityPost.objects.create(
                author=request.user,
                content=content,
                post_type=post_type
            )
            messages.success(request, "Your post is live! 🚀")
        else:
            messages.error(request, "Post content cannot be empty.")
            
    return redirect('community')


@login_required
def like_post(request, post_id):
    """Toggle like on a post."""
    post = get_object_or_404(CommunityPost, id=post_id)
    like, created = PostLike.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        post.likes_count -= 1
    else:
        post.likes_count += 1
        
    post.save()
    return redirect(request.META.get('HTTP_REFERER', 'community'))
