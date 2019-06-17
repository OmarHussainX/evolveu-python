"""
To create database and create tables with columns & relationships as
defined in python models:

1. in pgAdmin, create 'sales' database
2. in project folder, execute:
export FLASK_APP=app.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade

NOTE: Before performing the migration, need to comment out any code which
writes to the database!
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import pandas as pd

app = Flask(__name__)


"""
-----------------------------------------------------------
    POSTGRES DATABASE SETUP
-----------------------------------------------------------
"""
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://postgres:postgres@localhost/sales'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


"""
-----------------------------------------------------------
    LOAD SPREADSHEET INTO DATAFRAME
-----------------------------------------------------------
"""
# Load worksheets into a dictionary of DataFrames
sales_data = pd.read_excel('sales_data.xlsx',
                           sheet_name=['customers',
                                       'products',
                                       'invoices',
                                       'invoice line items'],
                           dtype={
                               'Customer': db.Integer,
                               'Invoice': db.Integer,
                               'Line': db.Integer,
                               'Product': db.Integer,
                               'Units': db.Integer,
                           })


# rename DataFrame columns to match DB table fields
sales_data['customers'] = \
    sales_data['customers'].rename(index=str,
                                   columns={'Customer': 'id',
                                            'First': 'first_name',
                                            'Last': 'last_name'})
sales_data['products'] = \
    sales_data['products'].rename(index=str,
                                  columns={'Product': 'id',
                                           'Name': 'name',
                                           'Price': 'price'})
sales_data['invoices'] = \
    sales_data['invoices'].rename(index=str,
                                  columns={'Invoice': 'id',
                                           'Date': 'date',
                                           'Customer': 'customer_id'})
sales_data['invoice line items'] = \
    sales_data['invoice line items'].rename(index=str,
                                            columns={'Line': 'id',
                                                     'Units': 'units',
                                                     'Invoice': 'invoice_id',
                                                     'Product': 'product_id'})

for df_key in sales_data:
    sales_data[df_key].dropna(inplace=True)
    print(f'\nsales_data["{df_key}"]:\n{sales_data[df_key]}')
    print(f'\ndata types:\n{sales_data[df_key].dtypes}')


"""
-----------------------------------------------------------
    LOAD RECORDS INTO DATABASE
-----------------------------------------------------------
"""
engine = create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost/sales', echo=True)

# Load each DataFrame data into a postgres table
# - do not add the DatFrame index/row numbers as a column
# - set certain columns as Integer to avoid default 'bigint'
try:
    sales_data['customers'].to_sql('customers',
                                   engine,
                                   if_exists='append',
                                   index=False,
                                   dtype={'id': db.Integer})
except IntegrityError as e:
    print(f'\nIntegrityError: {e}\n')
    pass

try:
    sales_data['products'].to_sql('products',
                                  engine,
                                  if_exists='append',
                                  index=False,
                                  dtype={
                                      'id': db.Integer,
                                      'price': db.Integer})
except IntegrityError as e:
    print(f'\nIntegrityError: {e}\n')
    pass

try:
    sales_data['invoices'].to_sql('invoices',
                                  engine,
                                  if_exists='append',
                                  index=False,
                                  dtype={
                                      'id': db.Integer,
                                      'date': db.Date,
                                      'customer_id': db.Integer})
except IntegrityError as e:
    print(f'\nIntegrityError: {e}\n')
    pass

try:
    sales_data['invoice line items'].to_sql('line_items',
                                            engine,
                                            if_exists='append',
                                            index=False,
                                            dtype={
                                                'id': db.Integer,
                                                'units': db.Integer,
                                                'invoice_id': db.Integer,
                                                'product_id': db.Integer})
except IntegrityError as e:
    print(f'\nIntegrityError: {e}\n')
    pass


"""
-----------------------------------------------------------
    Set primary key sequence to next highest value
-----------------------------------------------------------
"""
with engine.connect() as con:
    set_val = con.execute
    ("SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers)+1);")
    # print(f'set_val = {set_val.__dict__}\n')
    con.execute
    ("SELECT setval('products_id_seq', (SELECT MAX(id) FROM products)+1);")
    con.execute
    ("SELECT setval('invoices_id_seq', (SELECT MAX(id) FROM invoices)+1);")
    con.execute
    ("SELECT setval('line_items_id_seq', (SELECT MAX(id) FROM line_items)+1);")

# https://hcmc.uvic.ca/blogs/index.php/how_to_fix_postgresql_error_duplicate_ke?blog=22
# Primary key sequence out of sync due to import process ('id' values in
# spreadsheet often do not start from 1, and also skip some interim values)
# Have to manually reset the primary key index to the next largest 'id'
# value avaialable
#
# a. Check the highest id:
# SELECT MAX(id) FROM customers
#
# b. Check what the next id in sequence is (probably '1'):
# SELECT nextval('customers_id_seq')
#
# c. If the result of a is greater than b, then set set the sequence to
# the next available value that's higher than any existing primary key
# in the sequence
# SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers)+1);


print(f'\ntables in postgres DB: {engine.table_names()}')
