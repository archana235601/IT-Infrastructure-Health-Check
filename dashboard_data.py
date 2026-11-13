import sqlite3
from health_check import get_health_status

def get_dashboard_data():
    health = get_health_status()

    con = sqlite3.connect("incidents.db")
    total = con.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
    recent = con.execute(
        "SELECT * FROM incidents ORDER BY rowid DESC LIMIT 5"
    ).fetchall()
    con.close()

    return total, recent, health
