import os
import re

def fix_file(path, replacements, regex_replacements=None):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    if regex_replacements:
        for pattern, repl in regex_replacements:
            content = re.sub(pattern, repl, content, flags=re.MULTILINE)
            
    # Generic cleanup for stray closing braces before responsive block or after faulty edits
    content = re.sub(r'}\s+}\s+/\* FITX RESPONSIVE UTILITIES', '}\n\n/* FITX RESPONSIVE UTILITIES', content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {path}")

# 1. index.css (Global Underline & Nav Links)
fix_file(r'c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\index.css', [
    ('html { scroll-behavior: smooth; }', 'html { scroll-behavior: smooth; }\na { text-decoration: none !important; }'),
    ('.nav-links {\n  color: var(--muted);', '.nav-links a {\n  color: var(--muted);'),
])

# 2. trainers.css (Alignment & Base Card)
fix_file(r'c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\trainers.css', [
    ('.trainer-card:hover {', '.trainer-card {\n    background: var(--card-bg);\n    border: 1px solid var(--border);\n    border-radius: var(--radius);\n    overflow: hidden;\n    display: flex;\n    flex-direction: column;\n    transition: all 0.3s ease;\n    height: 100%;\n}\n.trainer-card:hover {'),
    ('.trainer-info { padding: 22px; display: flex; flex-direction: column; gap: 14px; flex-grow: 1; }', 
     '.trainer-info { padding: 22px; display: flex; flex-direction: column; gap: 14px; flex-grow: 1; }'),
    ('    margin-top: auto;\n    display: block', '    margin-top: auto !important;\n    display: block'),
])

# 3. workouts.css (Enroll Alignment & Broken Braces)
fix_file(r'c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\workouts.css', [
    ('.nav-links {\n    color: var(--text-muted);', '.nav-links a {\n    color: var(--text-muted);'),
    ('.social-links {\n    display: flex; gap: 12px; }\n    width:', '.social-links {\n    display: flex; gap: 12px; }\n.social-links a {\n    width:'),
    ('.program-card {', '.program-card {\n    display: flex;\n    flex-direction: column;'),
    ('.program-body { padding: 20px 22px; display: flex; flex-direction: column; gap: 12px; flex: 1; }', 
     '.program-body { padding: 20px 22px; display: flex; flex-direction: column; gap: 12px; flex: 1; }'), # Just ensuring it's there
    ('.program-footer {', '.program-footer {\n    margin-top: auto; padding-top: 20px;'),
])

# 4. fitness.css (Enroll alignment)
fix_file(r'c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\fitness.css', [
    ('.ex-box {', '.ex-box {\n    display: flex;\n    flex-direction: column;'),
    ('.ex-content { padding: 0 10px 10px; }', '.ex-content { padding: 0 10px 10px; flex-grow: 1; display: flex; flex-direction: column; }'),
    ('.ex-footer { display: flex; justify-content: space-between; align-items: center; }', 
     '.ex-footer { display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 15px; }'),
])

# 5. diet.css (Labels and Spacing)
fix_file(r'c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\static\diet\css\diet.css', [
    ('.section-header p {', '.section-header p {\n    color: var(--muted);\n    font-size: 1.1rem;'), # Fix possibly broken selector
    ('.form-group {', '.form-group {\n    margin-bottom: 15px;'),
])

# 6. community.css (Layout Grid)
fix_file(r'c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\community.css', [
    ('.feed {', '.comm-container {\n    display: grid;\n    grid-template-columns: 2fr 1fr;\n    gap: 40px;\n    max-width: 1300px;\n    margin: 60px auto;\n    padding: 0 5%;\n}\n.feed {'),
    ('.post-avatar {', '.post-avatar {\n    width: 60px;\n    height: 60px;\n    border-radius: 50%;\n    object-fit: cover;\n    border: 2px solid var(--accent);'),
])
