import sqlite3

DB_PATH = "ticks.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sightings (
                id TEXT PRIMARY KEY,
                date TEXT NOT NULL,
                location TEXT NOT NULL,
                species TEXT, 
                latinName TEXT
            )
""")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_date ON sightings(date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_location ON sightings(location)")