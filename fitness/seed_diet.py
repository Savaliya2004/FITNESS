
from diet.models import MealPlan
from account.models import FitnessProfile

def seed():
    # Deficit Plan (approx 1600-1800 kcal)
    plan_data = [
        {
            'day': 'monday',
            'bf': 'Rolled Oats with Berries & Honey',
            'lu': 'Grilled Chicken Breast with Quinoa & Steamed Spinach',
            'dn': 'Baked Salmon with Sweet Potato & Broccoli',
            'sn': 'Greek Yogurt with a handful of Walnuts',
            'cal': 1650, 'pro': 140, 'car': 150, 'fat': 50
        },
        {
            'day': 'tuesday',
            'bf': '3 Scrambled Eggs with Avocado & Toast',
            'lu': 'Turkey Breast Sandwich (Whole wheat) with side Salad',
            'dn': 'Lean Beef Stir-fry with Peppers & Brown Rice',
            'sn': 'Apple with 1 tbsp Almond Butter',
            'cal': 1720, 'pro': 130, 'car': 170, 'fat': 60
        },
        {
            'day': 'wednesday',
            'bf': 'Protein Smoothie: Whey, Banana, Spinach, Milk',
            'lu': 'Lentil Soup with Whole Grain Croutons',
            'dn': 'Grilled Cod with Asparagus & Mashed Cauliflower',
            'sn': 'Cottage Cheese with Pineapple chunks',
            'cal': 1580, 'pro': 125, 'car': 140, 'fat': 45
        },
        {
            'day': 'thursday',
            'bf': 'Poached Eggs on Rye Bread with Tomato',
            'lu': 'Chickpea & Bell Pepper Salad with Lemon Zest',
            'dn': 'Roasted Chicken Thighs (skinless) with Green Beans',
            'sn': 'Small protein bar (low sugar)',
            'cal': 1690, 'pro': 135, 'car': 160, 'fat': 55
        },
        {
            'day': 'friday',
            'bf': 'Chia Seed Pudding with Almond Milk',
            'lu': 'Tuna Salad Wrap (Whole wheat) with Lettuce',
            'dn': 'Turkey Meatballs with Zucchini Noodles & Tomato sauce',
            'sn': 'Boiled Egg & handful of Almonds',
            'cal': 1620, 'pro': 145, 'car': 130, 'fat': 50
        },
        {
            'day': 'saturday',
            'bf': 'Greek Yogurt with Granola & Raspberries',
            'lu': 'Stir-fried Tofu with Bok Choy & Ginger',
            'dn': 'Grilled Steak with sautéed Mushrooms',
            'sn': 'Orange or Pear',
            'cal': 1750, 'pro': 130, 'car': 180, 'fat': 65
        },
        {
            'day': 'sunday',
            'bf': 'Whole Grain Pancakes with Maple Syrup (limit)',
            'lu': 'Veggie & Bean Burrito bowl',
            'dn': 'Shrimp Skewers with Grilled Peppers',
            'sn': 'Dark Chocolate (1-2 squares)',
            'cal': 1680, 'pro': 120, 'car': 165, 'fat': 55
        }
    ]

    users = FitnessProfile.objects.all()
    for user in users:
        # Clear existing to ensure fresh start
        MealPlan.objects.filter(user=user).delete()
        for p in plan_data:
            MealPlan.objects.create(
                user=user,
                day_of_week=p['day'],
                meal_name="Deficit Plan",
                breakfast=p['bf'],
                lunch=p['lu'],
                dinner=p['dn'],
                snacks=p['sn'],
                calories=p['cal'],
                protein=p['pro'],
                carbs=p['car'],
                fats=p['fat']
            )
    print(f"Successfully seeded deficit diet plans for {users.count()} users.")

if __name__ == "__main__":
    seed()
