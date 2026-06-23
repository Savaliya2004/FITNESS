import re

filepath = r"c:\Users\Dev\Desktop\FITNESS\env\fitness\account\templates\account\admin_dashboard.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ─── 1. EXERCISES ────────────────────────────────────────────────────
OLD_EX = '                <td class="text-muted">{{ ex.muscle_group|default:"\u2014" }}</td>\r\n               </tr>'
NEW_EX = '                <td class="text-muted">{{ ex.muscle_group|default:"\u2014" }}</td>\r\n                 <td class="text-right" style="white-space:nowrap">\r\n                   <button type="button" onclick="openExerciseModal(\'{{ ex.id }}\',\'{{ ex.name|escapejs }}\',\'{{ ex.category }}\',\'{{ ex.exercise_type }}\',\'{{ ex.difficulty|escapejs }}\',\'{{ ex.reps_sets|escapejs }}\',\'{{ ex.calories_burned }}\',\'{{ ex.video_url|escapejs }}\',\'{{ ex.steps|escapejs }}\')" style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary);padding:4px 10px;border-radius:6px;font-size:12px;cursor:pointer;margin-right:4px;">Edit</button>\r\n                   <a href="{% url \'admin_delete_exercise\' ex.id %}" onclick="return confirm(\'Delete exercise?\')" style="background:rgba(244,63,94,0.12);border:1px solid rgba(244,63,94,0.3);color:var(--rose-light);padding:4px 10px;border-radius:6px;font-size:12px;">Delete</a>\r\n                 </td>\r\n               </tr>'

if OLD_EX in content:
    content = content.replace(OLD_EX, NEW_EX, 1)
    print("[OK] Exercise row patched.")
else:
    print("[WARN] Exercise row NOT found.")

# ─── 2. BLOG POSTS ───────────────────────────────────────────────────
# Find the blog post table loop
old_blog = content.find('{% for post in blog_posts %}')
if old_blog == -1:
    print("[WARN] Blog loop not found")
else:
    # Find </tr> after the loop
    end_tr = content.find('</tr>', old_blog)
    row_snippet = content[old_blog:end_tr+5]
    # Check it has a closing tag before empty/endfor
    if 'blog_posts' in row_snippet and '{{ post.created_at|date:"M d, Y" }}</td>' in row_snippet:
        OLD_BLOG = '{{ post.created_at|date:"M d, Y" }}</td>\r\n                </tr>'
        NEW_BLOG = '{{ post.created_at|date:"M d, Y" }}</td>\r\n                  <td class="text-right" style="white-space:nowrap">\r\n                    <button type="button" onclick="openBlogPostModal(\'{{ post.id }}\',\'{{ post.title|escapejs }}\',\'{{ post.content|escapejs }}\',\'{{ post.status }}\')" style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary);padding:4px 10px;border-radius:6px;font-size:12px;cursor:pointer;margin-right:4px;">Edit</button>\r\n                    <a href="{% url \'admin_delete_blogpost\' post.id %}" onclick="return confirm(\'Delete this blog post?\')" style="background:rgba(244,63,94,0.12);border:1px solid rgba(244,63,94,0.3);color:var(--rose-light);padding:4px 10px;border-radius:6px;font-size:12px;">Delete</a>\r\n                  </td>\r\n                </tr>'
        if OLD_BLOG in content:
            content = content.replace(OLD_BLOG, NEW_BLOG, 1)
            print("[OK] Blog row patched.")
        else:
            print("[WARN] Blog row pattern not found.")
    else:
        print("[WARN] Blog row structure unexpected.")

# ─── 3. CHALLENGES ──────────────────────────────────────────────────────
old_ch = content.find('{% for ch in challenges %}')
if old_ch == -1:
    print("[WARN] Challenge loop not found")
else:
    if '{{ ch.end_date|date:"M d, Y" }}</td>' in content:
        OLD_CH = '{{ ch.end_date|date:"M d, Y" }}</td>\r\n                </tr>'
        NEW_CH = '{{ ch.end_date|date:"M d, Y" }}</td>\r\n                  <td class="text-right" style="white-space:nowrap">\r\n                    <button type="button" onclick="openChallengeModal(\'{{ ch.id }}\',\'{{ ch.title|escapejs }}\',\'{{ ch.description|escapejs }}\',\'{{ ch.start_date|date:"Y-m-d" }}\',\'{{ ch.end_date|date:"Y-m-d" }}\',\'{{ ch.difficulty }}\',\'{{ ch.status }}\')" style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary);padding:4px 10px;border-radius:6px;font-size:12px;cursor:pointer;margin-right:4px;">Edit</button>\r\n                    <a href="{% url \'admin_delete_challenge\' ch.id %}" onclick="return confirm(\'Delete this challenge?\')" style="background:rgba(244,63,94,0.12);border:1px solid rgba(244,63,94,0.3);color:var(--rose-light);padding:4px 10px;border-radius:6px;font-size:12px;">Delete</a>\r\n                  </td>\r\n                </tr>'
        if OLD_CH in content:
            content = content.replace(OLD_CH, NEW_CH, 1)
            print("[OK] Challenge row patched.")
        else:
            print("[WARN] Challenge row pattern not found.")

# ─── 4. Add Actions TH for blog and challenge tables ─────────────────
# Blog table header - look for Views/Date headers 
if '<th>Views</th>\r\n              <th>Date</th>\r\n            </tr>' in content:
    content = content.replace(
        '<th>Views</th>\r\n              <th>Date</th>\r\n            </tr>',
        '<th>Views</th>\r\n              <th>Date</th>\r\n              <th class="text-right">Actions</th>\r\n            </tr>',
        1
    )
    print("[OK] Blog table header patched.")
else:
    # Looser search
    if '<th>Views</th>' in content:
        print("[WARN] Blog Views th found but full pattern doesn't match. Investigate.")
    else:
        print("[WARN] Blog table header Views not found.")

# Challenge table header
if '<th>Deadline</th>\r\n            </tr>' in content:
    content = content.replace(
        '<th>Deadline</th>\r\n            </tr>',
        '<th>Deadline</th>\r\n              <th class="text-right">Actions</th>\r\n            </tr>',
        1
    )
    print("[OK] Challenge table header patched.")
else:
    if '<th>Deadline</th>' in content:
        print("[WARN] Deadline th found but full pattern doesn't match.")
    else:
        print("[WARN] Challenge Deadline th not found.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll patches saved.")
