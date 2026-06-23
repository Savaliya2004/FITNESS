import os
import re

def convert_to_template(path, title, extra_css_files, content_match_start, content_match_end):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    # Try to extract the content between specific tags/marks
    content_re = re.compile(f'{re.escape(content_match_start)}(.*?){re.escape(content_match_end)}', re.DOTALL)
    match = content_re.search(full_text)
    if not match: 
        print(f"Could not find content in {path}")
        return
    
    inner_content = match.group(1).strip()
    
    # Extract scripts if any
    script_re = re.compile(r'<script>(.*?)</script>', re.DOTALL)
    scripts = script_re.findall(full_text)
    
    extra_css = ""
    for css in extra_css_files:
        extra_css += f'<link rel="stylesheet" href="{{% static \'{css}\' %}}">\n'
    
    new_template = f"""{{% extends 'core/base.html' %}}
{{% load static %}}

{{% block title %}}{title}{{% endblock %}}

{{% block extra_css %}}
{extra_css}
{{% endblock %}}

{{% block content %}}
{inner_content}
{{% endblock %}}

{{% block extra_js %}}
<script>
{''.join(scripts)}
</script>
{{% endblock %}}
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_template)
    print(f"Converted {path}")

# Convert store-cat.html
convert_to_template(
    r'c:\Users\Dev\Desktop\PROJECT\env\fitness\store\templates\store\store-cat.html',
    'FitX Store | Category',
    ['store/static/store/css/store.css'], # Path might need adjustment for template tag
    '<body>',
    '<!-- MEGA FOOTER -->'
)

# Convert diet-lose.html
convert_to_template(
    r'c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\templates\diet\diet-lose.html',
    'FitX | Weight Loss Protocol',
    ['diet/static/diet/css/diet.css'],
    '<body>',
    '<footer class="mega-footer">'
)

# Convert diet-gain.html
convert_to_template(
    r'c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\templates\diet\diet-gain.html',
    'FitX | Muscle Gain Protocol',
    ['diet/static/diet/css/diet.css'],
    '<body>',
    '<footer class="mega-footer">'
)
