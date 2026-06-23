from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_feed, name='community'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
]
