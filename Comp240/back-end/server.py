import os
import json
import pandas
from flask import Flask, jsonify

app = Flask(__name__)
# Configure a secret SECRET_KEY
# When will we learn a better way to do this...?
app.config['SECRET_KEY'] = 'mysecretkey'


@app.route('/', methods=['GET'])
def index():
    return '<h1>Comp240 flask server...</h1>'


@app.route('/datadump', methods=['GET'])
def data_dump():
    # load 'customers' worksheet into a DataFrame object, and
    # drop empty rows
    df = pandas.read_excel('./sales_data.xlsx', sheet_name='customers')
    df.dropna(inplace=True)
    print(f'DataFrame (type: {type(df)}) generated from spreadsheet:\n{df}')

    # convert pandas DataFrame to JSON
    resp_data = df.to_json(orient='records')

    print(f'DataFrame data (type: {type(resp_data)}) after conversion to JSON string:\n{resp_data}')
    
    # this returns a JSON string, but Content-Type in response headers
    # is text/html instead of application/json
    return resp_data

    # trying to formaat JSON properly...
    # this didn't work
    # alt_resp_data = json.dumps(resp_data)
    # # resp_data = df.to_json(orient='records', lines=True)
    # print(f'DataFrame data (type: {type(alt_resp_data)}) after json.dumps():\n{alt_resp_data}')

    # create a Flask Response object
    resp = jsonify(resp_data)

    print(f'--> \'200 OK\' Response object (containing JSON string), sent from\
\'/datadump()\' route:\n\
resp:\n{resp}\n\
type of resp: {type(resp)}\n\
resp.response:\n{resp.response}\n\
type of resp.response : {type(resp.response )}\n')
    return resp, 200


if __name__ == '__main__':
    app.run(debug=True)
