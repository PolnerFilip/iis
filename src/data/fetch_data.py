import json

import requests
import pandas as pd
import time
import schedule
from datetime import datetime


def fetch_and_process_data():
    response = requests.get(
        'https://api.jcdecaux.com/vls/v1/stations?contract=maribor&apiKey=5e150537116dbc1786ce5bec6975a8603286526b')
    data = response.json()

    with open('../../data/raw/raw_data.json', 'w') as f:
        json.dump(data, f)

    df = pd.DataFrame(data)

    df['last_update'] = pd.to_datetime(df['last_update'], unit='ms')

    df.to_csv('../../data/raw/test.csv')


# Runs the function when script starts
fetch_and_process_data()

# Runs the function every hour
schedule.every().hour.do(fetch_and_process_data)

# Keeps the script running
while True:
    schedule.run_pending()
    time.sleep(1)