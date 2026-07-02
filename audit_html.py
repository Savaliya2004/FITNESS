import os
import re

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Image optimizations: Add loading="lazy" if not present and not in a hero section (heuristic)
    # We will just add loading="lazy" to all img tags that don't have it.
    
    # regex for img tag
    img_pattern = re.compile(r'(<img\b[^>]*?)(/?>)', re.IGNORECASE)
    
    def process_img(match):
        img_tag = match.group(1)
        closing = match.group(2)
        
        # Don't add lazy loading to hero images (heuristic based on class or id)
        if 'hero' in img_tag.lower():
            # Ensure it has alt at least
            if 'alt=' not in img_tag.lower():
                img_tag += ' alt="Image"'
            return f'{img_tag}{closing}'
            
        if 'loading=' not in img_tag.lower():
            img_tag += ' loading="lazy"'
            
        if 'alt=' not in img_tag.lower():
            img_tag += ' alt="Image"'
            
        return f'{img_tag}{closing}'
        
    content = img_pattern.sub(process_img, content)
    
    # 2. Add aria-labels to buttons that only have icons
    # e.g. <button ...><i class="fa fa-times"></i></button>
    # Note: Regex parsing HTML is fraught, so we do a simple heuristic
    
    # 3. Form fields
    # If there are inputs without form-control but within our context?
    # Usually we rely on manual CSS updates.
    
    # 4. Semantic HTML:
    # We will manually replace generic `<div class="content-area">` with `<main class="content-area">` in dashboard.html.
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_dir = r'c:\Users\Dev\Desktop\FITNESS\fitness'
    modified_count = 0
    for root, dirs, files in os.walk(base_dir):
        # skip venv or other unneeded
        if 'venv' in root or '.git' in root:
            continue
            
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    if process_html_file(filepath):
                        print(f"Modified: {filepath}")
                        modified_count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
                    
    print(f"Total files modified: {modified_count}")

if __name__ == '__main__':
    main()
