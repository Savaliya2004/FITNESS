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

def final_clean(path):
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        stripped = line.strip()
        # If line has lots of single letters with spaces
        # e.g. " . c h a r t"
        if len(stripped) > 10:
            words = stripped.split()
            single_letter_words = [w for w in words if len(w) == 1]
            if len(single_letter_words) / len(words) > 0.5:
                continue
        new_lines.append(line)
    
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"Final clean of {path}")

for p in FILES: final_clean(p)
