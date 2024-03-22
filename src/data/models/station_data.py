from datetime import datetime
import os

import pandas as pd

from src.utils import logger
from src.utils.paths import DATA_DIR


class StationData:
    number: int
    contract_name: str
    name: str
    address: str
    lat: float
    lng: float
    banking: bool
    bonus: bool
    bike_stands: int
    available_bike_stands: int
    available_bikes: int
    status: str
    last_update: datetime
    fetched_at: datetime

    def __init__(self, number, contract_name, name, address, position, banking, bonus, bike_stands,
                 available_bike_stands, available_bikes, status, last_update):
        self.number = number
        self.contract_name = contract_name
        self.name = name
        self.address = address
        self.lat = position['lat']
        self.lng = position['lng']
        self.banking = banking
        self.bonus = bonus
        self.bike_stands = bike_stands
        self.available_bike_stands = available_bike_stands
        self.available_bikes = available_bikes
        self.status = status
        self.last_update = datetime.fromtimestamp(last_update / 1000)
        self.fetched_at = datetime.now()

    def save_station_data(self) -> None:
        file_path = f'{DATA_DIR}/processed/stations/station_{self.number}.csv'

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(columns=[
                'number', 'bike_stands', 'available_bike_stands', 'available_bikes', 'last_update', 'fetched_at'
            ])

        df = pd.concat([df, pd.DataFrame([self.__dict__])], join='inner', ignore_index=True)
        df.to_csv(file_path, index=False)

        logger.log_info(f'Station {self.number} data saved.')
