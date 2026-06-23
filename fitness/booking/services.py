"""
BookingService — handles atomic seat management, waitlists, and cancellations.
"""
import logging
from django.db import transaction
from django.utils import timezone

from .models import Booking, ClassSchedule, Waitlist

logger = logging.getLogger('fitx')


class BookingService:

    @staticmethod
    @transaction.atomic
    def create_booking(user, schedule_id):
        """
        Atomically book a seat or add to waitlist.
        Uses select_for_update to prevent race conditions.
        Returns: (booking, message)
        """
        schedule = (
            ClassSchedule.objects
            .select_for_update()
            .get(id=schedule_id)
        )

        # Check if user already has a booking
        existing = Booking.objects.filter(
            user=user, class_schedule=schedule
        ).exclude(status='cancelled').first()

        if existing:
            raise ValueError("You already have a booking for this class.")

        if schedule.status == 'cancelled':
            raise ValueError("This class has been cancelled.")

        if schedule.available_seats > 0:
            # BOOK directly
            schedule.current_bookings += 1
            schedule.save(update_fields=['current_bookings'])

            booking = Booking.objects.create(
                user=user,
                class_schedule=schedule,
                status='confirmed',
            )
            logger.info(f"Booking confirmed: {user.username} → {schedule}")

            # Send notification
            try:
                from notifications.services import NotificationService
                NotificationService.send(user, 'booking_confirmed', {
                    'class_name': schedule.class_type.name,
                    'date': str(schedule.date),
                    'time': schedule.start_time.strftime('%I:%M %p'),
                })
            except Exception:
                pass

            return booking, "Booking confirmed!"

        else:
            # WAITLIST
            waitlist_pos = Waitlist.objects.filter(class_schedule=schedule).count() + 1
            Waitlist.objects.create(
                user=user,
                class_schedule=schedule,
                position=waitlist_pos,
            )
            booking = Booking.objects.create(
                user=user,
                class_schedule=schedule,
                status='waitlisted',
                waitlist_position=waitlist_pos,
            )
            logger.info(f"Waitlisted #{waitlist_pos}: {user.username} → {schedule}")
            return booking, f"Class is full. You're #{waitlist_pos} on the waitlist."

    @staticmethod
    @transaction.atomic
    def cancel_booking(booking_id, user, reason=''):
        """
        Cancel booking with refund calculation.
        Auto-promotes next waitlisted user.
        Returns: (booking, refund_amount)
        """
        booking = (
            Booking.objects
            .select_for_update()
            .get(id=booking_id, user=user)
        )

        if booking.status in ('cancelled', 'attended', 'no_show'):
            raise ValueError(f"Cannot cancel a {booking.status} booking.")

        schedule = (
            ClassSchedule.objects
            .select_for_update()
            .get(id=booking.class_schedule_id)
        )

        was_confirmed = booking.status == 'confirmed'

        # Calculate refund
        refund = 0.0
        if booking.amount_paid > 0:
            hours_until = (
                timezone.datetime.combine(schedule.date, schedule.start_time) -
                timezone.now().replace(tzinfo=None)
            ).total_seconds() / 3600

            if hours_until >= 12:
                refund = float(booking.amount_paid)  # Full refund
            elif hours_until >= 4:
                refund = float(booking.amount_paid) * 0.50  # 50% refund
            # < 4 hours = no refund

        booking.status = 'cancelled'
        booking.cancelled_at = timezone.now()
        booking.cancellation_reason = reason
        booking.refund_amount = refund
        booking.save()

        if was_confirmed:
            schedule.current_bookings = max(0, schedule.current_bookings - 1)
            schedule.save(update_fields=['current_bookings'])

            # Auto-promote from waitlist
            BookingService._promote_from_waitlist(schedule)

        # Clean up waitlist entry
        Waitlist.objects.filter(user=user, class_schedule=schedule).delete()

        logger.info(f"Booking cancelled: {user.username} → {schedule}, refund: ₹{refund}")
        return booking, refund

    @staticmethod
    def _promote_from_waitlist(schedule):
        """Promote next person from waitlist to confirmed."""
        next_in_line = (
            Waitlist.objects
            .filter(class_schedule=schedule)
            .order_by('position')
            .first()
        )

        if next_in_line:
            booking = Booking.objects.filter(
                user=next_in_line.user,
                class_schedule=schedule,
                status='waitlisted'
            ).first()

            if booking:
                booking.status = 'confirmed'
                booking.waitlist_position = None
                booking.save()

                schedule.current_bookings += 1
                schedule.save(update_fields=['current_bookings'])

                next_in_line.delete()

                logger.info(f"Waitlist promoted: {booking.user.username} → {schedule}")

                try:
                    from notifications.services import NotificationService
                    NotificationService.send(booking.user, 'booking_confirmed', {
                        'class_name': schedule.class_type.name,
                        'date': str(schedule.date),
                        'time': schedule.start_time.strftime('%I:%M %p'),
                    })
                except Exception:
                    pass
