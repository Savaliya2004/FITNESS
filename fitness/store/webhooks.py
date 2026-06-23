"""
Razorpay webhook handler — server-to-server payment verification.
Replaces the insecure @csrf_exempt frontend callback.
"""
import json
import hmac
import hashlib
import logging

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from .models import Payment

logger = logging.getLogger('fitx.payments')


@csrf_exempt  # Webhooks don't have CSRF tokens — we verify by signature instead
@require_POST
def razorpay_webhook(request):
    """
    Razorpay server-to-server webhook.
    This is the ONLY reliable way to confirm payment.
    """
    webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', '')

    if not webhook_secret:
        logger.error("RAZORPAY_WEBHOOK_SECRET not configured")
        return HttpResponseBadRequest("Webhook not configured")

    # Step 1: Verify webhook signature
    signature = request.headers.get('X-Razorpay-Signature', '')

    expected = hmac.new(
        webhook_secret.encode('utf-8'),
        request.body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        logger.warning(f"Invalid webhook signature from {request.META.get('REMOTE_ADDR')}")
        return HttpResponseBadRequest("Invalid signature")

    # Step 2: Parse event
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    event = payload.get('event')
    logger.info(f"Razorpay webhook received: {event}")

    # Step 3: Handle events
    if event == 'payment.captured':
        payment_entity = payload['payload']['payment']['entity']
        order_id = payment_entity.get('order_id')
        payment_id = payment_entity.get('id')

        payment = Payment.objects.filter(razorpay_order_id=order_id).first()
        if payment and payment.status != 'success':
            payment.razorpay_payment_id = payment_id
            payment.status = 'success'
            payment.save()

            # Activate subscription
            if payment.membership:
                from .services import SubscriptionService
                SubscriptionService.activate_subscription(
                    payment.user, payment.membership, payment
                )
            logger.info(f"Payment captured: {order_id} → {payment_id}")

    elif event == 'payment.failed':
        payment_entity = payload['payload']['payment']['entity']
        order_id = payment_entity.get('order_id')
        payment = Payment.objects.filter(razorpay_order_id=order_id).first()
        if payment:
            payment.status = 'failed'
            payment.save()
            logger.warning(f"Payment failed: {order_id}")

    return JsonResponse({'status': 'ok'})
