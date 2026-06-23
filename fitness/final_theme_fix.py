import os

# --- PART 1: GLOBAL LIGHT THEME FIX ---
css_files = [
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\static\account\css\dashboard.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\static\account\css\success.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\admin.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\blog.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\community.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\contact.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\membership.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\story.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\static\diet\css\diet-gain.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\static\diet\css\diet-lose.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\static\diet\css\diet.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\cart.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\order-success.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store-acc.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store-equip.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store-footwear.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store-men.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store-new.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store-women.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\coaches.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\fitness.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\sport.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\trainers.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\workouts.css",
]

generic_light_block = """
/* UNIVERSAL LIGHT THEME SUPPORT */
[data-theme="light"] {
    --bg: #f5f7fa;
    --bg2: #ffffff;
    --bg-dark: #f0f2f5;
    --card-bg: #ffffff;
    --cardBg: #ffffff;
    --text-main: #111111;
    --text-dim: #555555;
    --muted: #666666;
    --glassBorder: rgba(0, 0, 0, 0.1);
    --glass-border: rgba(0, 0, 0, 0.1);
}
[data-theme="light"] body { background: var(--bg); color: #111; }
[data-theme="light"] h1, [data-theme="light"] h2, [data-theme="light"] h3, [data-theme="light"] h4, [data-theme="light"] h5, [data-theme="light"] h6 { color: #111; }
[data-theme="light"] p, [data-theme="light"] span, [data-theme="light"] li { color: #333; }
[data-theme="light"] .card, [data-theme="light"] .prod-card, [data-theme="light"] .program-card, [data-theme="light"] .trainer-card, [data-theme="light"] .faq-item { background: #fff; border-color: #ddd; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
[data-theme="light"] .navbar, [data-theme="light"] .store-nav { background: rgba(255, 255, 255, 0.95); border-bottom: 1px solid #ddd; }
[data-theme="light"] .nav-links a, [data-theme="light"] .nav-brand .logo-text { color: #111 !important; }
[data-theme="light"] .btn-ghost { color: #111; border-color: #ccc; }
[data-theme="light"] input, [data-theme="light"] textarea, [data-theme="light"] select { background: #fff; border: 1px solid #ccc; color: #111; }
[data-theme="light"] .mega-footer { background: #fdfdfd; border-top: 1px solid #eee; }
"""

for path in css_files:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "UNIVERSAL LIGHT THEME SUPPORT" not in content:
            with open(path, "a", encoding="utf-8") as f:
                f.write(generic_light_block)
            print(f"Added light theme to {path}")

# --- PART 2: UNIQUE AUTH TOGGLERS ---
login_html_path = r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\templates\account\login.html"
signup_html_path = r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\templates\account\signup.html"

# New Login Toggler (Circular Neon Purple)
login_toggler = """
    <!-- Premium Circular Toggler for Login -->
    <div class="auth-theme-toggle" id="themeToggleBtn" onclick="toggleAuthTheme()" style="position:fixed; top:30px; right:30px; z-index:1000; width:50px; height:50px; background:rgba(196,77,255,0.15); border:1px solid rgba(196,77,255,0.3); border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; backdrop-filter:blur(10px); transition:0.4s; box-shadow: 0 8px 32px rgba(196,77,255,0.2);">
      <i id="themeIcon" class="fas fa-moon" style="color:#c44dff; font-size:1.4rem;"></i>
    </div>
"""

login_script = """
    <script>
      function setAuthTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('fitx_theme', theme);
        const icon = document.getElementById('themeIcon');
        if(theme === 'light') {
          icon.className = 'fas fa-sun';
          icon.style.color = '#ff9f43';
          document.getElementById('themeToggleBtn').style.background = 'rgba(255,159,67,0.15)';
          document.getElementById('themeToggleBtn').style.borderColor = 'rgba(255,159,67,0.3)';
        } else {
          icon.className = 'fas fa-moon';
          icon.style.color = '#c44dff';
          document.getElementById('themeToggleBtn').style.background = 'rgba(196,77,255,0.15)';
          document.getElementById('themeToggleBtn').style.borderColor = 'rgba(196,77,255,0.3)';
        }
      }
      function toggleAuthTheme() {
        const curr = localStorage.getItem('fitx_theme') || 'dark';
        setAuthTheme(curr === 'dark' ? 'light' : 'dark');
      }
      // Initial Load
      const saved = localStorage.getItem('fitx_theme') || 'dark';
      setAuthTheme(saved);
    </script>
"""

# New Signup Toggler (Rounded Rectangle Switch)
signup_toggler = """
    <!-- Premium Switch Toggler for Signup -->
    <div class="auth-theme-toggle" onclick="toggleAuthTheme()" style="position:fixed; top:30px; right:30px; z-index:1000; padding:8px 16px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:30px; display:flex; align-items:center; gap:12px; cursor:pointer; backdrop-filter:blur(10px); transition:0.3s;">
      <span id="themeText" style="font-size:0.75rem; font-weight:700; color:#fff; text-transform:uppercase; letter-spacing:1px;">Dark Mode</span>
      <div id="switchBall" style="width:20px; height:20px; border-radius:50%; background:#c44dff; box-shadow:0 0 10px #c44dff; transition:0.3s;"></div>
    </div>
"""

signup_script = """
    <script>
      function setAuthTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('fitx_theme', theme);
        const text = document.getElementById('themeText');
        const ball = document.getElementById('switchBall');
        if(theme === 'light') {
          text.innerText = 'Light Mode';
          text.style.color = '#555';
          ball.style.transform = 'translateX(0)';
          ball.style.background = '#ff9f43';
          ball.style.boxShadow = '0 0 10px #ff9f43';
        } else {
          text.innerText = 'Dark Mode';
          text.style.color = '#fff';
          ball.style.background = '#c44dff';
          ball.style.boxShadow = '0 0 10px #c44dff';
        }
      }
      function toggleAuthTheme() {
        const curr = localStorage.getItem('fitx_theme') || 'dark';
        setAuthTheme(curr === 'dark' ? 'light' : 'dark');
      }
      const saved = localStorage.getItem('fitx_theme') || 'dark';
      setAuthTheme(saved);
    </script>
"""

# Update Login HTML
if os.path.exists(login_html_path):
    with open(login_html_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Remove old toggler if any
    import re
    content = re.sub(r'<!-- Theme Toggler specifically for this page -->.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- Premium Circular Toggler for Login -->.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- Auth Theme Script -->.*?<script>.*?</script>', '', content, flags=re.DOTALL)
    
    # Insert new ones
    content = content.replace('<body>', '<body>\n' + login_toggler)
    content = content.replace('</body>', login_script + '\n</body>')
    with open(login_html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated Login Toggler")

# Update Signup HTML
if os.path.exists(signup_html_path):
    with open(signup_html_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'<!-- Theme Toggler specifically for this page -->.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- Premium Switch Toggler for Signup -->.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- Auth Theme Script -->.*?<script>.*?</script>', '', content, flags=re.DOTALL)

    content = content.replace('<body>', '<body>\n' + signup_toggler)
    content = content.replace('</body>', signup_script + '\n</body>')
    with open(signup_html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated Signup Toggler")
