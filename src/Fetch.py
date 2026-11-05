#Fetching the API from Elanco website 
import requests

BASE_URL = "https://dev-task.elancoapps.com/data"

def fetch_sightings():
    response = requests.get(f"{BASE_URL}/tick-sightings", timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    data = fetch_sightings()
    print(type(data))
    print(len(data))

    #if the response is a list then only the first two sightings are printed 
    if isinstance(data, list):
        print(data[:2])
    else:
        print(data)