#Cleaning the data received from API
import pandas as pd

def clean(df):
    df = df.copy()
    columns = ["id", "date", "location", "species", "latinName"]
    for column in columns:
        #removing white space from all cells
        df[column] = df[column].str.strip()
    
    #empty string cells replaced NaN cells
    df[columns] = df[columns].replace("", pd.NA)

    #normalising string cells with qualitative attributes
    df["location"] = df["location"].str.title()
    df["species"] = df["species"].str.capitalize()
    df["latinName"] = df["latinName"].str.capitalize()

    #parsing dates, any unparsable cell becomes NaN
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    #dropping rows that have NaN cell/s of important subsets
    df = df.dropna(subset=["id", "date", "location"])

    #removing duplicates based on everything except for ID
    df = df.drop_duplicates(subset=["date", "location", "species", "latinName"])

    return df
