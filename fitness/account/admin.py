from django.contrib import admin
from django.contrib import messages
from .models import FitnessProfile
from diet.recommender import generate_7day_plan

@admin.register(FitnessProfile)
class FitnessProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'fitness_goal', 'membership_type', 'is_active')
    list_filter = ('fitness_goal', 'membership_type', 'is_active')
    search_fields = ('username', 'email')
    actions = ['generate_diet_plan_for_users']

    @admin.action(description='Generate 7-Day Diet Plan for selected users')
    def generate_diet_plan_for_users(self, request, queryset):
        success_count = 0
        for user in queryset:
            days = generate_7day_plan(user)
            if days:
                success_count += 1
        
        if success_count > 0:
            self.message_user(request, f'Successfully generated diet plans for {success_count} user(s).', messages.SUCCESS)
        else:
            self.message_user(request, 'Failed to generate plans. Make sure there are enough active meals in the database.', messages.ERROR)
