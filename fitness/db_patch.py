import sqlite3
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute("UPDATE django_migrations SET app='local_account' WHERE app='account'")
cur.execute("UPDATE django_content_type SET app_label='local_account' WHERE app_label='account'")
conn.commit()
conn.close()
print("DB patched successfully.")
