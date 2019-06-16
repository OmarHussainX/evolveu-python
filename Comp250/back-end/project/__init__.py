import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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


# Load spreadsheet data into a dictionary of DataFrames
# zeroth column has 'id' for postgres DB
sales_data = pd.read_excel('sales_data.xls',
                           sheet_name=['customers',
                                       'invoices',
                                       'invoice line items',
                                       'products'],
                           index_col=0,
                           dtype=object)


print(f'\nsales_data["customers"]:\n{sales_data["customers"]}')
print(f'\nsales_data["invoices"]:\n{sales_data["invoices"]}')
print(
    f'\nsales_data["invoice line items"]:\n{sales_data["invoice line items"]}')
print(f'\nsales_data["products"]:\n{sales_data["products"]}')

engine = create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost/sales')

# load DataFrame data into a postgres table
sales_data['customers'].to_sql('customers',
                               engine,
                               if_exists='replace')

sales_data['invoices'].to_sql('invoices',
                              engine,
                              if_exists='replace')

"""
sales_data['invoice line items'].to_sql('invoice line items',
                         engine,
                         if_exists='replace',
                         )

sales_data['products'].to_sql('products',
                         engine,
                         if_exists='replace',
                         )
 """

print(f'tables in postgres DB: {engine.table_names()}')
