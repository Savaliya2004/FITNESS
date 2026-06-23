from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ChatRoom, ChatMessage, SupportTicket

@login_required
def chat_inbox(request):
    """View to list all chat rooms for a user (tickets, trainer chats)."""
    user_rooms = request.user.chat_rooms.all()
    tickets = SupportTicket.objects.filter(user=request.user)
    
    return render(request, 'chat/inbox.html', {
        'rooms': user_rooms,
        'tickets': tickets,
    })

@login_required
def chat_room(request, room_id):
    """View for an individual chat room."""
    # Ensure user is a participant
    room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)
    messages = room.messages.all().order_by('created_at')
    
    # Mark messages as read
    room.messages.exclude(sender=request.user).update(is_read=True, read_at=timezone.now())
    
    return render(request, 'chat/room.html', {
        'room': room,
        'chat_messages': messages,
    })

@login_required
def send_message(request, room_id):
    """Endpoint to send a new message in a room."""
    if request.method == 'POST':
        room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)
        content = request.POST.get('content')
        
        if content:
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                content=content
            )
            # Update room metadata
            room.last_message_text = content[:195]
            room.last_message_at = timezone.now()
            room.last_message_by = request.user
            room.save()
            
    return redirect('chat:room', room_id=room_id)

@login_required
def create_ticket(request):
    """Endpoint to create a new support ticket."""
    if request.method == 'POST':
        subject = request.POST.get('subject')
        category = request.POST.get('category')
        priority = request.POST.get('priority')
        description = request.POST.get('description')
        
        if subject and description:
            # 1. Create a Chat Room
            room = ChatRoom.objects.create(
                room_type='support',
                name=f"Ticket: {subject}",
            )
            room.participants.add(request.user)
            
            # (Optional) Auto-assign admin agents to to room. 
            # In a real system, you'd find a support user and add them.
            
            # 2. Create the ticket
            SupportTicket.objects.create(
                user=request.user,
                chat_room=room,
                subject=subject,
                category=category,
                priority=priority,
            )
            
            # 3. Add initial message
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                content=description
            )
            
            messages.success(request, "Ticket created successfully! A support agent will respond shortly.")
            return redirect('chat:room', room_id=room.id)
            
    return redirect('chat:inbox')
