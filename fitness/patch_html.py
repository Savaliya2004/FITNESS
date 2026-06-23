import os
import re

filepath = r"c:\Users\Dev\Desktop\FITNESS\env\fitness\account\templates\account\admin_dashboard.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Add Exercise button
content = content.replace(
    '''<a href="{% url 'admin:workout_exercise_add' %}" class="btn btn-primary btn-sm" target="_blank">+ Add Exercise</a>''',
    '''<button type="button" onclick="openExerciseModal()" class="btn btn-primary btn-sm">+ Add Exercise</button>'''
)

# Replace Add Blog Post button
content = content.replace(
    '''<a href="{% url 'admin:core_blogpost_add' %}" class="btn btn-primary btn-sm" target="_blank">+ New Article</a>''',
    '''<button type="button" onclick="openBlogPostModal()" class="btn btn-primary btn-sm">+ New Article</button>'''
)

# Replace Add Challenge button
content = content.replace(
    '''<a href="{% url 'admin:core_challenge_add' %}" class="btn btn-primary btn-sm" target="_blank">+ New Challenge</a>''',
    '''<button type="button" onclick="openChallengeModal()" class="btn btn-primary btn-sm">+ New Challenge</button>'''
)

# Replace Django Admin Link
content = content.replace(
    '''<a href="{% url 'admin:index' %}" target="_blank" class="btn btn-primary btn-sm">Open Django Admin →</a>''',
    ''''''
)

# Exercise table actions
ex_th = '''<th>Type</th>
              <th>Difficulty</th>
              <th>Reps/Sets</th>
              <th>Calories</th>'''
ex_th_new = '''<th>Type</th>
              <th>Difficulty</th>
              <th>Reps/Sets</th>
              <th>Calories</th>
              <th class="text-right">Actions</th>'''
content = content.replace(ex_th, ex_th_new)

ex_td = '''<td><span class="badge badge-success">{{ ex.difficulty }}</span></td>
                  <td>{{ ex.reps_sets }}</td>
                  <td>{{ ex.calories_burned }}</td>
                </tr>'''
ex_td_new = '''<td><span class="badge badge-success">{{ ex.difficulty }}</span></td>
                  <td>{{ ex.reps_sets }}</td>
                  <td>{{ ex.calories_burned }}</td>
                  <td class="text-right">
                    <button type="button" onclick="openExerciseModal('{{ ex.id }}', '{{ ex.name|escapejs }}', '{{ ex.category }}', '{{ ex.exercise_type }}', '{{ ex.difficulty|escapejs }}', '{{ ex.reps_sets|escapejs }}', '{{ ex.calories_burned }}', '{{ ex.video_url|escapejs }}', '{{ ex.steps|escapejs }}')" class="btn btn-sm" style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary)">Edit</button>
                    <a href="{% url 'admin_delete_exercise' ex.id %}" class="btn btn-sm" style="background:rgba(244,63,94,0.1);color:var(--rose-light)" onclick="return confirm('Delete this exercise?')">Delete</a>
                  </td>
                </tr>'''
content = content.replace(ex_td, ex_td_new)

# Blog table actions
blog_th = '''<th>Category</th>
              <th>Status</th>
              <th>Views</th>
              <th>Date</th>'''
blog_th_new = '''<th>Category</th>
              <th>Status</th>
              <th>Views</th>
              <th>Date</th>
              <th class="text-right">Actions</th>'''
content = content.replace(blog_th, blog_th_new)

blog_td = '''<td>{{ post.views_count }}</td>
                  <td>{{ post.created_at|date:"M d, Y" }}</td>
                </tr>'''
blog_td_new = '''<td>{{ post.views_count }}</td>
                  <td>{{ post.created_at|date:"M d, Y" }}</td>
                  <td class="text-right">
                    <button type="button" onclick="openBlogPostModal('{{ post.id }}', '{{ post.title|escapejs }}', '{{ post.content|escapejs }}', '{{ post.status }}')" class="btn btn-sm" style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary)">Edit</button>
                    <a href="{% url 'admin_delete_blogpost' post.id %}" class="btn btn-sm" style="background:rgba(244,63,94,0.1);color:var(--rose-light)" onclick="return confirm('Delete this blog post?')">Delete</a>
                  </td>
                </tr>'''
content = content.replace(blog_td, blog_td_new)


# Challenge table actions
ch_th = '''<th>Participants</th>
              <th>Status</th>
              <th>Reward</th>
              <th>Deadline</th>'''
ch_th_new = '''<th>Participants</th>
              <th>Status</th>
              <th>Reward</th>
              <th>Deadline</th>
              <th class="text-right">Actions</th>'''
content = content.replace(ch_th, ch_th_new)

ch_td = '''<td>{{ ch.reward }} ({{ ch.reward_xp }} XP)</td>
                  <td>{{ ch.end_date|date:"M d, Y" }}</td>
                </tr>'''
