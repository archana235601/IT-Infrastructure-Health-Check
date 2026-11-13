import psutil
import os
import sqlite3

def get_health_status():

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(os.path.abspath(os.sep))

    health = {
        "cpu": cpu,
        "memory": memory.percent,
        "disk": disk.percent
    }

    incidents = []

    if cpu > 80:
        incidents.append(("High CPU Usage", f"CPU: {cpu}%"))

    if memory.percent > 80:
        incidents.append(("High Memory Usage", f"RAM: {memory.percent}%"))

    if disk.percent > 90:
        incidents.append(("High Disk Usage", f"Disk: {disk.percent}%"))

    if incidents:
        con = sqlite3.connect("incidents.db")

        for title, description in incidents:
            con.execute(
                "INSERT INTO incidents (title, description) VALUES (?, ?)",
                (title, description)
            )

        con.commit()
        con.close()

    return health
