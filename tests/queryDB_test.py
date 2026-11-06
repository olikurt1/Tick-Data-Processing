from datetime import date
from src.Store import search_sightings, get_sightings, count_by_period, count_by_region

print(search_sightings(locationFilter="Manchester", limit="3"))
print("----------------------------")
print(len(search_sightings(startDate=date(2020, 1, 1), endDate=date(2020, 12, 31), limit = 1000)))
print("----------------------------")
print(get_sightings("9WB23vVRf7JDX7dPijds"))
print("----------------------------")
print(count_by_region())
print("----------------------------")
print(count_by_period("month"))