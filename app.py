from os import path, getenv

import boto3
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

LOCAL_BASE_PATH = getenv('BASE_PATH')
REMOTE_TRAINED_PATH = getenv('REMOTE_TRAINED_PATH')
BUCKET_STORAGE = getenv('BUCKET_STORAGE')
LOCAL_PATH = path.join(LOCAL_BASE_PATH,
                          'trained_model.parquet')

@app.route('/_health')
def serverHealth():
    return jsonify('Server is happy :)')



@app.route('/api/v1/featuresClients/<client_id>')
def client_id_search(client_id):
    s3 = boto3.resource('s3')
    s3.Object(BUCKET_STORAGE, REMOTE_TRAINED_PATH).download_file(LOCAL_PATH)
    df = pd.read_parquet(LOCAL_PATH)
    data = df[df.id==client_id]
    return jsonify(data.to_dict('records'))



if __name__ == '__main__':
    app.run(debug=True)