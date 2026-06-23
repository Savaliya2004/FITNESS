from django.contrib import admin
from .models import BlogPost, Challenge, Testimonial, SuccessStory, FAQ, ContactMessage


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('created_at',)


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'reward')
    search_fields = ('title', 'description')
    list_filter = ('start_date', 'end_date')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('rating',)


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'result_stat', 'is_gain', 'created_at')
    search_fields = ('name', 'brief')
    list_filter = ('is_gain',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    search_fields = ('question', 'answer')
    list_editable = ('order',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'topic', 'is_resolved', 'created_at')
    search_fields = ('name', 'email', 'message', 'topic')
    list_filter = ('is_resolved', 'topic', 'created_at')
    list_editable = ('is_resolved',)
