#Cleaning the data received from API
from src.Fetch import fetch_sightings
import pandas as pd


df = pd.DataFrame(fetch_sightings())

print(df.head())
print(df.tail())

#checking for duplicates based on same ID
print(f"Duplicated ID's: {df.duplicated(subset="id").sum()}.")

#checking for duplicated sightings with different ID's
print(f"Duplicate sightings with different ID: {df.drop(columns="id").duplicated().sum()}")
