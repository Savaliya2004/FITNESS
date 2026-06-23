"""
Seed script — populate the Meal table with a rich library of meals.
Run from within the Django shell:
    python manage.py shell -c "exec(open('seed_meals.py').read())"
OR as a management command after importing.

Covers: breakfast / lunch / dinner / snack
        veg / egg / nonveg
        all major goal tags
"""

import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness.settings')
django.setup()

from diet.models import Meal

MEALS = [
    # ── BREAKFAST – VEG ──────────────────────────────────────────
    dict(name="Masala Oats with Vegetables", meal_type="breakfast", dietary_type="veg",
         goal_tag="weight_loss", calories=320, protein=12, carbs=48, fats=8, fiber=6,
         description="Rolled oats cooked with onion, tomato, cumin & herbs. Light and filling."),
    dict(name="Moong Dal Chilla with Mint Chutney", meal_type="breakfast", dietary_type="veg",
         goal_tag="weight_loss", calories=280, protein=14, carbs=38, fats=6, fiber=5,
         description="2 crisp lentil pancakes served with fresh mint-coriander chutney."),
    dict(name="Paneer Bhurji with Multigrain Toast", meal_type="breakfast", dietary_type="veg",
         goal_tag="muscle_gain", calories=480, protein=32, carbs=38, fats=18, fiber=4,
         description="Spiced cottage cheese scramble with capsicum & onion on 2 slices of toast."),
    dict(name="Chia Seed Pudding with Berries", meal_type="breakfast", dietary_type="veg",
         goal_tag="fat_loss", calories=310, protein=10, carbs=36, fats=12, fiber=8,
         description="Almond milk chia pudding topped with fresh strawberries and blueberries."),
    dict(name="Banana Oat Smoothie", meal_type="breakfast", dietary_type="veg",
         goal_tag="endurance", calories=360, protein=12, carbs=60, fats=6, fiber=5,
         description="Blended oats, banana, almond milk & honey. Great pre-workout fuel."),
    dict(name="Greek Yogurt Parfait with Granola", meal_type="breakfast", dietary_type="veg",
         goal_tag="any", calories=400, protein=20, carbs=48, fats=11, fiber=4,
         description="Low-fat Greek yogurt layered with oat granola and seasonal fruit."),
    dict(name="Poha with Peanuts", meal_type="breakfast", dietary_type="veg",
         goal_tag="maintenance", calories=340, protein=10, carbs=52, fats=9, fiber=4,
         description="Light flattened rice seasoned with mustard seeds, curry leaves & roasted peanuts."),
    dict(name="Whole Grain Upma", meal_type="breakfast", dietary_type="veg",
         goal_tag="general_fitness", calories=320, protein=9, carbs=50, fats=8, fiber=5,
         description="Semolina porridge with mixed vegetables, cashews & tempering."),
    dict(name="High-Protein Soy Shake", meal_type="breakfast", dietary_type="veg",
         goal_tag="muscle_gain", calories=420, protein=40, carbs=28, fats=10, fiber=2,
         description="Soy protein shake blended with milk, oats, and a banana."),
    dict(name="Avocado Toast with Seeds", meal_type="breakfast", dietary_type="veg",
         goal_tag="fat_loss", calories=380, protein=10, carbs=34, fats=22, fiber=7,
         description="Multigrain toast topped with mashed avocado, chia & flaxseeds."),

    # ── BREAKFAST – EGG ───────────────────────────────────────────
    dict(name="Spinach & Egg White Omelette", meal_type="breakfast", dietary_type="egg",
         goal_tag="fat_loss", calories=220, protein=20, carbs=6, fats=10, fiber=2,
         description="3-egg-white omelette packed with spinach, mushrooms & a sprinkle of feta."),
    dict(name="Boiled Eggs with Rye Toast", meal_type="breakfast", dietary_type="egg",
         goal_tag="weight_loss", calories=300, protein=22, carbs=28, fats=10, fiber=4,
         description="2 hard-boiled eggs alongside 2 slices of seeded rye bread."),
    dict(name="Shakshuka (2 eggs)", meal_type="breakfast", dietary_type="egg",
         goal_tag="maintenance", calories=380, protein=22, carbs=30, fats=18, fiber=5,
         description="Eggs poached in a spiced tomato-capsicum sauce. Served with pita."),
    dict(name="Scrambled Eggs with Avocado", meal_type="breakfast", dietary_type="egg",
         goal_tag="muscle_gain", calories=480, protein=28, carbs=14, fats=34, fiber=5,
         description="3 scrambled eggs on toast with half an avocado and chilli flakes."),
    dict(name="Egg & Veggie Breakfast Wrap", meal_type="breakfast", dietary_type="egg",
         goal_tag="general_fitness", calories=420, protein=24, carbs=40, fats=16, fiber=5,
         description="Whole-wheat wrap filled with scrambled eggs, peppers & salsa."),

    # ── BREAKFAST – NON-VEG ───────────────────────────────────────
    dict(name="Smoked Salmon with Cream Cheese Toast", meal_type="breakfast", dietary_type="nonveg",
         goal_tag="fat_loss", calories=340, protein=24, carbs=26, fats=14, fiber=2,
         description="80g smoked salmon on whole-grain toast with light cream cheese & capers."),
    dict(name="Chicken Sausage Scramble", meal_type="breakfast", dietary_type="nonveg",
         goal_tag="muscle_gain", calories=560, protein=38, carbs=30, fats=26, fiber=2,
         description="2 chicken sausages with 3 scrambled eggs and whole-grain toast."),
    dict(name="Turkey Bacon & Egg Muffin", meal_type="breakfast", dietary_type="nonveg",
         goal_tag="weight_loss", calories=310, protein=26, carbs=22, fats=12, fiber=2,
         description="A lean turkey bacon & egg sandwich on a whole-wheat English muffin."),

    # ── LUNCH – VEG ───────────────────────────────────────────────
    dict(name="Dal Tadka with Brown Rice", meal_type="lunch", dietary_type="veg",
         goal_tag="any", calories=520, protein=22, carbs=80, fats=10, fiber=10,
         description="Yellow lentil curry with a cumin-ghee tadka, served with 1 cup brown rice."),
    dict(name="Paneer Tikka Salad Bowl", meal_type="lunch", dietary_type="veg",
         goal_tag="fat_loss", calories=420, protein=28, carbs=22, fats=22, fiber=6,
         description="Grilled paneer cubes on a bed of quinoa, cucumber, cherry tomatoes & tahini."),
    dict(name="Rajma Chawal", meal_type="lunch", dietary_type="veg",
         goal_tag="muscle_gain", calories=650, protein=26, carbs=100, fats=12, fiber=12,
         description="Kidney bean curry with 1.5 cups brown rice and a side of cucumber raita."),
    dict(name="Tofu Stir-Fry with Broccoli & Brown Rice", meal_type="lunch", dietary_type="veg",
         goal_tag="weight_loss", calories=440, protein=24, carbs=55, fats=14, fiber=8,
         description="Pan-fried tofu with ginger-garlic broccoli stir-fry on brown rice."),
    dict(name="Chana Masala with Roti", meal_type="lunch", dietary_type="veg",
         goal_tag="endurance", calories=580, protein=22, carbs=88, fats=12, fiber=14,
         description="Spiced chickpea curry served with 3 whole-wheat chapatis."),
    dict(name="Quinoa Buddha Bowl", meal_type="lunch", dietary_type="veg",
         goal_tag="general_fitness", calories=490, protein=18, carbs=64, fats=16, fiber=9,
         description="Quinoa with roasted sweet potato, avocado, edamame & lemon-tahini dressing."),
    dict(name="Veggie & Paneer Wrap", meal_type="lunch", dietary_type="veg",
         goal_tag="maintenance", calories=500, protein=24, carbs=58, fats=18, fiber=6,
         description="Whole-wheat wrap with grilled paneer, roasted peppers, hummus & greens."),
    dict(name="Lentil Soup with Multigrain Bread", meal_type="lunch", dietary_type="veg",
         goal_tag="weight_loss", calories=380, protein=18, carbs=52, fats=8, fiber=10,
         description="Thick red lentil soup with cumin & lemon, served with 2 grain bread slices."),

    # ── LUNCH – EGG ───────────────────────────────────────────────
    dict(name="Egg Curry with Brown Rice", meal_type="lunch", dietary_type="egg",
         goal_tag="maintenance", calories=580, protein=30, carbs=70, fats=18, fiber=6,
         description="2 boiled eggs in a rich onion-tomato masala with 1 cup brown rice."),
    dict(name="Egg Fried Rice", meal_type="lunch", dietary_type="egg",
         goal_tag="muscle_gain", calories=640, protein=26, carbs=90, fats=18, fiber=4,
         description="Wok-tossed brown rice with 3 eggs, carrots, peas & soy sauce."),
    dict(name="Egg & Veggie Grain Bowl", meal_type="lunch", dietary_type="egg",
         goal_tag="fat_loss", calories=420, protein=26, carbs=44, fats=14, fiber=7,
         description="Farro base with 2 boiled eggs, massaged kale, roasted beetroot & mustard dressing."),

    # ── LUNCH – NON-VEG ───────────────────────────────────────────
    dict(name="Grilled Chicken Breast with Quinoa", meal_type="lunch", dietary_type="nonveg",
         goal_tag="muscle_gain", calories=620, protein=52, carbs=54, fats=14, fiber=5,
         description="180g grilled chicken breast with 1 cup quinoa and steamed broccoli."),
    dict(name="Baked Salmon with Sweet Potato", meal_type="lunch", dietary_type="nonveg",
         goal_tag="fat_loss", calories=560, protein=40, carbs=46, fats=20, fiber=5,
         description="160g baked salmon fillet with mashed sweet potato and sautéed spinach."),
    dict(name="Chicken Caesar Salad", meal_type="lunch", dietary_type="nonveg",
         goal_tag="weight_loss", calories=420, protein=38, carbs=18, fats=20, fiber=4,
         description="Grilled chicken strips on romaine with parmesan, croutons & light Caesar dressing."),
    dict(name="Tuna Wrap", meal_type="lunch", dietary_type="nonveg",
         goal_tag="fat_loss", calories=380, protein=32, carbs=36, fats=10, fiber=4,
         description="Whole-wheat wrap with tuna, avocado, lettuce, tomato & Dijon mustard."),
    dict(name="Chicken Biryani (Brown Rice)", meal_type="lunch", dietary_type="nonveg",
         goal_tag="endurance", calories=720, protein=42, carbs=90, fats=20, fiber=4,
         description="Slow-cooked chicken biryani with aromatic whole spices on brown rice."),
    dict(name="Prawn Stir-Fry with Noodles", meal_type="lunch", dietary_type="nonveg",
         goal_tag="maintenance", calories=540, protein=34, carbs=60, fats=14, fiber=4,
         description="Stir-fried prawns with bok choy, noodles and ginger-soy sauce."),

    # ── DINNER – VEG ──────────────────────────────────────────────
    dict(name="Dal Makhani with 2 Rotis", meal_type="dinner", dietary_type="veg",
         goal_tag="maintenance", calories=520, protein=20, carbs=72, fats=16, fiber=10,
         description="Creamy black-lentil curry slow-cooked with butter & fenugreek. 2 chapatis."),
    dict(name="Soya Chunks Curry with Rice", meal_type="dinner", dietary_type="veg",
         goal_tag="muscle_gain", calories=580, protein=38, carbs=72, fats=12, fiber=8,
         description="High-protein soy chunks in a spiced tomato-onion gravy with basmati rice."),
    dict(name="Tofu & Vegetable Thai Curry", meal_type="dinner", dietary_type="veg",
         goal_tag="fat_loss", calories=440, protein=22, carbs=40, fats=20, fiber=7,
         description="Silken tofu in a light coconut-green curry with bell peppers & jasmine rice."),
    dict(name="Palak Paneer with Roti", meal_type="dinner", dietary_type="veg",
         goal_tag="general_fitness", calories=500, protein=26, carbs=44, fats=24, fiber=6,
         description="Cottage cheese in a smooth spinach sauce with 2 whole-wheat chapatis."),
    dict(name="Mushroom & Pea Pulao", meal_type="dinner", dietary_type="veg",
         goal_tag="weight_loss", calories=380, protein=12, carbs=60, fats=9, fiber=5,
         description="Fragrant rice pilaf with mushrooms, green peas, whole spices & herbs."),
    dict(name="Mixed Vegetable Khichdi", meal_type="dinner", dietary_type="veg",
         goal_tag="endurance", calories=420, protein=16, carbs=66, fats=10, fiber=7,
         description="Comforting one-pot rice-lentil dish with carrots, beans & a ghee tadka."),
    dict(name="Vegetable Dal Khichdi", meal_type="dinner", dietary_type="veg",
         goal_tag="weight_loss", calories=390, protein=14, carbs=62, fats=8, fiber=8,
         description="Light moong dal and rice khichdi with seasonal vegetables and a cumin tadka."),
    dict(name="Tofu Tikka Masala with Roti", meal_type="dinner", dietary_type="veg",
         goal_tag="weight_loss", calories=430, protein=22, carbs=46, fats=15, fiber=5,
         description="Tofu chunks in a light tomato-based tikka masala served with 2 whole-wheat rotis."),
    dict(name="Spinach & Lentil Soup", meal_type="dinner", dietary_type="veg",
         goal_tag="weight_loss", calories=310, protein=16, carbs=42, fats=7, fiber=9,
         description="Hearty red lentil and spinach soup with garlic, cumin and lemon."),
    dict(name="Baked Stuffed Capsicum", meal_type="dinner", dietary_type="veg",
         goal_tag="fat_loss", calories=340, protein=14, carbs=40, fats=12, fiber=7,
         description="Bell peppers stuffed with spiced quinoa and vegetables, oven baked."),
    dict(name="Mushroom Oat Risotto", meal_type="dinner", dietary_type="veg",
         goal_tag="maintenance", calories=420, protein=14, carbs=58, fats=12, fiber=6,
         description="Creamy steel-cut oat risotto with mushrooms, parmesan and fresh thyme."),

    # ── DINNER – EGG ──────────────────────────────────────────────
    dict(name="Egg & Spinach Quesadilla", meal_type="dinner", dietary_type="egg",
         goal_tag="weight_loss", calories=420, protein=26, carbs=38, fats=18, fiber=5,
         description="Whole-wheat tortilla with 2 eggs scrambled, spinach, and feta cheese."),
    dict(name="Frittata with Mixed Vegetables", meal_type="dinner", dietary_type="egg",
         goal_tag="fat_loss", calories=360, protein=24, carbs=18, fats=20, fiber=4,
         description="Oven-baked Italian egg cake with courgette, capsicum & cherry tomatoes."),
    dict(name="Egg Noodles Stir-Fry", meal_type="dinner", dietary_type="egg",
         goal_tag="muscle_gain", calories=580, protein=28, carbs=74, fats=16, fiber=4,
         description="Wok noodles with 3 eggs, mixed veg & oyster sauce."),

    # ── DINNER – NON-VEG ──────────────────────────────────────────
    dict(name="Baked Cod with Asparagus", meal_type="dinner", dietary_type="nonveg",
         goal_tag="fat_loss", calories=340, protein=36, carbs=14, fats=12, fiber=4,
         description="150g cod fillet baked with lemon, herbs & olive oil. Asparagus on the side."),
    dict(name="Grilled Chicken Thighs with Green Beans", meal_type="dinner", dietary_type="nonveg",
         goal_tag="weight_loss", calories=420, protein=38, carbs=16, fats=20, fiber=5,
         description="Skinless chicken thighs marinated in herbs, grilled with steamed green beans."),
    dict(name="Beef Stir-Fry with Broccoli", meal_type="dinner", dietary_type="nonveg",
         goal_tag="muscle_gain", calories=620, protein=48, carbs=36, fats=28, fiber=6,
         description="Lean beef strips wok-fried with broccoli, oyster sauce & sesame on rice."),
    dict(name="Prawn & Vegetable Skewers", meal_type="dinner", dietary_type="nonveg",
         goal_tag="maintenance", calories=380, protein=34, carbs=18, fats=16, fiber=4,
         description="Grilled prawn & bell pepper skewers with a garlic-lemon marinade."),
    dict(name="Tandoori Chicken with Salad", meal_type="dinner", dietary_type="nonveg",
         goal_tag="any", calories=460, protein=44, carbs=14, fats=22, fiber=4,
         description="Marinated tandoori chicken drumsticks with a fresh onion-cucumber salad."),
    dict(name="Salmon with Mashed Cauliflower", meal_type="dinner", dietary_type="nonveg",
         goal_tag="fat_loss", calories=480, protein=40, carbs=20, fats=26, fiber=6,
         description="Pan-seared salmon on smooth cauliflower mash with a dill butter sauce."),

    # ── SNACKS – VEG ──────────────────────────────────────────────
    dict(name="Roasted Chickpeas", meal_type="snack", dietary_type="veg",
         goal_tag="any", calories=160, protein=8, carbs=24, fats=4, fiber=6,
         description="Crunchy oven-roasted chickpeas seasoned with paprika & cumin."),
    dict(name="Greek Yogurt with Honey", meal_type="snack", dietary_type="veg",
         goal_tag="muscle_gain", calories=200, protein=14, carbs=22, fats=4, fiber=0,
         description="200g full-fat Greek yogurt drizzled with raw honey."),
    dict(name="Apple with Almond Butter", meal_type="snack", dietary_type="veg",
         goal_tag="fat_loss", calories=190, protein=4, carbs=28, fats=10, fiber=5,
         description="1 medium apple sliced with 1 tbsp natural almond butter."),
    dict(name="Mixed Nuts & Dried Fruit", meal_type="snack", dietary_type="veg",
         goal_tag="endurance", calories=220, protein=6, carbs=18, fats=14, fiber=3,
         description="30g mix of walnuts, almonds, cashews & raisins."),
    dict(name="Paneer Cubes with Pepper", meal_type="snack", dietary_type="veg",
         goal_tag="muscle_gain", calories=180, protein=14, carbs=4, fats=12, fiber=0,
         description="Chilled raw paneer cubes dusted with black pepper & chaat masala."),
    dict(name="Makhana (Fox Nuts) Roasted", meal_type="snack", dietary_type="veg",
         goal_tag="weight_loss", calories=120, protein=4, carbs=20, fats=2, fiber=0,
         description="Lightly roasted fox nuts with a pinch of turmeric and black salt."),
    dict(name="Banana & Peanut Butter", meal_type="snack", dietary_type="veg",
         goal_tag="endurance", calories=250, protein=7, carbs=38, fats=9, fiber=4,
         description="1 medium banana with 1.5 tbsp natural peanut butter."),
    dict(name="Hummus & Carrot Sticks", meal_type="snack", dietary_type="veg",
         goal_tag="any", calories=160, protein=6, carbs=18, fats=8, fiber=5,
         description="3 tbsp hummus with 8 carrot sticks — great mid-afternoon snack."),

    # ── SNACKS – EGG ──────────────────────────────────────────────
    dict(name="Hard Boiled Eggs (2)", meal_type="snack", dietary_type="egg",
         goal_tag="muscle_gain", calories=160, protein=14, carbs=1, fats=10, fiber=0,
         description="2 hard-boiled eggs with a pinch of salt, pepper & paprika."),
    dict(name="Egg Salad Lettuce Cups", meal_type="snack", dietary_type="egg",
         goal_tag="fat_loss", calories=180, protein=14, carbs=4, fats=11, fiber=2,
         description="Chopped boiled eggs with light mayo & mustard in iceberg lettuce cups."),

    # ── SNACKS – NON-VEG ──────────────────────────────────────────
    dict(name="Grilled Chicken Strips", meal_type="snack", dietary_type="nonveg",
         goal_tag="muscle_gain", calories=200, protein=24, carbs=2, fats=8, fiber=0,
         description="80g herbed grilled chicken breast strips — high protein, low carb."),
    dict(name="Tuna on Rice Cakes", meal_type="snack", dietary_type="nonveg",
         goal_tag="fat_loss", calories=170, protein=18, carbs=14, fats=4, fiber=1,
         description="2 lightly salted rice cakes topped with canned tuna in spring water."),
    dict(name="Whey Protein Shake", meal_type="snack", dietary_type="nonveg",
         goal_tag="any", calories=160, protein=25, carbs=8, fats=3, fiber=0,
         description="1 scoop whey protein blended with water and ice. Quick post-workout option."),
    dict(name="Salmon & Cucumber Bites", meal_type="snack", dietary_type="nonveg",
         goal_tag="fat_loss", calories=140, protein=16, carbs=4, fats=7, fiber=1,
         description="Smoked salmon pieces on cucumber rounds with a touch of cream cheese."),
]


def run():
    created = 0
    for data in MEALS:
        obj, is_new = Meal.objects.get_or_create(
            name=data['name'],
            meal_type=data['meal_type'],
            defaults=data
        )
        if is_new:
            created += 1

    print(f"✅ Seeded {created} new meals. Total in DB: {Meal.objects.count()}")


run()
