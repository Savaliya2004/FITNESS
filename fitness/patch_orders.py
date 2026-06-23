import os

filepath = r"c:\Users\Dev\Desktop\FITNESS\env\fitness\account\templates\account\admin_dashboard.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

orders_table_html = """
      <div class="table-card" style="margin-top:20px;">
        <div class="table-card-header">
          <div class="table-card-title">🛍️ Store Orders</div>
          <div class="table-actions">
            <div class="table-search">
              <span class="table-search-icon">🔍</span>
              <input type="text" placeholder="Search orders..." oninput="filterTable('orders-table', this.value)">
            </div>
          </div>
        </div>
        <div style="overflow-x:auto;">
          <table class="data-table" id="orders-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>User</th>
                <th>Final Price</th>
                <th>Status</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {% for order in store_orders %}
              <tr>
                <td>#{{ order.id }}</td>
                <td>
                  <div class="user-cell">
                    <div class="user-avatar-sm">{{ order.user.username|slice:":1"|upper }}</div>
                    <div class="user-name">{{ order.user.username }}</div>
                  </div>
                </td>
                <td style="font-family: monospace;">₹{{ order.final_price }}</td>
                <td>
                  {% if order.status == 'pending' %}<span class="badge badge-amber">Pending</span>
                  {% elif order.status == 'shipped' %}<span class="badge badge-purple">Shipped</span>
                  {% elif order.status == 'delivered' %}<span class="badge badge-emerald">Delivered</span>
                  {% else %}<span class="badge badge-inactive">{{ order.status|title }}</span>{% endif %}
                </td>
                <td class="text-muted fs-xs">{{ order.created_at|date:"d M Y, h:i A" }}</td>
              </tr>
              {% empty %}
              <tr>
                <td colspan="5" class="text-center text-muted" style="padding:40px;">No store orders found.</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
"""

# find the end of the payments-table card.
# The structure is:
#       <div class="table-card">
#           ... payment table ...
#       </div>
#     </div> <!-- end of section-revenue -->

# Let's search for "<!-- end section-revenue -->" or similar, or just insert it right before `<div class="admin-section" id="section-content">`

idx = content.find('<div class="admin-section" id="section-content">')
if idx != -1:
    content = content[:idx] + orders_table_html + "\n    " + content[idx:]
    print("Store Orders table added before section-content.")
else:
    print("Could not find section-content.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Template patched.")
