import os

def replace_in_file(path, old, new):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {path}")

# 1. Global Underline Removal in base.html
replace_in_file(r'c:\Users\Dev\Desktop\PROJECT\env\fitness\core\templates\core\base.html', 
    '{% block extra_css %}{% endblock %}', 
    '{% block extra_css %}{% endblock %}\n  <style>a, a:hover, a:focus, a:active { text-decoration: none !important; }</style>'
)

# 2. Fix Community Images
replace_in_file(r'c:\Users\Dev\Desktop\PROJECT\env\fitness\core\templates\core\community.html', 
    'https://images.unsplash.com/photo-1599058945522-28d584b6f4ff?w=600&q=80', 
    'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&q=80'
)

# 3. Ensure Enroll Now buttons are aligned in workouts.html
# We already fixed the CSS, let's just make sure the HTML is clean
replace_in_file(r'c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\templates\workout\workouts.html',
    '<div class="program-footer">',
    '<div class="program-footer" style="margin-top: auto;">'
)
