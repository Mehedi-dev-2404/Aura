import sqlite3


def getconnection():
    conn = sqlite3.connect("aura.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        priority TEXT NOT NULL,
        energy_required TEXT NOT NULL,
        deadline TEXT NOT NULL,
        estimated_duration INTEGER NOT NULL,
        status TEXT NOT NULL
    )
    """)
    conn.commit()
    return conn