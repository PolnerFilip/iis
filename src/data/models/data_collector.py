import os
from datetime import datetime
from typing import Final
import threading

import pandas as pd

from src.data.models.station_data import StationData
from src.utils import logger
from src.utils.paths import DATA_DIR


class DataCollector:
    fetched_at: datetime
    station_data: list[StationData]
    raw_data: list[dict]

    file_path_raw: Final[str] = f'{DATA_DIR}/raw/station_data.csv'
    file_path_processed: Final[str] = f'{DATA_DIR}/processed/station_data.csv'

    def __init__(self, data: list[dict]):
        self.fetched_at = datetime.now()
        self.station_data = [StationData(**station) for station in data]
        self.raw_data = data

    def save_snapshot(self) -> None:
        df_raw = pd.DataFrame(self.raw_data)
        df_raw['fetched_at'] = self.fetched_at.isoformat()
        df_processed = df_raw.copy(deep=True)
        df_processed.drop(
            columns=['contract_name', 'name', 'address', 'position', 'banking', 'bonus', 'status'],
            inplace=True)

        if os.path.exists(self.file_path_raw):
            df = pd.read_csv(self.file_path_raw)
        else:
            df = pd.DataFrame(columns=df_raw.columns)
        df = pd.concat([df, df_raw], ignore_index=True)
        df.to_csv(self.file_path_raw, index=False)

        if os.path.exists(self.file_path_processed):
            df = pd.read_csv(self.file_path_processed)
        else:
            df = pd.DataFrame(columns=df_processed.columns)
        df_processed['last_update'] = df_processed['last_update'].apply(lambda x: datetime.fromtimestamp(x / 1000))
        df = pd.concat([df, df_processed], ignore_index=True)
        df.to_csv(self.file_path_processed, index=False)

        logger.log_info('Data snapshot saved.')
        pass

    def save_stations(self) -> None:
        for station in self.station_data:
            thread = threading.Thread(target=station.save_station_data)
            thread.start()