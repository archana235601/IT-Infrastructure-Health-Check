from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    from dashboard_data import get_dashboard_data
    total, recent, health = get_dashboard_data()
    return render_template("dashboard.html", total_incidents=total,
                           recent_incidents=recent, health=health)

# Health Check
@app.route("/health", methods=["GET", "POST"])
def health():
    from health_check import get_health_status
    data = get_health_status() if request.method == "POST" else None
    return render_template("health_check.html", health=data)

# Create Database
con = sqlite3.connect("incidents.db")
con.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    severity TEXT DEFAULT 'Medium',
    status TEXT DEFAULT 'Pending'
)
""")
columns = [row[1] for row in con.execute("PRAGMA table_info(incidents)")]
if "status" not in columns:
    con.execute("ALTER TABLE incidents ADD COLUMN status TEXT DEFAULT 'Pending'")
con.close()

# Incident Reporting
@app.route("/incidents", methods=["GET", "POST"])
def incidents():
    con = sqlite3.connect("incidents.db")
    if request.method == "POST":
        con.execute(
            "INSERT INTO incidents (title, description, severity) VALUES (?, ?, ?)",
            (request.form["title"], request.form["description"],
             request.form["severity"])
        )
        con.commit()
        con.close()
        return redirect("/incidents")

    search = request.args.get("search", "")
    severity = request.args.get("severity", "")
    query = "SELECT * FROM incidents WHERE title LIKE ?"
    params = ["%" + search + "%"]
    if severity:
        query += " AND severity = ?"
        params.append(severity)

    data = con.execute(query, params).fetchall()
    con.close()
    return render_template("incidents.html", incidents=data)

# Resolve Incident
@app.route("/resolve/<int:incident_id>", methods=["POST"])
def resolve_incident(incident_id):
    con = sqlite3.connect("incidents.db")
    con.execute("UPDATE incidents SET status = 'Resolved' WHERE id = ?",
                (incident_id,))
    con.commit()
    con.close()
    return redirect("/incidents")

if __name__ == "__main__":
    app.run(debug=True)

