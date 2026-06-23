from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_inbox, name='inbox'),
    path('room/<int:room_id>/', views.chat_room, name='room'),
    path('room/<int:room_id>/send/', views.send_message, name='send_message'),
    path('ticket/create/', views.create_ticket, name='create_ticket'),
]
