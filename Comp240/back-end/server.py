from flask import Flask

app = Flask(__name__)
# Configure a secret SECRET_KEY
# Will learn a better way to do this...
app.config['SECRET_KEY'] = 'mysecretkey'


@app.route('/', methods=['GET'])
def index():
    return '<h1>Comp240 flask server...</h1>'


if __name__ == '__main__':
    app.run(debug=True)