ch_td_new = '''<td>{{ ch.reward }} ({{ ch.reward_xp }} XP)</td>
                  <td>{{ ch.end_date|date:"M d, Y" }}</td>
                  <td class="text-right">
                    <button type="button" onclick="openChallengeModal('{{ ch.id }}', '{{ ch.title|escapejs }}', '{{ ch.description|escapejs }}', '{{ ch.start_date|date:"Y-m-d" }}', '{{ ch.end_date|date:"Y-m-d" }}', '{{ ch.difficulty }}', '{{ ch.status }}')" class="btn btn-sm" style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary)">Edit</button>
                    <a href="{% url 'admin_delete_challenge' ch.id %}" class="btn btn-sm" style="background:rgba(244,63,94,0.1);color:var(--rose-light)" onclick="return confirm('Delete this challenge?')">Delete</a>
                  </td>
                </tr>'''
content = content.replace(ch_td, ch_td_new)


# Add Modals and CSS/JS
MODALS = """
<!-- ================== CUSTOM MODALS ================== -->
<style>
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.6); backdrop-filter: blur(5px);
  z-index: 9999; display: none; align-items: center; justify-content: center;
  opacity: 0; transition: opacity 0.3s;
}
.modal-overlay.show { opacity: 1; }
.modal-content {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius-lg); width: 100%; max-width: 600px;
  max-height: 90vh; overflow-y: auto; transform: scale(0.95);
  transition: transform 0.3s; padding: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}
.modal-overlay.show .modal-content { transform: scale(1); }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 12px; }
.modal-title { font-size: 18px; font-weight: 700; }
.btn-close { background: none; border: none; color: var(--text-muted); font-size: 24px; cursor: pointer; }
.btn-close:hover { color: var(--text-primary); }

.form-group { margin-bottom: 16px; }
.form-label { display: block; font-size: 13px; color: var(--text-secondary); margin-bottom: 6px; }
.form-control {
  width: 100%; background: var(--bg-glass); border: 1px solid var(--border);
  color: var(--text-primary); padding: 10px 14px; border-radius: 8px; font-size: 14px;
}
.form-control:focus { outline: none; border-color: var(--purple); }
.modal-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 24px; }
</style>

<!-- Exercise Modal -->
<div id="exerciseModal" class="modal-overlay">
  <div class="modal-content">
    <div class="modal-header">
      <div class="modal-title" id="exModalTitle">Add Exercise</div>
      <button class="btn-close" onclick="closeModal('exerciseModal')">&times;</button>
    </div>
    <form id="exForm" method="POST" action="{% url 'admin_add_exercise' %}">
      {% csrf_token %}
      <div class="form-group">
        <label class="form-label">Name</label>
        <input type="text" name="name" id="ex_name" class="form-control" required>
      </div>
      <div style="display:flex;gap:16px;">
        <div class="form-group" style="flex:1;">
          <label class="form-label">Category</label>
          <select name="category" id="ex_category" class="form-control">
            <option value="strength">Strength Training</option>
            <option value="cardio">Cardio</option>
            <option value="hiit">HIIT</option>
            <option value="yoga">Yoga</option>
            <option value="home">Home Workout</option>
            <option value="flexibility">Flexibility</option>
          </select>
        </div>
        <div class="form-group" style="flex:1;">
          <label class="form-label">Type</label>
          <select name="exercise_type" id="ex_type" class="form-control">
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
            <option value="core">Core</option>
            <option value="fullbody">Full Body</option>
            <option value="basics">Basics</option>
            <option value="cardio">Cardio Blast</option>
          </select>
        </div>
      </div>
      <div style="display:flex;gap:16px;">
        <div class="form-group" style="flex:1;">
          <label class="form-label">Difficulty</label>
          <input type="text" name="difficulty" id="ex_diff" class="form-control" value="Beginner" required>
        </div>
        <div class="form-group" style="flex:1;">
          <label class="form-label">Reps/Sets</label>
          <input type="text" name="reps_sets" id="ex_reps" class="form-control" value="3 sets of 10" required>
        </div>
        <div class="form-group" style="flex:1;">
          <label class="form-label">Calories</label>
          <input type="number" name="calories_burned" id="ex_cal" class="form-control" value="50" required>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">Video URL</label>
        <input type="url" name="video_url" id="ex_video" class="form-control">
      </div>
      <div class="form-group">
        <label class="form-label">Steps</label>
        <textarea name="steps" id="ex_steps" class="form-control" rows="3"></textarea>
      </div>
      <div class="modal-actions">
        <button type="button" class="btn" style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary)" onclick="closeModal('exerciseModal')">Cancel</button>
        <button type="submit" class="btn btn-primary">Save Exercise</button>
      </div>
    </form>
  </div>
</div>

<!-- Blog Post Modal -->
<div id="blogModal" class="modal-overlay">
  <div class="modal-content">
    <div class="modal-header">
      <div class="modal-title" id="blogModalTitle">Add Blog Post</div>
      <button class="btn-close" onclick="closeModal('blogModal')">&times;</button>
    </div>
    <form id="blogForm" method="POST" action="{% url 'admin_add_blogpost' %}">
      {% csrf_token %}
      <div class="form-group">
        <label class="form-label">Title</label>
        <input type="text" name="title" id="blog_title" class="form-control" required>
      </div>
      <div class="form-group">
        <label class="form-label">Status</label>
        <select name="status" id="blog_status" class="form-control">
          <option value="draft">Draft</option>
          <option value="published">Published</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Content</label>
        <textarea name="content" id="blog_content" class="form-control" rows="8" required></textarea>
      </div>
      <div class="modal-actions">
        <button type="button" class="btn" style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary)" onclick="closeModal('blogModal')">Cancel</button>
        <button type="submit" class="btn btn-primary">Save Post</button>
      </div>
    </form>
  </div>
</div>

<!-- Challenge Modal -->
<div id="challengeModal" class="modal-overlay">
  <div class="modal-content">
    <div class="modal-header">
      <div class="modal-title" id="chModalTitle">Add Challenge</div>
      <button class="btn-close" onclick="closeModal('challengeModal')">&times;</button>
    </div>
    <form id="chForm" method="POST" action="{% url 'admin_add_challenge' %}">
      {% csrf_token %}
      <div class="form-group">
        <label class="form-label">Title</label>
        <input type="text" name="title" id="ch_title" class="form-control" required>
      </div>
      <div style="display:flex;gap:16px;">
        <div class="form-group" style="flex:1;">
          <label class="form-label">Start Date</label>
          <input type="date" name="start_date" id="ch_start" class="form-control" required>
        </div>
        <div class="form-group" style="flex:1;">
          <label class="form-label">End Date</label>
          <input type="date" name="end_date" id="ch_end" class="form-control" required>
        </div>
      </div>
      <div style="display:flex;gap:16px;">
        <div class="form-group" style="flex:1;">
          <label class="form-label">Difficulty</label>
          <select name="difficulty" id="ch_diff" class="form-control">
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
        <div class="form-group" style="flex:1;">
          <label class="form-label">Status</label>
          <select name="status" id="ch_status" class="form-control">
            <option value="upcoming">Upcoming</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">Description</label>
        <textarea name="description" id="ch_desc" class="form-control" rows="4" required></textarea>
      </div>
      <div class="modal-actions">
        <button type="button" class="btn" style="background:var(--bg-glass);border:1px solid var(--border);color:var(--text-primary)" onclick="closeModal('challengeModal')">Cancel</button>
        <button type="submit" class="btn btn-primary">Save Challenge</button>
      </div>
    </form>
  </div>
</div>

<script>
function openModal(id) {
  const m = document.getElementById(id);
  m.style.display = 'flex';
  setTimeout(() => m.classList.add('show'), 10);
}
function closeModal(id) {
  const m = document.getElementById(id);
  m.classList.remove('show');
  setTimeout(() => m.style.display = 'none', 300);
}

function openExerciseModal(id, name, cat, type, diff, reps, cal, vid, steps) {
  const form = document.getElementById('exForm');
  if (id) {
    document.getElementById('exModalTitle').innerText = 'Edit Exercise';
    form.action = `/accounts/admin-panel/exercise/edit/${id}/`;
    document.getElementById('ex_name').value = name || '';
    document.getElementById('ex_category').value = cat || 'strength';
    document.getElementById('ex_type').value = type || 'beginner';
    document.getElementById('ex_diff').value = diff || '';
    document.getElementById('ex_reps').value = reps || '';
    document.getElementById('ex_cal').value = cal || '';
    document.getElementById('ex_video').value = vid || '';
    document.getElementById('ex_steps').value = steps || '';
  } else {
    document.getElementById('exModalTitle').innerText = 'Add Exercise';
    form.action = "{% url 'admin_add_exercise' %}";
    form.reset();
  }
  openModal('exerciseModal');
}

function openBlogPostModal(id, title, content, status) {
  const form = document.getElementById('blogForm');
  if (id) {
    document.getElementById('blogModalTitle').innerText = 'Edit Blog Post';
    form.action = `/accounts/admin-panel/blog/edit/${id}/`;
    document.getElementById('blog_title').value = title || '';
    document.getElementById('blog_content').value = content || '';
    document.getElementById('blog_status').value = status || 'draft';
  } else {
    document.getElementById('blogModalTitle').innerText = 'Add Blog Post';
    form.action = "{% url 'admin_add_blogpost' %}";
    form.reset();
  }
  openModal('blogModal');
}

function openChallengeModal(id, title, desc, start, end, diff, status) {
  const form = document.getElementById('chForm');
  if (id) {
    document.getElementById('chModalTitle').innerText = 'Edit Challenge';
    form.action = `/accounts/admin-panel/challenge/edit/${id}/`;
    document.getElementById('ch_title').value = title || '';
    document.getElementById('ch_desc').value = desc || '';
    document.getElementById('ch_start').value = start || '';
    document.getElementById('ch_end').value = end || '';
    document.getElementById('ch_diff').value = diff || 'beginner';
    document.getElementById('ch_status').value = status || 'upcoming';
  } else {
    document.getElementById('chModalTitle').innerText = 'Add Challenge';
    form.action = "{% url 'admin_add_challenge' %}";
    form.reset();
  }
  openModal('challengeModal');
}
</script>
"""

content = content.replace("</body>", MODALS + "\n</body>")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch complete.")
