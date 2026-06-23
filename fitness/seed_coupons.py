import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness.settings')
django.setup()

from store.models import Coupon
from django.utils import timezone
from datetime import timedelta

def seed_coupons():
    coupons = [
        {'code': 'FIT10', 'discount_percent': 10},
        {'code': 'SUPERSALE25', 'discount_percent': 25},
        {'code': 'NEWATHLETE', 'discount_percent': 15},
        {'code': 'STAYFIT50', 'discount_percent': 50},
        {'code': 'WELLNESS05', 'discount_percent': 5},
    ]

    for data in coupons:
        coupon, created = Coupon.objects.get_or_create(
            code=data['code'].upper(),
            defaults={
                'discount_percent': data['discount_percent'],
                'active': True,
                'valid_from': timezone.now(),
                'valid_to': timezone.now() + timedelta(days=365)
            }
        )
        if created:
            print(f"Created coupon: {data['code']}")
        else:
            print(f"Coupon already exists: {data['code']}")

if __name__ == '__main__':
    seed_coupons()
