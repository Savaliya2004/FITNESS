"""
SubscriptionService — manages full subscription lifecycle.
"""
import uuid
import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import Subscription, Invoice

logger = logging.getLogger('fitx')


class SubscriptionService:

    @staticmethod
    @transaction.atomic
    def activate_subscription(user, plan, payment):
        """Called after successful payment verification."""
        now = timezone.now()

        existing = Subscription.objects.filter(
            user=user, status='active'
        ).select_for_update().first()

        if existing:
            if existing.plan == plan:
                # RENEWAL — extend expiry date
                existing.expires_at = existing.expires_at + timedelta(days=plan.duration_days)
                existing.last_payment = payment
                existing.next_billing_date = (existing.expires_at - timedelta(days=3)).date()
                existing.save()
                subscription = existing
            else:
                # UPGRADE/DOWNGRADE
                existing.status = 'cancelled'
                existing.cancelled_at = now
                existing.cancellation_reason = f"Switched to {plan.name}"
                existing.save()
                subscription = Subscription.objects.create(
                    user=user, plan=plan, status='active',
                    starts_at=now,
                    expires_at=now + timedelta(days=plan.duration_days),
                    last_payment=payment,
                    next_billing_date=(now + timedelta(days=plan.duration_days - 3)).date(),
                )
        else:
            subscription = Subscription.objects.create(
                user=user, plan=plan, status='active',
                starts_at=now,
                expires_at=now + timedelta(days=plan.duration_days),
                last_payment=payment,
                next_billing_date=(now + timedelta(days=plan.duration_days - 3)).date(),
            )

        # Update user membership
        user.membership_type = plan.plan_type
        user.membership_expires_at = subscription.expires_at
        user.save(update_fields=['membership_type', 'membership_expires_at'])

        # Generate invoice
        SubscriptionService._generate_invoice(user, payment, plan)

        logger.info(f"Subscription activated: {user.username} → {plan.name}")
        return subscription

    @staticmethod
    def _generate_invoice(user, payment, plan):
        tax_rate = 0.18  # 18% GST
        base_amount = float(payment.amount) / (1 + tax_rate)
        tax_amount = float(payment.amount) - base_amount

        Invoice.objects.create(
            user=user,
            payment=payment,
            invoice_number=f"FTX-{timezone.now().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}",
            amount=round(base_amount, 2),
            tax_amount=round(tax_amount, 2),
            total_amount=payment.amount,
            description=f"{plan.name} Membership — {plan.duration_days} days",
        )

    @staticmethod
    def check_and_expire_subscriptions():
        """Expire subscriptions past their expiry date."""
        now = timezone.now()
        expired = Subscription.objects.filter(status='active', expires_at__lte=now)

        count = 0
        for sub in expired:
            sub.status = 'expired'
            sub.save(update_fields=['status'])

            sub.user.membership_type = 'free'
            sub.user.membership_expires_at = None
            sub.user.save(update_fields=['membership_type', 'membership_expires_at'])
            count += 1

        if count:
            logger.info(f"Expired {count} subscriptions")
