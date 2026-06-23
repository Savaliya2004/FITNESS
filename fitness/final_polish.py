import os

CSS_ROOT = r"c:\Users\Dev\Desktop\PROJECT\env\fitness"
css_files = []
for root, dirs, files in os.walk(CSS_ROOT):
    for file in files:
        if file.endswith(".css"):
            css_files.append(os.path.join(root, file))

# Fix Coach Alignment in EVERY coaches/trainers related CSS
COACH_FIX = """
/* FORCE ALIGN BOOK SESSION BUTTONS */
.trainer-card, .coach-card {
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
}
.trainer-info, .coach-info {
    display: flex !important;
    flex-direction: column !important;
    flex-grow: 1 !important;
}
.btn-book, .book-btn, .action-btn {
    margin-top: auto !important;
}
"""

for f in css_files:
    if "final_theme_fix.py" in f or "apply_responsiveness.py" in f: continue
    
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Remove spaced junk if any (sometimes my edits fail and leave residue)
    content = content.replace(". c h a r t", ".chart")
    
    # Apply Coach Fix to relevant files
    if "trainer" in f or "coach" in f:
        if "FORCE ALIGN BOOK SESSION" not in content:
            content += COACH_FIX
            
    with open(f, "w", encoding="utf-8") as file:
        file.write(content)

print("Done polishing coach alignment and cleaning residue.")
