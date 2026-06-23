from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ClassSchedule, Booking
from .services import BookingService
from core.decorators import role_required


def class_schedule(request):
    """View to list upcoming class schedules."""
    # Show active classes from today onwards
    schedules = ClassSchedule.objects.filter(
        date__gte=timezone.now().date(),
        status='scheduled'
    ).select_related('class_type', 'center', 'trainer').order_by('date', 'start_time')
    
    # If authenticated, get user's active bookings
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(
            user=request.user, 
            status__in=['confirmed', 'waitlisted']
        )
        booking_map = {b.schedule_id: b.id for b in bookings}
        
        for schedule in schedules:
            schedule.user_booking_id = booking_map.get(schedule.id, None)

    context = {
        'schedules': schedules,
    }
    return render(request, 'booking/schedule.html', context)


@login_required
def book_class(request, schedule_id):
    """Endpoint to book a class using BookingService."""
    if request.method == 'POST':
        schedule = get_object_or_404(ClassSchedule, id=schedule_id)
        try:
            booking = BookingService.book_class(request.user, schedule)
            if booking.status == 'waitlisted':
                messages.warning(request, f"Class is full. You've been added to the waitlist (Position {booking.waitlist_position}).")
            else:
                messages.success(request, f"Successfully booked {schedule.class_type.name} on {schedule.date}!")
        except ValueError as e:
            messages.error(request, str(e))
    
    return redirect('schedule')


@login_required
def cancel_booking(request, booking_id):
    """Endpoint to cancel a booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        try:
            BookingService.cancel_booking(booking)
            messages.success(request, "Your booking was successfully cancelled.")
        except ValueError as e:
            messages.error(request, str(e))
            
    # Typically would redirect back to user's dashboard or schedule
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
