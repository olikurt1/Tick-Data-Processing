from src.Clean import clean
import pandas as pd

messy = [
    {"id": "1", "date": "2022-08-01T06:40:31", "location": " leeds ", "species": "marsh tick", "latinName": "ixodes apronophorus"},
    {"id": "2", "date": "2022-08-01T06:40:31", "location": "Leeds", "species": "Marsh tick", "latinName": "Ixodes apronophorus"},
    {"id": "3", "date": "not a date", "location": "London", "species": "Sheep tick", "latinName": "Ixodes ricinus"},
    {"id": "4", "date": "2022-08-02T10:00:00", "location": "   ", "species": "Sheep tick", "latinName": "Ixodes ricinus"},
]

df = pd.DataFrame(messy)

print(f"Length before cleaning: {len(df)}")
records = clean(df)
print(f"Length after cleaning: {len(records)}")