import os
import re

CSS_DIR = r"c:\Users\Dev\Desktop\PROJECT\env\fitness"
FILES_TO_FIX = [
    os.path.join(CSS_DIR, r"account\static\account\css\dashboard.css"),
    os.path.join(CSS_DIR, r"account\static\account\css\success.css"),
    os.path.join(CSS_DIR, r"core\static\core\css\blog.css"),
    os.path.join(CSS_DIR, r"core\static\core\css\community.css"),
    os.path.join(CSS_DIR, r"core\static\core\css\contact.css"),
    os.path.join(CSS_DIR, r"core\static\core\css\index.css"),
    os.path.join(CSS_DIR, r"core\static\core\css\membership.css"),
    os.path.join(CSS_DIR, r"core\static\core\css\story.css"),
    os.path.join(CSS_DIR, r"diet\static\diet\css\diet-gain.css"),
    os.path.join(CSS_DIR, r"diet\static\diet\css\diet-lose.css"),
    os.path.join(CSS_DIR, r"diet\static\diet\css\diet.css"),
    os.path.join(CSS_DIR, r"store\static\store\css\store.css"),
    os.path.join(CSS_DIR, r"store\static\store\css\store-men.css"),
    os.path.join(CSS_DIR, r"store\static\store\css\store-women.css"),
    os.path.join(CSS_DIR, r"workout\static\workout\css\coaches.css"),
    os.path.join(CSS_DIR, r"workout\static\workout\css\fitness.css"),
    os.path.join(CSS_DIR, r"workout\static\workout\css\sport.css"),
    os.path.join(CSS_DIR, r"workout\static\workout\css\trainers.css"),
    os.path.join(CSS_DIR, r"workout\static\workout\css\workouts.css"),
]

# Comprehensive list of grid classes used across the project
GRID_CLASSES = ".prod-grid, .workout-grid, .exercise-grid, .trainer-grid, .program-grid, .success-grid, .coaches-grid, .diet-grid, .product-grid, .story-grid, .stats-grid, .diet-plan-grid, .challenge-grid, .profile-details-grid, .action-buttons"

# --- RESPONSIVE CSS SNIPPET ---
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
    {GRID_CLASSES}, .charts-wrap {{
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
    {GRID_CLASSES}, .charts-wrap, .diet-plan-grid, .challenge-grid, .profile-details-grid, .action-buttons {{
        display: grid !important;
        grid-template-columns: 1fr !important;
        gap: 15px !important;
    }}
    .navbar {{
        padding: 0 15px !important;
    }}
    .nav-links {{
        display: none !important; /* Hide by default on mobile, handled by hamburger */
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

def clean_css_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Filter out junk lines (spaced out letters)
        new_lines = []
        for line in lines:
            # Check for widely spaced characters like ". d a s h b o a r d"
            if re.search(r'\w\s+\w\s+\w\s+\w\s+\w', line):
                continue
            new_lines.append(line)
        
        content = "".join(new_lines)
        
        # Remove existing responsive blocks to avoid duplicates
        content = re.sub(r'/\* FITX RESPONSIVE UTILITIES.*?\*/.*?\n(@media.*?\{.*?\}\s*?)+', '', content, flags=re.DOTALL)
        
        # Append the new block
        content = content.strip() + "\n\n" + RESPONSIVE_BLOCK
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed responsiveness and cleaned {path}")

def apply_to_all():
    for file_path in FILES_TO_FIX:
        clean_css_file(file_path)

if __name__ == "__main__":
    apply_to_all()
