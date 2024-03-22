from flask import Flask
from src.serve.routes.predict import predict_blueprint

app = Flask(__name__)

app.register_blueprint(predict_blueprint, url_prefix='/mbajk')

if __name__ == '__main__':
    app.run(port=5001)
