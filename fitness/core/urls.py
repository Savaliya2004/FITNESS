from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('success_stories/', views.success_stories),  
    path('story/', views.story_detail, name='story_detail'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('faq/', views.faq_page, name='faq'),
    path('custom-admin/', views.custom_admin, name='custom_admin'),
    path('challenges/', views.challenges_list, name='challenges_list'),
    path('challenges/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('challenges/<int:challenge_id>/join/', views.join_challenge, name='join_challenge'),
    path('challenges/task/<int:task_id>/log/', views.log_task, name='log_challenge_task'),
]
