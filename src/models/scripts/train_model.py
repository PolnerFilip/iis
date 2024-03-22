import pandas as pd

from src.models.model import create_time_series, create_model, train_model, save_metrics
from src.models.preprocessing import preprocess_data, get_target_colum_index, train_test_split, scale_data, load_data
from src.utils import logger
from src.utils.paths import DATA_DIR


def _main():
    logger.log_info('Script train_model.py started')

    # 1. Loads data
    logger.log_info('Loading data')
    df = load_data()

    # 2. Preprocess data
    logger.log_info('Preprocessing data')
    df = preprocess_data(df)
    TARGET_COL_INDEX = get_target_colum_index(df, 'available_bike_stands')

    # 3. Train test split
    train, test = train_test_split(df, test_size=0.2)

    # 4. Scale data
    train, test = scale_data(train, test)

    # 5. Prepare data for time series
    X_train, y_train = create_time_series(train, 48, TARGET_COL_INDEX)
    X_test, y_test = create_time_series(test, 48, TARGET_COL_INDEX)



    # 6. Create model
    logger.log_info('Creating model')
    model = create_model((X_train.shape[1], X_train.shape[2]))

    # 7. Train model
    logger.log_info('Training model')
    train_metrics, test_metrics = train_model(model, X_test, y_test, X_train, y_train, epochs=10, batch_size=32)

    logger.log_info('Model saved')

    # 8. Save metrics
    save_metrics(train_metrics, 'train_metrics.txt')
    save_metrics(test_metrics, 'metrics.txt')


if __name__ == "__main__":
    _main()
