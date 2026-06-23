import os

login_css_path = r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\static\account\css\login.css"
signup_css_path = r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\static\account\css\signup.css"

for path in [login_css_path, signup_css_path]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "body::after { display: none; }" not in content:
        content += '\n[data-theme="light"] body::after { display: none; }\n'
        content += '[data-theme="light"] .auth-header h2, [data-theme="light"] .brand h1 { color: #111; }\n'
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {path}")
