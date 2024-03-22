from flask import Blueprint, request, jsonify, Request
from keras.models import load_model
from src.models.model import create_time_series, inverse_transform
from src.models.preprocessing import get_target_colum_index, scale_data, preprocess_data
import numpy as np
import pandas as pd

from src.utils.paths import MODELS_DIR

# Load the trained model
model = load_model(f'{MODELS_DIR}/gru_model.keras')

# Define the blueprint
predict_blueprint = Blueprint('predict', __name__)


def read_file_and_convert_to_df(req: Request) -> pd.DataFrame:
    if 'file' not in request.files:
        raise Exception('No file part in the request')

    file = request.files['file']

    if file.filename == '':
        raise Exception('No file part in the request')

    if file and file.filename.endswith('.csv'):
        return pd.read_csv(file)


@predict_blueprint.route('/predict', methods=['POST'])
def predict():
    try:
        df = read_file_and_convert_to_df(request)
    except Exception as e:
        return str(e), 400

    df = preprocess_data(df)
    print(df)
    TARGET_COL_INDEX = get_target_colum_index(df, 'available_bike_stands')

    df, _ = scale_data(df, df)

    X, _ = create_time_series(df, 48, TARGET_COL_INDEX)

    prediction = model.predict(X)

    final_prediction = inverse_transform(prediction, TARGET_COL_INDEX)
    return jsonify({"prediction": round(final_prediction.tolist()[0])}), 200


