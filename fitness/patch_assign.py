import os

filepath = r"c:\Users\Dev\Desktop\FITNESS\env\fitness\account\templates\account\admin_dashboard.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Assign button to users table
old_btn_marker = "{% if not u.is_superuser %}"
new_btn = """{% if not u.is_superuser %}
                    <button type="button" class="btn btn-info btn-xs" style="background:var(--cyan);border-color:var(--cyan);color:#fff;" onclick="openAssignModal('{{ u.id }}', '{{ u.username|escapejs }}')">Assign Plans</button>"""

if old_btn_marker in content:
    # Need to be careful, it might occur multiple times?
    # Let's count
    if content.count(old_btn_marker) == 1:
        content = content.replace(old_btn_marker, new_btn)
        print("Assign button added to users table.")
    else:
        # replace only in the users-table block
        idx = content.find('users-table')
        if idx != -1:
            idx2 = content.find(old_btn_marker, idx)
            if idx2 != -1:
                content = content[:idx2] + new_btn + content[idx2 + len(old_btn_marker):]
                print("Assign button added to users table (targeted).")
else:
    print("WARNING: Could not find user table actions.")

# 2. Add Assign Modal and JS
assign_modal_html = """
<!-- Assign Plans Modal -->
<div id="assignModal" class="modal-overlay">
  <div class="modal-content" style="max-width: 800px;">
    <div class="modal-header">
      <div class="modal-title" id="assignModalTitle">Assign Plans to User</div>
      <button class="btn-close" onclick="closeModal('assignModal')">&times;</button>
    </div>
    
    <div style="display:flex; gap:20px;">
      <!-- Assign Exercise Section -->
      <div style="flex:1; border-right: 1px solid var(--border); padding-right: 20px;">
        <h4 style="margin-top:0; color:var(--text-primary);">Assign Workout</h4>
        <form id="assignExerciseForm" method="POST" action="">
          {% csrf_token %}
          <div class="form-group">
            <label class="form-label">Select Exercise</label>
            <select name="exercise_id" class="form-control" required>
              <option value="">-- Choose an Exercise --</option>
              {% for ex in exercises %}
              <option value="{{ ex.id }}">{{ ex.name }} ({{ ex.category }})</option>
              {% endfor %}
            </select>
          </div>
          <button type="submit" class="btn btn-primary" style="width:100%;">Assign Exercise</button>
        </form>
      </div>
      
      <!-- Assign Diet Plan Section -->
      <div style="flex:1;">
        <h4 style="margin-top:0; color:var(--text-primary);">Create Diet Plan</h4>
        <form id="assignMealForm" method="POST" action="">
          {% csrf_token %}
          <div class="form-group">
            <label class="form-label">Day of Week</label>
            <select name="day_of_week" class="form-control" required>
              <option value="monday">Monday</option>
              <option value="tuesday">Tuesday</option>
              <option value="wednesday">Wednesday</option>
              <option value="thursday">Thursday</option>
              <option value="friday">Friday</option>
              <option value="saturday">Saturday</option>
              <option value="sunday">Sunday</option>
            </select>
          </div>
          
          <div style="display:flex;gap:10px;">
            <div class="form-group" style="flex:1;">
              <label class="form-label">Calories</label>
              <input type="number" name="calories" class="form-control" placeholder="e.g. 2000" required>
            </div>
            <div class="form-group" style="flex:1;">
              <label class="form-label">Protein (g)</label>
              <input type="number" name="protein" class="form-control" placeholder="e.g. 150" required>
            </div>
          </div>
          <div style="display:flex;gap:10px;">
            <div class="form-group" style="flex:1;">
              <label class="form-label">Carbs (g)</label>
              <input type="number" name="carbs" class="form-control" placeholder="e.g. 200" required>
            </div>
            <div class="form-group" style="flex:1;">
              <label class="form-label">Fats (g)</label>
              <input type="number" name="fats" class="form-control" placeholder="e.g. 60" required>
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-label">Breakfast</label>
            <input type="text" name="breakfast" class="form-control" placeholder="e.g. Oatmeal & Eggs">
          </div>
          <div class="form-group">
            <label class="form-label">Lunch</label>
            <input type="text" name="lunch" class="form-control" placeholder="e.g. Chicken & Rice">
          </div>
          <div class="form-group">
            <label class="form-label">Dinner</label>
            <input type="text" name="dinner" class="form-control" placeholder="e.g. Salmon & Greens">
          </div>
          <div class="form-group">
            <label class="form-label">Snacks</label>
            <input type="text" name="snacks" class="form-control" placeholder="e.g. Protein Shake">
          </div>
          
          <button type="submit" class="btn btn-primary" style="width:100%;">Create Meal Plan</button>
        </form>
      </div>
    </div>
  </div>
</div>

<script>
function openAssignModal(userId, username) {
  document.getElementById('assignModalTitle').innerText = 'Assign Plans to ' + username;
  document.getElementById('assignExerciseForm').action = '/accounts/admin-panel/user/' + userId + '/assign-exercise/';
  document.getElementById('assignMealForm').action = '/accounts/admin-panel/user/' + userId + '/assign-meal-plan/';
  openModal('assignModal');
}
</script>
"""

# inject before </body>
idx = content.find("</body>")
if idx != -1:
    content = content[:idx] + assign_modal_html + "\n" + content[idx:]
    print("Assign modal added.")
else:
    print("WARNING: Could not find </body>.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Template updated successfully.")
