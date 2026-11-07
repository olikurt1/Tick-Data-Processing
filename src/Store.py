import sqlite3
import pandas as pd
from datetime import timedelta

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

#default parameter are possible filters but set to none as filter not applied until set
def search_sightings(startDate=None, endDate=None, locationFilter=None, speciesFilter=None, 
                        db_path=DB_PATH, limit=50, offset=0):
    conditions = []
    parameters = []        
    
    #if filter isn't empty append condition to be inserted into query and parameters to be inserted into query
        
    if startDate:
        conditions.append("date >= ?")
        parameters.append(startDate.isoformat())
    if endDate:
        conditions.append("date < ?")
        parameters.append((endDate + timedelta(days=1)).isoformat())
    if locationFilter:
        conditions.append("location = ? COLLATE NOCASE") #ignore capitals
        parameters.append(locationFilter)
    if speciesFilter:
        conditions.append("species = ? COLLATE NOCASE")
        parameters.append(speciesFilter)

    #building query sql statements
    sql = "SELECT * FROM sightings"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY date DESC LIMIT ? OFFSET ?"
    parameters += [limit, offset]

    #connect and query ticks.db with constructed SQL queries
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, parameters).fetchall()
    
    return [dict(row) for row in rows]

#Query database for sighting by id
def get_sighting(sightings_id, db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM sightings WHERE id = ?", (sightings_id,)).fetchone()
    #condition to handle lack of row if row with given id doesn't exist
    if row:
        return dict(row)
    else:
        return None

#groups rows by location and counts how many sightings each location has
def count_by_region(db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT location, COUNT(*) AS sightings FROM sightings "
        "GROUP BY location ORDER BY sightings DESC").fetchall()
    return [dict(row) for row in rows]

#group rows by period of time and count sightings for each period
FORMATS = {"month": "%Y-%m ", "week": "%Y-W%W "}

def count_by_period(period="month", db_path=DB_PATH):
    format = FORMATS[period]

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT strftime(?, date) AS period, COUNT(*) AS sighting from sightings "
        "GROUP BY period ORDER BY period", (format, )).fetchall()
    return [dict(row) for row in rows]

def count_sightings(db_path=DB_PATH):
    try:
        with sqlite3.connect(db_path) as conn:
            #return one row which counts rows in sightings
            return conn.execute("SELECT COUNT(*) FROM sightings").fetchone()[0]
    #will occur if table doesn't exist
    except sqlite3.OperationalError:
        return 0