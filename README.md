# Tick-Data-Processing

## Overview

This program is a Flask API backend which provides endpoints for querying tick sightings pulled from the Elanco public API. The data is fetched using requests, cleaned using pandas and stored in an sqlite3 database. The program includes testing for Clean and Fetch to showcase in the event that an error does need handling, the error handlers do work.

## How to run

To run the program:
- Clone the repository
- Create a virtual environment and run pip install -r requirements.txt, this will install all the dependencies required for running the program
- run python -m src.sync from the root of the folder, this will run the core programs
- run flask --app src.app run. This will run the API server that receieves requests for endpoints in app.py.

## Endpoints

| Method | Path | Parameters | Example |
|--------|------|------------|---------|
| GET | '/sightings' | 'start', 'end', 'location', 'species', 'limit', 'offset' | '/sightings?location=leeds&limit=20 |
| GET | 'sightings/<sighting_id> | None | 'sightings/idxxxxxxx |
| GET | '/stats/by-region' | None | '/stats/by-region' |
| GET | 'stats/by-period' | 'period' ('month' or 'week') | '/stats/by-period?period=week' |
| GET | '/health' | None | '/health' | 

## Design

The design behind this backend is that each section of the data pipeline is its own module. Each section is independent of other sections. This enforces separation of concerns. If one part of the pipeline breaks, other parts aren't affected. It also means that each part can be tested individually. Fetch.py is responsible for calling Elanco's API and returning the JSON body through fetch_sightings(). 

Clean.py is responsible for cleaning the data provided by fetch_sightings(). It converts the list of dictionaries (JSON body) cleanly into a DataFrame. Pandas is used for this.  

Store.py is responsible for ingesting the DateFrame which clean() returns. It creates an SQLite3 database (ticks.db) which is always generated/regenerated (upserted). The structure is created and the data is inserted into the database also, through save_sightings().  

Store.py also includes all the functions responsible for querying the database and returning values that the endpoints in app.py are to respond with. 

sync.py is responsible for orchestrating the data pipeline. It runs every single function relevant to receiving, cleaning and storing the Elanco API data. sync.py initialises the database, runs the API client, calls clean() on the body received through the API client and finally runs save_sightings() from Store.py which stores the cleaned data into tick.db. 

I chose to store the entire Elanco tick dataset into a database once rather than constantly calling the API because in the event that the Elanco service was to go down, my program would still have the dataset stored. app.py would still be able to fulfill requests. The only shortfall of this decision is that if the Elanco dataset is updated, my database won't reflect this so the program will be working on older data. This can be resolved by re running sync.py but knowing when to run sync.py is the issue. 

I chose to use Python because I'm most familiar with this language. It also includes many well established libraries that enable fast development speed on a deadline. I decided to use Flask as I had played around with it before so had some familiarity with how it worked. Along with this Pandas provides strong data cleaning tools. Furthermore, using Python has provided room to grow in terms of implementing AI/ML insights through libraries such as scikit-learn.

app.py is the Flask API server responsible for serving requests made to endpoints that query the database with specificity. This file includes all the endpoints that query the database and the endpoint for checking the database health. 

## Data Handling

The API client includes fetch_with_retry(). This means that the Elanco API will be called until a successful response is received or until the assigned maximum amount of retries has occurred. The client retries if there is a status code 429/5xx with exponential back off to respect rate limits. 

Within Clean.py Clean() first strips whitespace from all cells in every column, then any cells that are empty are converted into NaN cells. Descriptive cells like location, species and latinName are all normalised to have capitalisation. Date cells are parsed into datetime data type and if not they become NaN. Also, rows that have NaN cells of and/or id, date and location are dropped because there are core value that every sighting must have. Finally, duplicates are dropped based on everything except for ID because if there are more than one row with these values matching, then it means the same sighting was recorded twice under different ID's or a very big coincidence. There are no duplicates currently but de-duplicating is added in the scenario that they do appear

Furthermore, I use INSERT OR REPLACE when inserting data into the database. This ensures that everytime the tick_sightings get stored into the database, the data isn't duplicated and instead updated. Since id is a primary key, it must be unique, therefore INSERT OR REPLACE respects this, so rows with existing ID's are updated or left along and any rows with new ID's are new so are added to the database. This prevents the database from having 1000 rows from the first insertion and another 1000 rows where the updated rows are added along with the first 1000 rows. Primary Keys wouldn't allow this anyway but it would raise an error so upserting avoids the error. 

## Error Handling

The API client handles error gracefully during API call tries and after. Relevant exceptions are first raised if a response cannot be received. An exception for request timing out or lack of connection to server. If a bad status code is received then a relevant message is provided before a retry occurs. If maximum retries have been reached, RunTimeError is raised gracefully with an error message and the program exits. Fetch_sightings() also handles errors by checking that the response body is a list and raises a ValueError if not.

The Flask server app.py includes two custom functions; parse_date_parameter() and parse_int_parameter(). The first function parses a date filter into ISO format and if it fails, ValueError is raised because it means the request url had an invalid date format and 400 status code is the response. Parse_int_parameter() takes limit and offset and ensures these are valid integers and not abc etc since the url could include this initially. The function tries casting the passed value to an integer, if it fails, ValueError is raised and the response is a 400 status code. Each endpoint also includes graceful error handling. Getting a sighting by ID first the function checks if sightings actually exists. If it doesn't 404 is raised with relevant message. List_sightings(), used for finding sightings with filters ensures that start date isn't later than end date otherwise 404 is raised with valid message. Other endpoints also handle errors by aborting with relevant status code and message.

To handle these errors, app.py includes errorhandler routes over the functions used when aborting an endpoint.

Within Store.py, value_to_db() is required for the attributes it is applied to because said attributes didn't affect the rows being dropped for being NaN. Therefore, NaN cells for the attributes using value_to_db() were passed into Store.py, value_to_db ensures that before they are inserted into tick.db, it is converted into 'None' or the value is just returned. This ensures that tick.db treats the cell as NULL. 

## Future Versions

- Scheduled sychronisation: Run sync.py automatically at set intervals. 
- Containerising with Docker
- Deploy to a public URL

## Walkthrough

[Walkthrough](https://youtu.be/GY-o8DDqKg8)