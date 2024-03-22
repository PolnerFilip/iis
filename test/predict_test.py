import unittest
from flask import Flask, Request
from src.serve.routes import predict
from src.utils.paths import OTHER_DIR


class TestPredict(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(predict.predict_blueprint)
        self.client = self.app.test_client()

    def test_predict_success(self):
        response = self.client.post('/predict', data={'file': (open(f'../other/predict_test.csv', 'rb'), 'test.csv')})
        self.assertEqual(response.status_code, 200)

    def test_predict_no_file_part(self):
        response = self.client.post('/predict', data={})
        self.assertEqual(response.status_code, 400)

    def test_predict_no_file(self):
        response = self.client.post('/predict', data={'file': ''})
        self.assertEqual(response.status_code, 400)
