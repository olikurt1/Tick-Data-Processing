import sqlite3
import pandas as pd

DB_PATH = "ticks.db"

#initialising database
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
        #adding indexes for filtering 
        conn.execute("CREATE INDEX IF NOT EXISTS idx_date ON sightings(date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_location ON sightings(location)")

#checks if value is Na before adding to database, returns None if Na and value if value exists
def value_to_db(value):
    if pd.isna(value):
        return None
    else:
        return value

def save_sightings(df):
    rows = []
    for row in df.itertuples():
        rows.append((row.id, row.date.strftime("%Y-%m-%dT%H:%M:%S"), row.location, value_to_db(row.species), value_to_db(row.latinName)))

    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO sightings (id, date, location, species, latinName) " 
            "VALUES (?, ?, ?, ?, ?)",
            rows

        )
    return len(rows)

    
