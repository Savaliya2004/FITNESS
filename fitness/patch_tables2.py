filepath = r"c:\Users\Dev\Desktop\FITNESS\env\fitness\account\templates\account\admin_dashboard.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ─── 1. EXERCISE ROW ────────────────────────────────────────────────────────
OLD_EX = '                <td class="text-muted">{{ ex.muscle_group|default:"\u2014" }}</td>\n              </tr>'
NEW_EX = ('                <td class="text-muted">{{ ex.muscle_group|default:"\u2014" }}</td>\n'
           '                <td class="text-right" style="white-space:nowrap">\n'
           '                  <button type="button" onclick="openExerciseModal(\'{{ ex.id }}\',\'{{ ex.name|escapejs }}\',\'{{ ex.category }}\',\'{{ ex.exercise_type }}\',\'{{ ex.difficulty|escapejs }}\',\'{{ ex.reps_sets|escapejs }}\',\'{{ ex.calories_burned }}\',\'{{ ex.video_url|escapejs }}\',\'{{ ex.steps|escapejs }}\')" '
           'style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary);padding:4px 10px;border-radius:6px;font-size:12px;cursor:pointer;margin-right:4px;">Edit</button>\n'
           '                  <a href="{% url \'admin_delete_exercise\' ex.id %}" onclick="return confirm(\'Delete exercise?\')" '
           'style="background:rgba(244,63,94,0.12);border:1px solid rgba(244,63,94,0.3);color:var(--rose-light);padding:4px 10px;border-radius:6px;font-size:12px;">Delete</a>\n'
           '                </td>\n'
           '              </tr>')

if OLD_EX in content:
    content = content.replace(OLD_EX, NEW_EX, 1)
    print("[OK] Exercise row patched.")
else:
    print("[FAIL] Exercise row NOT found.")

# ─── 2. BLOG ROW ────────────────────────────────────────────────────────────
OLD_BLOG = ('                <td class="text-muted fs-xs">{{ post.created_at|date:"d M Y" }}</td>\n'
            '              </tr>')
NEW_BLOG = ('                <td class="text-muted fs-xs">{{ post.created_at|date:"d M Y" }}</td>\n'
            '                <td class="text-right" style="white-space:nowrap">\n'
            '                  <button type="button" onclick="openBlogPostModal(\'{{ post.id }}\',\'{{ post.title|escapejs }}\',\'{{ post.content|escapejs }}\',\'{{ post.status }}\')" '
            'style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary);padding:4px 10px;border-radius:6px;font-size:12px;cursor:pointer;margin-right:4px;">Edit</button>\n'
            '                  <a href="{% url \'admin_delete_blogpost\' post.id %}" onclick="return confirm(\'Delete this blog post?\')" '
            'style="background:rgba(244,63,94,0.12);border:1px solid rgba(244,63,94,0.3);color:var(--rose-light);padding:4px 10px;border-radius:6px;font-size:12px;">Delete</a>\n'
            '                </td>\n'
            '              </tr>')

if OLD_BLOG in content:
    content = content.replace(OLD_BLOG, NEW_BLOG, 1)
    print("[OK] Blog row patched.")
else:
    print("[FAIL] Blog row NOT found.")

# ─── 3. CHALLENGE ROW ───────────────────────────────────────────────────────
OLD_CH = ('                <td class="text-muted fs-xs">{{ ch.start_date|date:"d M" }} \u2013 {{ ch.end_date|date:"d M Y" }}</td>\n'
          '              </tr>')
NEW_CH = ('                <td class="text-muted fs-xs">{{ ch.start_date|date:"d M" }} \u2013 {{ ch.end_date|date:"d M Y" }}</td>\n'
          '                <td class="text-right" style="white-space:nowrap">\n'
          '                  <button type="button" onclick="openChallengeModal(\'{{ ch.id }}\',\'{{ ch.title|escapejs }}\',\'{{ ch.description|escapejs }}\',\'{{ ch.start_date|date:"Y-m-d" }}\',\'{{ ch.end_date|date:"Y-m-d" }}\',\'{{ ch.difficulty }}\',\'{{ ch.status }}\')" '
          'style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary);padding:4px 10px;border-radius:6px;font-size:12px;cursor:pointer;margin-right:4px;">Edit</button>\n'
          '                  <a href="{% url \'admin_delete_challenge\' ch.id %}" onclick="return confirm(\'Delete this challenge?\')" '
          'style="background:rgba(244,63,94,0.12);border:1px solid rgba(244,63,94,0.3);color:var(--rose-light);padding:4px 10px;border-radius:6px;font-size:12px;">Delete</a>\n'
          '                </td>\n'
          '              </tr>')

if OLD_CH in content:
    content = content.replace(OLD_CH, NEW_CH, 1)
    print("[OK] Challenge row patched.")
else:
    print("[FAIL] Challenge row NOT found.")
    # Debug: print what the end of ch row looks like
    idx = content.find('ch.end_date')
    if idx != -1:
        print("  end_date context:", repr(content[idx:idx+120]))

# ─── 4. ADD Actions TH headers ──────────────────────────────────────────────
# Blog table header - look for date header inside thead
# Find blog table first (look for post.created_at)
blog_th_idx = content.find('post.views_count')
if blog_th_idx != -1:
    # Look back for the thead row
    thead_start = content.rfind('<thead>', 0, blog_th_idx)
    thead_end = content.find('</thead>', thead_start) + 8
    old_blog_head = content[thead_start:thead_end]
    if '</tr></thead>' in old_blog_head or '</tr>\n</thead>' in old_blog_head:
        # Add Actions before closing tr
        new_blog_head = old_blog_head.replace('</tr>', '<th class="text-right">Actions</th></tr>', 1)
        content = content[:thead_start] + new_blog_head + content[thead_end:]
        print("[OK] Blog table header patched.")
    else:
        print("[WARN] Blog thead closing pattern not expected.")

# Challenge table header
ch_th_idx = content.find('ch.current_participants')
if ch_th_idx != -1:
    thead_start = content.rfind('<thead>', 0, ch_th_idx)
    thead_end = content.find('</thead>', thead_start) + 8
    old_ch_head = content[thead_start:thead_end]
    new_ch_head = old_ch_head.replace('</tr>', '<th class="text-right">Actions</th></tr>', 1)
    content = content[:thead_start] + new_ch_head + content[thead_end:]
    print("[OK] Challenge table header patched.")

# Fix blog empty state colspan (now 7)
content = content.replace(
    'for post in blog_posts %}',
    'for post in blog_posts %}'
)
# Fix colspan=6 to 7 for blog empty state
blog_empty = 'colspan="6"><div class="empty-state"><div class="empty-state-icon">\U0001f4dd'
if blog_empty in content:
    content = content.replace(
        'colspan="6"><div class="empty-state"><div class="empty-state-icon">\U0001f4dd',
        'colspan="7"><div class="empty-state"><div class="empty-state-icon">\U0001f4dd',
        1
    )
    print("[OK] Blog empty state colspan fixed.")

# Fix challenge empty state colspan
ch_empty_idx = content.find('for ch in challenges %}')
if ch_empty_idx != -1:
    empty_idx = content.find('colspan="6"', ch_empty_idx)
    if empty_idx != -1:
        content = content[:empty_idx] + 'colspan="7"' + content[empty_idx+11:]
        print("[OK] Challenge empty state colspan fixed.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone!")
