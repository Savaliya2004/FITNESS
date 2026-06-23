import os
import re

def final_sanitize_css():
    base_dir = r'c:\Users\Dev\Desktop\PROJECT\env\fitness'
    
    # 1. Patterns for missing selectors
    missing_selectors = {
        r'\.social-links \{\s*display:\s*flex;.*?\}\s+width:\s*38px;': r'.social-links { display: flex; gap: 12px; }\n.social-links a {\n    width: 38px;',
        r'\.f-bottom \{\s*text-align:\s*center;.*?\}\s+color:\s*#444;': r'.f-bottom { text-align: center; }\n.f-bottom p {\n  color: #444;',
        r'padding:\s*14px\s*20px;\s*font-size:\s*0\.72rem;': r'.dropdown a {\n  padding: 14px 20px; font-size: 0.72rem;',
        r'color:\s*var\(--muted\);\s*text-decoration:\s*none;\s*font-size:\s*\.85rem;\s*transition:\s*color\s*var\(--transition\);': r'.footer-links a {\n  color: var(--muted); text-decoration: none; font-size: .85rem;\n  transition: color var(--transition);',
    }

    # 2. Pattern for redundant media queries (anything between @media ... { and its closing brace that contains grid-template-columns: repeat)
    redundant_mq_pattern = re.compile(r'@media\s*\(max-width:\s*(?:1200|1199|768|767|480)px\)\s*\{.*?grid-template-columns:.*?\}', re.DOTALL)

    # 3. Pattern for hardcoded footers in CSS
    hardcoded_footer_pattern = re.compile(r'/\* FOOTER \*/.*?site-footer.*?\}', re.DOTALL | re.IGNORECASE)
    hardcoded_footer_pattern2 = re.compile(r'\.site-footer.*?\}', re.DOTALL)
    hardcoded_footer_pattern3 = re.compile(r'\.footer-grid.*?\}', re.DOTALL)

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.css'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                
                # Fix specific missing selectors
                for pattern, replacement in missing_selectors.items():
                    new_content = re.sub(pattern, replacement, new_content, flags=re.DOTALL)
                
                # Special fix for workouts.css social-links
                if 'workouts.css' in file:
                    new_content = new_content.replace('.social-links { display: flex; gap: 12px; }\n    width: 38px;', 
                                                       '.social-links { display: flex; gap: 12px; }\n.social-links a {\n    width: 38px;')

                # Remove redundant media queries (keep the ones in index.css as primary)
                if file != 'index.css':
                    # We want to keep some layout MQ but remove the grid ones if they conflict
                    # For now, let's just clear the common broken ones
                    new_content = redundant_mq_pattern.sub('', new_content)
                    new_content = hardcoded_footer_pattern.sub('', new_content)
                    new_content = hardcoded_footer_pattern2.sub('', new_content)
                    new_content = hardcoded_footer_pattern3.sub('', new_content)
                
                # Remove duplicate declarations in same block
                new_content = re.sub(r'(margin-top:\s*auto;\s*padding-top:\s*20px;)\s+\1', r'\1', new_content)

                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Sanitized {file}")

def fix_enroll_buttons():
    base_dir = r'c:\Users\Dev\Desktop\PROJECT\env\fitness'
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Fix hardcoded .html links
                new_content = content.replace('href="login.html"', 'href="{% url \'login\' %}"')
                new_content = new_content.replace('href="signup.html"', 'href="{% url \'signup\' %}"')
                new_content = new_content.replace('href="workouts.html"', 'href="{% url \'workouts\' %}"')
                new_content = new_content.replace('href="diet.html"', 'href="{% url \'diet\' %}"')
                new_content = new_content.replace('href="index.html"', 'href="{% url \'home\' %}"')
                new_content = new_content.replace('href="trainers.html"', 'href="{% url \'trainers\' %}"')
                new_content = new_content.replace('href="coaches.html"', 'href="{% url \'trainers\' %}"')
                new_content = new_content.replace('href="community.html"', 'href="{% url \'community\' %}"')

                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed links in {file}")

if __name__ == "__main__":
    final_sanitize_css()
    fix_enroll_buttons()
