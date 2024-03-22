import time

import schedule

from src.data.fetch_and_process_data import fetch_and_process_data

# Runs the function when script starts
fetch_and_process_data()

# Runs the function every hour
schedule.every(1).hour.do(fetch_and_process_data)

# Keeps the script running
while True:
    schedule.run_pending()
    time.sleep(1)
