import pandas
from flask import Flask, render_template

app = Flask(__name__)
# Configure a secret SECRET_KEY
# When will we learn a better way to do this...?
app.config['SECRET_KEY'] = 'mysecretkey'


@app.route('/', methods=['GET'])
def index():
    return f'<h1>Comp240 Flask server</h1>\n\
<h3>route <code>\'/datadump\'</code> for raw dump of JSON data</h3>\n\
<h3>route <code>\'/viewdata\'</code> for Jinja2 template rendering of JSON data</h3>'


@app.route('/datadump', methods=['GET'])
def data_dump():
    # load 'customers' worksheet into a DataFrame object,
    # preserving data as stored in Excel - i.e. no interpretation of the types
    # of data in the columns
    #
    # https://www.marsja.se/pandas-excel-tutorial-how-to-read-and-write-excel-files/#Setting_the_Data_type_for_data_or_columns
    # (unable to get dtype={'Customer': 'int'} working...)
    df = pandas.read_excel('./sales_data.xlsx',
                           sheet_name='customers',
                           dtype=object)

    print('printing df.info()...')
    df.info()

    # drop empty rows
    df.dropna(inplace=True)

    print(f'\nDataFrame (type: {type(df)}) generated from spreadsheet:\n{df}')

    # convert pandas DataFrame to JSON string
    resp_data = df.to_json(orient='records')

    print(f'\nDataFrame data (type: {type(resp_data)}) after conversion to JSON \
string:\n{resp_data}')

    # NOTE: no need to create a Flask Response object via jsonify():
    #   resp = jsonify(resp_data)
    #   return resp, 200
    # jsonify() serializes data passed to it, and the response data has already
    # been serialized (converted) into a JSON string in this case

    # create Flask Response object
    resp = app.response_class(response=resp_data,
                              status=200,
                              mimetype='application/json')

    print(f'\n--> \'200 OK\' Response object (containing JSON string data), sent from\
\'/datadump()\' route:\n\
resp: {resp}\n\
type of resp: {type(resp)}\n\
resp.response:\n{resp.response}\n\
type of resp.response : {type(resp.response )}\n')

    return resp


@app.route('/viewdata', methods=['GET'])
def view_data():
    df = pandas.read_excel('./sales_data.xlsx',
                           sheet_name='customers',
                           dtype=object)
    df.dropna(inplace=True)
    # by default, 'to_dict()' will create a dictionary where the keys are
    # column headings, and the values are a dictionary of all the values
    # in a column, with row index as key
    col_dic_data = df.to_dict()

    # https://stackoverflow.com/a/26716774/11245656
    # set 'Customer' column as index so that the values from this column are
    # the dictionary's keys, then transpose the DataFrame.
    # For the dictionary's values, specify that a 'list' is to be returned for
    # each column - otherwise by default a dictionary of key:value pairs will
    # be returned
    data = df.set_index('Customer').T.to_dict('list')

    return render_template('viewdata.html',
                           col_dic_data=col_dic_data,
                           data=data)


if __name__ == '__main__':
    app.run(debug=True)
