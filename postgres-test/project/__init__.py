import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd

app = Flask(__name__)

# CSRF Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'


############################################
#        SQL DATABASE AND MODELS
############################################

# http://www.jan-langfellner.de/storing-a-pandas-dataframe-in-a-postgresql-database/
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://postgres:postgres@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


# load spreadsheet data into a dictionary of DataFrames
db_data = pd.read_excel('db_data.xls',
                        sheet_name=['puppies', 'owners'],
                        # index_col=0,
                        dtype=object)

print(f'\ndb_data:\n{db_data}')

print(f'\ndb_data["puppies"]:\n{db_data["puppies"]}')
print(f'\ndb_data["owners"]:\n{db_data["owners"]}')
