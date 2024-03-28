from datetime import datetime, date
import os

import pandas as pd
import requests

from src.utils import logger
from src.utils.paths import DATA_DIR


def merge_station_and_weather_data(station_df: pd.DataFrame, weather_df: pd.DataFrame) -> pd.DataFrame:
    station_df['last_update'] = pd.to_datetime(station_df['last_update'])
    weather_df['time'] = pd.to_datetime(weather_df['time'])

    station_df['hour'] = station_df['last_update'].dt.hour
    weather_df['hour'] = weather_df['time'].dt.hour

    merged_df = pd.merge(station_df, weather_df, on='hour')

    merged_df = merged_df.drop(columns=['hour', 'time'])

    return merged_df


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
        weather_df = self.get_weather_data()

        file_path = f'data/processed/stations/station_{self.number}.csv'

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(columns=[
                'number', 'bike_stands', 'available_bike_stands', 'available_bikes', 'last_update', 'fetched_at',
                'temperature_2m', 'apparent_temperature', 'precipitation', 'wind_speed_10m', 'is_day'
            ])

        df_merged = merge_station_and_weather_data(pd.DataFrame([self.__dict__]), weather_df)
        print(df_merged)
        df = pd.concat([df, df_merged], join='inner', ignore_index=True)


        df.to_csv(file_path, index=False)

        logger.log_info(f'Station {self.number} data saved.')

    def get_weather_data(self) -> pd.DataFrame:
        response = requests.get('https://api.open-meteo.com/v1/forecast?'
                                f'latitude={self.lat}'
                                f'&longitude={self.lng}'
                                '&hourly=temperature_2m,apparent_temperature,precipitation,wind_speed_10m,is_day&forecast_days=1')

        data = response.json()

        return pd.DataFrame(data['hourly'])

