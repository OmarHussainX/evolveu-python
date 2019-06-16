import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from sqlalchemy import create_engine
import pandas as pd


app = Flask(__name__)


############################################
#        POSTGRES DATABASE SETUP
############################################

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://postgres:postgres@localhost/sales'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Migrate(app, db)
############################################

# load spreadsheet data into a dictionary of DataFrames
# zeroth column has 'id' for postgres DB
db_data = pd.read_excel('db_data.xls',
                        sheet_name=['customers',
                                    'invoices',
                                    'invoice line items',
                                    'products'],
                        index_col=0,
                        dtype=object)


print(f'\ndb_data["customers"]:\n{db_data["customers"]}')
print(f'\ndb_data["invoices"]:\n{db_data["invoices"]}')
print(f'\ndb_data["invoice line items"]:\n{db_data["invoice line items"]}')
print(f'\ndb_data["products"]:\n{db_data["products"]}')

engine = create_engine(
            'postgresql+psycopg2://postgres:postgres@localhost/sales')

# load DataFrame data into a postgres table
db_data['customers'].to_sql('customers',
                            engine,
                            if_exists='replace')

db_data['invoices'].to_sql('invoices',
                           engine,
                           if_exists='replace')

"""
db_data['invoice line items'].to_sql('invoice line items',
                         engine,
                         if_exists='replace',
                         )

db_data['products'].to_sql('products',
                         engine,
                         if_exists='replace',
                         )
 """

print(f'tables in postgres DB: {engine.table_names()}')
