from typing import Tuple, Any

import joblib
import numpy as np
import pandas as pd
from keras import Sequential
from keras.layers import Dropout, GRU, BatchNormalization, Dense
from sklearn.metrics import *

from src.utils import logger
from src.utils.paths import MODELS_DIR, REPORTS_DIR


def create_time_series(data: pd.DataFrame, window_size: int, target_col_index: int) -> Tuple[np.array, np.array]:
    X, y = [], []
    for i in range(len(data) - window_size - 1):
        X.append(data[i:i+window_size])
        y.append(data[i+window_size, target_col_index])
    return np.array(X), np.array(y)


def create_model(input_shape: Tuple[int, int]) -> Sequential:
    model = Sequential([
        GRU(128, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        GRU(64, return_sequences=True),
        Dropout(0.2),
        GRU(32),
        BatchNormalization(),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def train_model(model: Sequential, X_test: np.array, y_test: np.array, X_train: np.array, y_train: np.array, epochs: int, batch_size: int) -> Tuple[dict, dict]:
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))

    pred_test = model.predict(X_test)
    pred_train = model.predict(X_train)

    train_metrics = {
        'mse': mean_squared_error(y_train, pred_train),
        'mae': mean_absolute_error(y_train, pred_train),
        'evs': explained_variance_score(y_train, pred_train)
    }

    test_metrics = {
        'mse': mean_squared_error(y_test, pred_test),
        'mae': mean_absolute_error(y_test, pred_test),
        'evs': explained_variance_score(y_test, pred_test)
    }

    model.save(f'{MODELS_DIR}/gru_model.keras')

    return train_metrics, test_metrics


def save_metrics(metrics: dict, file_name: str) -> None:
    with open(f'{REPORTS_DIR}/{file_name}', 'w') as f:
        for key, value in metrics.items():
            f.write(f'{key}: {value}\n')


def inverse_transform(prediction: np.array, target_col_index: int) -> np.array:
    scaler = joblib.load(f'{MODELS_DIR}/minmax_scaler.pkl')
    dummy_array = np.zeros((prediction.shape[0], 8))

    dummy_array[:, target_col_index] = prediction.ravel()

    inversed = scaler.inverse_transform(dummy_array)

    return inversed[:, target_col_index]