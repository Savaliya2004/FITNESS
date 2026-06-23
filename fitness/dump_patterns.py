with open(r"c:\Users\Dev\Desktop\FITNESS\env\fitness\account\templates\account\admin_dashboard.html", 'r', encoding='utf-8') as f:
    content = f.read()

# Check exercise
ex_idx = content.find('muscle_group')
if ex_idx != -1:
    snippet = content[ex_idx-10:ex_idx+100]
    with open('debug_ex.txt', 'w', encoding='utf-8') as f:
        f.write(repr(snippet))
    print("Ex snippet written to debug_ex.txt")

# Check blog
blog_idx = content.find('blog_posts %}')
if blog_idx != -1:
    snippet2 = content[blog_idx:blog_idx+800]
    with open('debug_blog.txt', 'w', encoding='utf-8') as f:
        f.write(repr(snippet2))
    print("Blog snippet written to debug_blog.txt")

# Check challenge
ch_idx = content.find('challenges %}')
if ch_idx != -1:
    snippet3 = content[ch_idx:ch_idx+800]
    with open('debug_ch.txt', 'w', encoding='utf-8') as f:
        f.write(repr(snippet3))
    print("Challenge snippet written to debug_ch.txt")
