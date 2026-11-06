from datetime import date
from src.Store import search_sightings

print(search_sightings(locationFilter="Manchester", limit="3"))
print("----------------------------")
print(len(search_sightings(startDate=date(2020, 1, 1), endDate=date(2020, 12, 31), limit = 1000)))