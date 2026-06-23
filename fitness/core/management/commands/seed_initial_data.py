"""Seed initial data: FAQs, Membership Plans."""
from django.core.management.base import BaseCommand
from core.models import FAQ
from store.models import MembershipPlan


class Command(BaseCommand):
    help = 'Seed initial data: FAQs, Membership Plans. Run once after migrations.'

    def handle(self, *args, **options):
        self._seed_faqs()
        self._seed_plans()
        self.stdout.write(self.style.SUCCESS('[SUCCESS] Initial data seeded successfully'))

    def _seed_faqs(self):
        faqs = [
            ("What makes FitX different from other gyms?",
             "FitX is a holistic fitness ecosystem with world-class facilities, nutrition coaching, mental wellness programs, and a vibrant community.", 1),
            ("Can I access multiple centers with one membership?",
             "Yes! Our 'FitX Elite' plan gives you seamless access to every FitX center and partner gym across the country.", 2),
            ("Are personal trainers available?",
             "Absolutely. We have elite, certified trainers specialized in bodybuilding, CrossFit, Yoga, and athletic conditioning.", 3),
            ("Do you have a mobile app?",
             "Yes, the FitX app is available on both iOS and Android. Book classes, track nutrition, and monitor progress on the go.", 4),
            ("Is there a trial period?",
             "Yes, we offer a 3-day complimentary pass for all first-time visitors.", 5),
            ("What are your opening hours?",
             "Premium centers are open 24/7. Standard centers operate from 5:00 AM to 11:00 PM.", 6),
            ("Do you offer student discounts?",
             "Yes, special rates for students under 25 with valid ID.", 7),
        ]
        created = 0
        for q, a, order in faqs:
            _, was_created = FAQ.objects.get_or_create(
                question=q, defaults={'answer': a, 'order': order}
            )
            if was_created:
                created += 1
        self.stdout.write(f'  FAQs: {created} created')

    def _seed_plans(self):
        plans = [
            ('Basic Plan', 'free', 0, 30, 'Browse Exercises\nTrack Limited Progress\nAccess Community'),
            ('Premium', 'premium', 999, 30, 'Unlimited Workouts\nPersonalized Diet Plan\nProgress Tracking\nChat Support'),
            ('Elite', 'elite', 1999, 30, 'Everything in Premium\nPersonal Trainer\nNutrition Consultation\nPriority Support\nAll Centers Access'),
        ]
        created = 0
        for name, ptype, price, days, features in plans:
            _, was_created = MembershipPlan.objects.get_or_create(
                plan_type=ptype,
                defaults={'name': name, 'price': price, 'duration_days': days, 'features': features}
            )
            if was_created:
                created += 1
        self.stdout.write(f'  Membership Plans: {created} created')
