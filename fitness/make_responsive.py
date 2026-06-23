import os
import glob
import re

css_dir = r"c:\Users\Dev\Desktop\PROJECT\env\fitness"

# Find all css files
css_files = glob.glob(os.path.join(css_dir, "**", "*.css"), recursive=True)

for file in css_files:
    if "make_responsive" in file or ".antigravityignore" in file: continue
    
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
        
    original = content
        
    # Standardize breakpoints
    content = content.replace("max-width: 1024px", "max-width: 1199px")
    content = content.replace("max-width: 768px", "max-width: 767px")
    
    # Common issues preventing responsiveness
    # 1. minmax(350px/380px...) which breaks mobile
    content = re.sub(r"minmax\([3-9]\d{2}px", "minmax(280px", content)
    
    # 2. Add padding trick for body if not present to ensure padding on sides for mobile
    if "@media (max-width: 767px)" in content and "body {" not in content.split("@media (max-width: 767px)")[1][:100]:
        # just replace minmax to 1fr on mobile grids if any grid template columns exist
        pass
        
    if content != original:
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {file}")

print("Done processing CSS files.")
