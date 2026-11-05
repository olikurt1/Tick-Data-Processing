#Fetching the API from Elanco website 
import requests
import time

BASE_URL = "https://dev-task.elancoapps.com/data"

def fetch_with_retry(url, max_retries=5):
    for attempt in range(max_retries):
        #exponential backoff in case of rate limit or server error
        wait = 2 ** attempt

        #tries GET for passed url, attempt fails if timed out or connection error
        try:
            response = requests.get(url, timeout=10)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            print(f"Attempt {attempt + 1}: {type(e).__name__}, retrying in {wait}s.")
            time.sleep(wait)
            continue
        
        if response.status_code == 200:
            return response.json()

        if response.status_code == 429 or response.status_code >= 500:
            print(f"Attempt {attempt + 1}: status {response.status_code}, retrying in {wait}s.")
            time.sleep(wait)
            continue

        #handles other errors that retries won't help with
        response.raise_for_status()
    
    #if all retries fail raise error         
    raise RuntimeError(f"Failed to fetch {url} after {max_retries} attempts.")


def fetch_sightings():
    data = fetch_with_retry(f"{BASE_URL}/tick-sightings")
    if not isinstance(data, list):
        raise ValueError(f"Expected a list, got {type(data).__name__}.")
    return data

#checks that program is being directly executed 
if __name__ == "__main__":
    data = fetch_sightings()

    #if the response is a list then only the first two sightings are printed 
    if isinstance(data, list):
        print(data[:2])
    else:
        print(data)