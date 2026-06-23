import os
import re

def fix_index_css():
    path = r'c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\index.css'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define robust light theme variables in index.css
    light_theme_block = """[data-theme="light"] {
  --bg:         #ffffff;
  --bg2:        #f8fafc;
  --card:       #f1f5f9;
  --card2:      #e2e8f0;
  --accent:     #6a5cff;
  --accent2:    #3b82f6;
  --accentDim:  rgba(106, 92, 255, 0.1);
  --glass:      rgba(255, 255, 255, 0.8);
  --glassBorder:rgba(0, 0, 0, 0.08);
  --text:       #0f172a;
  --muted:      #64748b;
  --radius:     16px;
}"""
    
    # Replace broken light theme block
    content = re.sub(r'\[data-theme="light"\] \{.*?\}', light_theme_block, content, flags=re.DOTALL)

    # Fix broken nav-links a selector
    content = content.replace('.nav-links { display: flex; gap: 20px; list-style: none; }\n  color: var(--muted);', 
                              '.nav-links { display: flex; gap: 20px; list-style: none; }\n.nav-links a {\n  color: var(--muted);')

    # Fix footer broken selectors
    content = content.replace('  color: #888; \n  font-size: 0.95rem; \n  line-height: 1.6; \n  max-width: 320px; \n}', 
                              '.f-brand p {\n  color: #888; \n  font-size: 0.95rem; \n  line-height: 1.6; \n  max-width: 320px; \n}')
    
    content = content.replace('  color: #888; \n  text-decoration: none; \n  font-size: 0.95rem; \n  transition: var(--transition);\n}', 
                              '.f-links a {\n  color: #888; \n  text-decoration: none; \n  font-size: 0.95rem; \n  transition: var(--transition);\n}')
    
    content = content.replace('  font-size: 1.1rem; \n  color: #fff; \n  background: rgba(255,255,255,0.08); \n  width: 44px; \n  height: 44px; \n  border-radius: 50%; \n  display: inline-flex; \n  align-items: center; \n  justify-content: center; \n  transition: var(--transition); \n  cursor: pointer; \n}',
                              '.f-social i {\n  font-size: 1.1rem; \n  color: #fff; \n  background: rgba(255,255,255,0.08); \n  width: 44px; \n  height: 44px; \n  border-radius: 50%; \n  display: inline-flex; \n  align-items: center; \n  justify-content: center; \n  transition: var(--transition); \n  cursor: pointer; \n}')

    content = content.replace('  color: #444; \n  font-size: 0.85rem; \n  border-top: 1px solid rgba(255,255,255,0.05); \n  padding-top: 30px;\n}',
                              '.f-bottom p {\n  color: #444; \n  font-size: 0.85rem; \n  border-top: 1px solid rgba(255,255,255,0.05); \n  padding-top: 30px;\n}')

    # Improved Footer Styling
    improved_footer = """
.mega-footer { 
  border-top: 1px solid var(--glassBorder); 
  background: #050505; 
  padding: 80px 0 40px; 
  font-family: 'Inter', sans-serif; 
  position: relative; 
  z-index: 100;
  transition: background 0.3s ease;
}
[data-theme="light"] .mega-footer { background: #f1f5f9; border-top-color: #e2e8f0; }
[data-theme="light"] .f-brand h2 { color: #0f172a; }
[data-theme="light"] .f-brand p { color: #475569; }
[data-theme="light"] .f-links a { color: #475569; }
[data-theme="light"] .f-links a:hover { color: var(--accent); }
[data-theme="light"] .f-social i { background: #e2e8f0; color: #475569; }
[data-theme="light"] .f-social i:hover { background: var(--accent); color: #fff; }
[data-theme="light"] .f-bottom p { color: #94a3b8; border-top-color: #e2e8f0; }
"""
    # Replace the old mega-footer block
    content = re.sub(r'\.mega-footer \{.*?\}', improved_footer, content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed index.css")

def clean_other_css_files():
    base_dir = r'c:\Users\Dev\Desktop\PROJECT\env\fitness'
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.css') and file != 'index.css':
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove redundant universal light theme blocks
                new_content = re.sub(r'/\* UNIVERSAL LIGHT THEME SUPPORT \*/\s*\[data-theme="light"\] \{.*?\}', '', content, flags=re.DOTALL)
                new_content = re.sub(r'\[data-theme="light"\] body \{.*?\}', '', new_content, flags=re.DOTALL)
                new_content = re.sub(r'\[data-theme="light"\] h1,.*?\{.*?\}', '', new_content, flags=re.DOTALL)
                new_content = re.sub(r'\[data-theme="light"\] p,.*?\{.*?\}', '', new_content, flags=re.DOTALL)
                new_content = re.sub(r'\[data-theme="light"\] .navbar,.*?\{.*?\}', '', new_content, flags=re.DOTALL)
                new_content = re.sub(r'\[data-theme="light"\] .nav-links a,.*?\{.*?\}', '', new_content, flags=re.DOTALL)
                new_content = re.sub(r'\[data-theme="light"\] .btn-ghost \{.*?\}', '', new_content, flags=re.DOTALL)
                new_content = re.sub(r'\[data-theme="light"\] input,.*?\{.*?\}', '', new_content, flags=re.DOTALL)
                new_content = re.sub(r'\[data-theme="light"\] .mega-footer \{.*?\}', '', new_content, flags=re.DOTALL)
                
                # Also remove fixed footer headers if they exist
                new_content = re.sub(r'/\* ===========================\s*MEGA FOOTER.*?=========================== \*/', '', new_content, flags=re.DOTALL)

                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Cleaned {file}")

if __name__ == "__main__":
    fix_index_css()
    clean_other_css_files()
