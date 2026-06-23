import os

REPAIRS = {
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\static\account\css\dashboard.css": [
        (".sidebar-brand {", "    height: var(--header-height);", ".sidebar-brand i {"),
        (".nav-item {", "    display: flex;", ".nav-item i {"),
        ('[data-theme="light"] .home-btn, [data-theme="light"] .notif-btn { background: #fff; border-color: #eee; color: #1a1a2e; }', "    background: #fff; border-color: #eee; box-shadow: 0 4px 15px rgba(0,0,0,0.05);", '[data-theme="light"] .stat-card, [data-theme="light"] .chart-card, [data-theme="light"] .action-btn.outline, [data-theme="light"] .workout-card, [data-theme="light"] .meal-card, [data-theme="light"] .challenge-card, [data-theme="light"] .profile-header-card, [data-theme="light"] .detail-card, [data-theme="light"] .settings-section {'),
    ],
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store.css": [
        (".nav-brand .logo-text span { color: var(--accent); }", "  color: var(--muted); text-decoration: none; font-size: .75rem;", ".nav-links a {"),
        (".store-nav {", "    backdrop-filter: blur(20px); border-bottom: 1px solid var(--glassBorder);", ".nav-links-inner a {"),
    ],
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\static\diet\css\diet.css": [
        ('[data-theme="light"] p, [data-theme="light"] span, [data-theme="light"] li { color: #333; }', "    background: #fff; border-color: #ddd; box-shadow: 0 4px 12px rgba(0,0,0,0.05); color: #111;", '[data-theme="light"] .meal-card, [data-theme="light"] .planner-card, [data-theme="light"] .calories-box, [data-theme="light"] .quote-card, [data-theme="light"] .water-card {'),
        ('[data-theme="light"] .quote-card p { color: #111; }', "    background: #fff !important; color: #111 !important; border: 1px solid #ccc !important;", '[data-theme="light"] input, [data-theme="light"] select {'),
        (".navbar {", "        padding: 0 15px !important;", "    }"), # Closing brace was missing too? No.
    ]
}

def repair_file(path, rules):
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    for anchor, target_props, missing_selector in rules:
        if anchor in content and missing_selector not in content:
            # We want to insert missing_selector before the properties
            # This is tricky because properties might be indented
            pattern = re.escape(target_props)
            content = content.replace(target_props, missing_selector + "\n" + target_props)
            print(f"Repaired {path}: Added {missing_selector}")

    # Fix the Utility Block in EVERY file
    GRID_CLASSES = ".prod-grid, .workout-grid, .exercise-grid, .trainer-grid, .program-grid, .success-grid, .coaches-grid, .diet-grid, .product-grid, .story-grid, .stats-grid, .diet-plan-grid, .challenge-grid, .profile-details-grid, .action-buttons, .charts-wrap"
    
    RESPONSIVE_BLOCK = f"""
/* FITX RESPONSIVE UTILITIES - 4-2-1 COLUMN SYSTEM */
@media (min-width: 1200px) {{
    {GRID_CLASSES} {{
        display: grid !important;
        grid-template-columns: repeat(4, 1fr) !important;
        gap: 25px !important;
    }}
    .diet-plan-grid, .challenge-grid, .charts-wrap {{
        grid-template-columns: repeat(2, 1fr) !important;
    }}
}}

@media (max-width: 1199px) and (min-width: 768px) {{
    {GRID_CLASSES} {{
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 20px !important;
    }}
    .page-hero, .hero-section {{
        flex-direction: column !important;
        text-align: center !important;
        padding: 60px 5% !important;
    }}
    .hero-content {{ margin-bottom: 30px !important; }}
}}

@media (max-width: 767px) {{
    {GRID_CLASSES} {{
        display: grid !important;
        grid-template-columns: 1fr !important;
        gap: 15px !important;
    }}
    .navbar {{
        padding: 0 15px !important;
    }}
    .nav-links {{
        display: none !important;
    }}
    .hamburger, .menu-toggle {{
        display: block !important;
    }}
    img {{
        max-width: 100% !important;
        height: auto !important;
    }}
    h1 {{ font-size: 1.8rem !important; }}
    h2 {{ font-size: 1.5rem !important; }}
    .btn, button {{ width: 100% !important; margin-bottom: 10px !important; }}
    .sidebar {{ width: 100% !important; z-index: 2000 !important; }}
}}
"""
    # Remove any existing responsive blocks first to avoid mess
    content = re.sub(r'/\* FITX RESPONSIVE UTILITIES.*', '', content, flags=re.DOTALL)
    content = content.strip() + "\n" + RESPONSIVE_BLOCK

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

import re
FILES_TO_CLEAN = [
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\static\account\css\dashboard.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\static\account\css\success.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\blog.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\community.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\contact.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\index.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\membership.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\story.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\static\diet\css\diet-gain.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\static\diet\css\diet-lose.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\static\diet\css\diet.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store-men.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store-women.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\coaches.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\fitness.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\sport.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\trainers.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\workouts.css",
]

for p in FILES_TO_CLEAN:
    repair_file(p, REPAIRS.get(p, []))
