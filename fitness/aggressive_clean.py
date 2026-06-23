import os

FILES = [
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\static\account\css\dashboard.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\account\static\account\css\success.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\blog.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\community.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\contact.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\index.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\membership.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\story.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\static\diet\css\diet-gain.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\static\diet\css\diet-lose.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\diet\static\diet\css\diet.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store-men.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\store\static\store\css\store-women.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\coaches.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\fitness.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\sport.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\trainers.css",
    r"c:\Users\Dev\Desktop\PROJECT\env\fitness\workout\static\workout\css\workouts.css",
]

def clean_extreme(path):
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # If line contains spaced out 'c h a r t' or 'b a c k d r o p'
        if "c h a r t" in line or "b a c k d r o p" in line or "s e c t i o n" in line or "w o r k o u t" in line:
            continue
        new_lines.append(line)
    
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"Aggressively cleaned {path}")

for p in FILES: clean_extreme(p)
