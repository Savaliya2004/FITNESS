import os
import re
from pathlib import Path

# Use the current directory as the base directory
BASE_DIR = Path(__file__).parent.resolve()

# Regex to find all CSS files in the project
def get_all_css_files():
    css_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # Exclude env, node_modules, etc if any exist
        if 'env' in dirs:
            dirs.remove('env')
        for file in files:
            if file.endswith('.css'):
                css_files.append(os.path.join(root, file))
    return css_files

# Comprehensive list of grid and flex classes used across the project based on previous analysis
GRID_CLASSES = ".prod-grid, .workout-grid, .exercise-grid, .trainer-grid, .program-grid, .success-grid, .coaches-grid, .diet-grid, .product-grid, .story-grid, .stats-grid, .diet-plan-grid, .challenge-grid, .profile-details-grid, .action-buttons, .categories-grid, .programs-grid, .trainers-track, .plans-grid, .dash-grid, .dash-cards, .app-grid, .footer-grid, .f-top"

FLEX_CLASSES_TO_WRAP = ".flex-row, .d-flex, .nav-actions, .hero-ctas, .testi-track, .form-row"

# --- SUPER RESPONSIVE CSS SNIPPET ---
RESPONSIVE_BLOCK = f"""
/* ==========================================================================
   FITX GLOBAL RESPONSIVE OVERRIDES (ADDED AUTOMATICALLY)
   ========================================================================== */

/* --- GLOBAL RESETS --- */
html, body {{
    max-width: 100vw !important;
    overflow-x: hidden !important;
}}

/* Images and Media Scaling */
img, video, canvas, iframe, object, embed {{
    max-width: 100% !important;
    height: auto !important;
}}

/* Tables Responsiveness */
table {{
    width: 100% !important;
    border-collapse: collapse;
}}
table, thead, tbody, th, td, tr {{
    /* Ensure tables don't cause overflow */
    max-width: 100%;
}}
.table-container, .table-responsive {{
    width: 100%;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch;
}}

/* Forms, Inputs and Buttons */
input[type="text"], input[type="email"], input[type="password"], input[type="number"], 
input[type="search"], input[type="tel"], input[type="url"], textarea, select {{
    max-width: 100% !important;
    box-sizing: border-box !important;
}}

/* --- MEDIA QUERIES --- */

/* LAPTOP / SMALL DESKTOP (1025px - 1440px) */
@media (max-width: 1440px) and (min-width: 1025px) {{
    {GRID_CLASSES} {{
        gap: 20px !important;
    }}
}}

/* TABLET (768px - 1024px) */
@media (max-width: 1024px) and (min-width: 768px) {{
    {GRID_CLASSES}, .charts-wrap {{
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 20px !important;
    }}
    .footer-grid, .f-top {{
        grid-template-columns: repeat(2, 1fr) !important;
    }}
    .page-hero, .hero-section {{
        padding: 60px 5% !important;
    }}
    {FLEX_CLASSES_TO_WRAP} {{
        flex-wrap: wrap !important;
    }}
}}

/* MOBILE (320px - 767px) */
@media (max-width: 767px) {{
    /* Stack Grids into Single Column */
    {GRID_CLASSES}, .charts-wrap, .diet-plan-grid, .challenge-grid, .profile-details-grid, .action-buttons {{
        display: grid !important;
        grid-template-columns: 1fr !important;
        gap: 16px !important;
    }}
    
    /* Footer & Headers */
    .footer-grid, .f-top {{
        grid-template-columns: 1fr !important;
        gap: 30px !important;
        text-align: left;
    }}
    
    /* Flex Containers Wrap & Stack */
    {FLEX_CLASSES_TO_WRAP} {{
        flex-direction: column !important;
        align-items: flex-start !important;
        width: 100% !important;
        gap: 12px !important;
    }}
    
    /* Navbar specifics for mobile handled via js/hamburger normally, but fallback: */
    .navbar {{
        padding: 0 15px !important;
    }}
    
    /* Full Width Elements */
    .btn, button, .btn-primary, .btn-ghost, .btn-outline, .btn-plan, .btn-store {{
        width: 100% !important;
        margin-bottom: 10px !important;
        justify-content: center !important;
        text-align: center !important;
    }}
    
    /* Forms Stack */
    .form-group, .form-row {{
        flex-direction: column !important;
        width: 100% !important;
    }}
    
    /* Typography Scaling */
    h1, .hero-title {{
        font-size: 2.2rem !important;
        line-height: 1.2 !important;
    }}
    h2, .section-title {{
        font-size: 1.8rem !important;
    }}
    
    /* Ensure Cards don't exceed screen */
    .card, .cat-card, .prog-card, .plan-card, .metric-card, .testi-card {{
        width: 100% !important;
        box-sizing: border-box !important;
    }}
    
    /* Sidebars */
    .sidebar, .dashboard-sidebar {{
        width: 100% !important;
        height: auto !important;
        position: relative !important;
        padding-bottom: 20px !important;
    }}
    
    /* Tables for mobile */
    table, thead, tbody, th, td, tr {{
        display: block;
    }}
    thead tr {{
        display: none; /* Hide headers visually but could keep them for screen readers */
    }}
    tr {{ border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; }}
    td {{
        border-bottom: none;
        position: relative;
        padding-left: 50% !important;
        text-align: right !important;
    }}
    td::before {{
        content: attr(data-label);
        position: absolute;
        left: 15px;
        width: 45%;
        padding-right: 10px;
        white-space: nowrap;
        text-align: left;
        font-weight: bold;
        color: var(--muted, #888);
    }}
}}
"""

def clean_css_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Filter out junk lines (spaced out letters)
        new_lines = []
        for line in lines:
            if re.search(r'\w\s+\w\s+\w\s+\w\s+\w', line):
                continue
            new_lines.append(line)
        
        content = "".join(new_lines)
        
        # Remove existing responsive blocks to avoid duplicates
        # Look for the old or new header signature
        content = re.sub(r'/\* (FITX RESPONSIVE UTILITIES|==========================================================================\s*FITX GLOBAL RESPONSIVE).*?\*/.*?\n(@media.*?\{.*?\n\}\s*?)+', '', content, flags=re.DOTALL)
        content = re.sub(r'/\* =+ \n\s*FITX GLOBAL RESPONSIVE OVERRIDES.*?(?=\Z|/\* =+)', '', content, flags=re.DOTALL)

        # Basic cleanup: if there is a lingering FITX GLOBAL RESPONSIVE OVERRIDES, we forcefully trim from that point onwards if it's at the end
        if "/* ==========================================================================" in content:
            content = content.split("/* ==========================================================================")[0]
        
        # Append the new block
        content = content.strip() + "\n\n" + RESPONSIVE_BLOCK
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed responsiveness and cleaned {path}")

def apply_to_all():
    css_files = get_all_css_files()
    print(f"Found {len(css_files)} CSS files.")
    for file_path in css_files:
        clean_css_file(file_path)
    print("Done applying responsive fixes to all CSS files.")

if __name__ == "__main__":
    apply_to_all()
