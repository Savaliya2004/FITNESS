from celery import shared_task
from .services import SubscriptionService
import logging

logger = logging.getLogger('fitx')

@shared_task
def check_expired_subscriptions():
    """Daily chron job to expire subscriptions and downgrade memberships."""
    logger.info("Running daily check for expired subscriptions...")
    SubscriptionService.check_and_expire_subscriptions()
    logger.info("Finished expiring subscriptions.")
