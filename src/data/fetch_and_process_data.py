import json
from datetime import datetime

import requests

from src.data.models.data_collector import DataCollector
from src.utils import logger
from dotenv import load_dotenv
import os

from src.utils.paths import DATA_DIR

load_dotenv()
API_KEY = os.getenv('API_KEY')


def fetch_and_process_data() -> None:
    logger.log_info('Fetching data from API...')
    try:
        response = requests.get(f'https://api.jcdecaux.com/vls/v1/stations?contract=maribor&apiKey={API_KEY}')
        data = response.json()

        data_collector = DataCollector(data)
        data_collector.save_snapshot()
        data_collector.save_stations()

        save_json(data)
    except requests.exceptions.RequestException as e:
        logger.log_error(f'Error fetching data: {e}')


def save_json(data: dict) -> None:
    file_path = f'{DATA_DIR}/raw/raw_data.json'

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            json_data = json.load(f)
    else:
        json_data = []

    json_data.append({
        "fetched_at": datetime.now().isoformat(),
        "data": data
    })

    with open(file_path, 'w') as f:
        json.dump(json_data, f, indent=4)

    logger.log_info('json file updated')


if __name__ == "__main__":
    fetch_and_process_data()
