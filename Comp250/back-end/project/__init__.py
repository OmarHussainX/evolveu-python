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
sales_data = pd.read_excel('sales_data.xlsx',
                           sheet_name=['customers',
                                       'invoices',
                                       'invoice line items',
                                       'products'],
                           skip_blank_lines=True,
                           index_col=0)

for key in sales_data:
    sales_data[key].dropna(inplace=True)
    print(f'\nsales_data["{key}"]:\n{sales_data[key]}')

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
