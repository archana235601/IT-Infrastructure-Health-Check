import sqlite3

con = sqlite3.connect("incidents.db")

con.execute(
    "ALTER TABLE incidents ADD COLUMN status TEXT DEFAULT 'Pending'"
)

con.commit()
con.close()

print("Status column added successfully!")
