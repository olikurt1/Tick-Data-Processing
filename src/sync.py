#Centralised program that runs Fetch, Clean, Store
import sqlite3
from src.Fetch import fetch_sightings
from src.Clean import clean
from src.Store import init_db, save_sightings

init_db()

records = fetch_sightings()
cleaned_records = clean(records)

save_sightings(cleaned_records)

#checking row count of database to confirm all data is there
with sqlite3.connect("ticks.db") as conn:
    print(conn.execute("SELECT COUNT(*) FROM sightings").fetchone())