from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.utils.paths import MODELS_DIR, DATA_DIR


def load_data() -> pd.DataFrame:
    return pd.read_csv(f'{DATA_DIR}/train.csv', index_col=0)


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(columns=['bike_stands', 'date'], inplace=True)
    df.fillna(df.mean(), inplace=True)

    return df


def get_target_colum_index(df: pd.DataFrame, target_column: str) -> int:
    return df.columns.get_loc(target_column)


def train_test_split(df: pd.DataFrame, test_size: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
    test_size = int(len(df) * test_size)
    return df.iloc[:-test_size], df.iloc[-test_size:]


def scale_data(train: pd.DataFrame, test: pd.DataFrame) -> Tuple[np.array, np.array]:
    try:
        scaler = joblib.load(f'{MODELS_DIR}/minmax_scaler.pkl')
    except FileNotFoundError:
        scaler = MinMaxScaler()
    train = scaler.fit_transform(train)
    test = scaler.transform(test)

    joblib.dump(scaler, f'{MODELS_DIR}/minmax_scaler.pkl')

    return train, test
