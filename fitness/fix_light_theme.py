import os

store_css_path = r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store.css"

light_theme_css = """
/* LIGHT THEME OVERRIDES FOR STORE */
[data-theme="light"] {
    --bg: #f9f9fb;
    --bg2: #ffffff;
    --cardBg: #ffffff;
    --glassBorder: rgba(0, 0, 0, 0.1);
    --muted: #666666;
}
[data-theme="light"] body { background: var(--bg); color: #111; }
[data-theme="light"] .navbar { background: rgba(255, 255, 255, 0.95); border-bottom: 1px solid #ccc; }
[data-theme="light"] .nav-brand .logo-text { color: #111; }
[data-theme="light"] .store-nav { background: rgba(255, 255, 255, 0.95); border-bottom: 1px solid #ccc; color: #111; }
[data-theme="light"] .dropdown-menu { background: #fff; border: 1px solid #ccc; }
[data-theme="light"] .dropdown-item { color: #444; }
[data-theme="light"] .dropdown-item:hover { background: rgba(0,0,0,0.05); }
[data-theme="light"] .prod-card { background: #fff; border: 1px solid #ddd; }
[data-theme="light"] .prod-name { color: #111; }
[data-theme="light"] .price { color: #111; }
[data-theme="light"] .cart-icon-btn { color: #111; border-color: #ccc; }
[data-theme="light"] .mega-footer { background: #fdfdfd; border-top: 1px solid #ddd; }
[data-theme="light"] .f-brand h2 { color: #111; }
[data-theme="light"] .f-links h4 { color: #111; }
[data-theme="light"] .f-links a { color: #555; }
[data-theme="light"] .f-social i { color: #111; background: rgba(0,0,0,0.05); }
[data-theme="light"] .checkout-section-title { color: #111; }
[data-theme="light"] .form-input { background: #fff; border: 1px solid #ccc; color: #111; }
[data-theme="light"] .pay-card { background: #fff; border: 1px solid #ccc; color: #111; }
[data-theme="light"] .faq-item { background: #fff; border: 1px solid #ccc; }
[data-theme="light"] .faq-q { color: #111; }
[data-theme="light"] .checkout-summary-card { background: #fff; border: 1px solid #ccc; }
[data-theme="light"] .s-item-name, [data-theme="light"] .s-item-price { color: #111; }
[data-theme="light"] .summary-total { color: #111; border-top: 1px solid #ccc; }
[data-theme="light"] .btn-ghost { color: #111; border-color: #ccc; }
[data-theme="light"] .c-item-name { color: #111; }
[data-theme="light"] .cart-list, [data-theme="light"] .cart-summary { background: #fff; border-color: #ccc; }
"""

with open(store_css_path, "r", encoding="utf-8") as f:
    content = f.read()

if "LIGHT THEME OVERRIDES FOR STORE" not in content:
    with open(store_css_path, "a", encoding="utf-8") as f:
        f.write(light_theme_css)
    print("Added light theme CSS to store.css")
else:
    print("Light theme CSS already exists in store.css")

"""
Also need to fix login and signup page toggler.
"""
login_path = r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\templates\account\login.html"
signup_path = r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\templates\account\signup.html"

toggler_html = """
    <!-- Theme Toggler specifically for this page -->
    <div style="position: absolute; top: 20px; right: 20px; z-index: 100; display: flex; gap: 8px; background: rgba(0,0,0,0.2); padding: 5px 10px; border-radius: 20px; backdrop-filter: blur(10px);">
      <button onclick="setAuthTheme('dark')" style="background:transparent; border:none; cursor:pointer; font-size:1.1rem;" title="Dark Mode">🌙</button>
      <button onclick="setAuthTheme('light')" style="background:transparent; border:none; cursor:pointer; font-size:1.1rem;" title="Light Mode">☀️</button>
    </div>
"""

theme_script = """
    <!-- Auth Theme Script -->
    <script>
      const AUTH_THEME_KEY = 'fitx_theme';
      const authSavedTheme = localStorage.getItem(AUTH_THEME_KEY) || 'dark';
      document.documentElement.setAttribute('data-theme', authSavedTheme);

      function setAuthTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(AUTH_THEME_KEY, theme);
      }
    </script>
"""

# LOGIN HTML
with open(login_path, "r", encoding="utf-8") as f:
    login_content = f.read()

if "Auth Theme Script" not in login_content:
    login_content = login_content.replace('<body>', '<body>\n' + toggler_html)
    login_content = login_content.replace('</body>', theme_script + '\n</body>')
    with open(login_path, "w", encoding="utf-8") as f:
        f.write(login_content)
    print("Updated login.html")

# SIGNUP HTML
with open(signup_path, "r", encoding="utf-8") as f:
    signup_content = f.read()

if "Auth Theme Script" not in signup_content:
    signup_content = signup_content.replace('<body>', '<body>\n' + toggler_html)
    signup_content = signup_content.replace('</body>', theme_script + '\n</body>')
    with open(signup_path, "w", encoding="utf-8") as f:
        f.write(signup_content)
    print("Updated signup.html")

# ALSO need to ensure light theme rules exist in login.css and signup.css
login_css_path = r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\static\account\css\login.css"
signup_css_path = r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\static\account\css\signup.css"

auth_light_css = """
/* LIGHT THEME FOR AUTH */
[data-theme="light"] {
    --bg-dark: #f0f2f5;
    --card-bg: #ffffff;
    --text-main: #111111;
    --text-dim: #555555;
    --glass-border: rgba(0,0,0,0.1);
}
[data-theme="light"] body { background: var(--bg-dark); }
[data-theme="light"] body::before { display: none; }
[data-theme="light"] .auth-card { background: var(--card-bg); box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
[data-theme="light"] .form-control { background: #fdfdfd; border: 1px solid #ccc; color: #111; }
[data-theme="light"] .form-control::placeholder { color: #888; }
[data-theme="light"] .divider { color: #888; }
[data-theme="light"] .divider::before, [data-theme="light"] .divider::after { background: #ccc; }
[data-theme="light"] .btn-social { background: #f3f4f6; border-color: #ddd; color: #111; }
[data-theme="light"] .btn-social:hover { background: #e5e7eb; }
"""

with open(login_css_path, "r", encoding="utf-8") as f:
    content = f.read()
if "LIGHT THEME FOR AUTH" not in content:
    with open(login_css_path, "a", encoding="utf-8") as f:
        f.write(auth_light_css)
    print("Updated login.css")

with open(signup_css_path, "r", encoding="utf-8") as f:
    content = f.read()
if "LIGHT THEME FOR AUTH" not in content:
    with open(signup_css_path, "a", encoding="utf-8") as f:
        f.write(auth_light_css)
    print("Updated signup.css")
