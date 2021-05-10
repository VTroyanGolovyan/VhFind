from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
# Allow cross domain
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


@app.route('/')
def empty_request():
    return json.dumps(
        {
            'status': 200,
            'data': 'REST API IS WORKING'
        }
    )


@app.route('/find', methods=['POST', 'OPTIONS'])
def find():
    return json.dumps(
        {
            'status': 200,
            'data': ''
        }
    )


@app.route('<access_token>/find', methods=['POST', 'OPTIONS'])
def find(access_token):
    return json.dumps(
        {
            'status': 200,
            'data': ''
        }
    )


@app.route('/sign/in', methods=['POST', 'OPTIONS'])
def sign_in():
    return json.dumps(
        {
            'status': 200,
            'data': ''
        }
    )


@app.route('/sign/up', methods=['POST', 'OPTIONS'])
def sign_up():
    form_data = json.loads(request.data.decode('utf-8'))
    return json.dumps(
        {
            'status': 200,
            'data': ''
        }
    )


@app.route('<access_token>/sign/out', methods=['POST', 'OPTIONS'])
def sign_out(access_token):
    return json.dumps(
        {
            'status': 200,
            'data': ''
        }
    )


@app.route('<access_token>/history', methods=['GET', 'OPTIONS'])
def history(access_token):
    return json.dumps(
        {
            'status': 200,
            'data': ''
        }
    )


if __name__ == '__main__':
    app.run()
