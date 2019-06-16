"""
To create database and create tables with columns & relationships as
defined in python models:

1. in pgAdmin, create 'sales' database
2. in project folder, execute:
export FLASK_APP=app.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade

NOTE: before performing the migration, need to comment out any code which
writes to the database!
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd

app = Flask(__name__)


############################################
#        POSTGRES DATABASE SETUP
############################################

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://postgres:postgres@localhost/sales'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


############################################
#        LOAD SPREADSHEET INTO DATAFRAME
############################################

# Load worksheets into a dictionary of DataFrames
sales_data = pd.read_excel('sales_data.xlsx',
                        #    sheet_name=['customers',
                        #                'invoices',
                        #                'invoice line items',
                        #                'products'],
                           sheet_name=['customers',
                                       'invoices'],
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

sales_data['invoices'] = \
    sales_data['invoices'].rename(index=str,
                                  columns={'Invoice': 'id',
                                           'Date': 'date',
                                           'Customer': 'customer_id'})

for df_key in sales_data:
    sales_data[df_key].dropna(inplace=True)
    print(f'\nsales_data["{df_key}"]:\n{sales_data[df_key]}')
    print(f'\ndata types:\n{sales_data[df_key].dtypes}')


############################################
#        LOAD RECORDS INTO DATABASE
############################################

engine = create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost/sales', echo=True)

# Load DataFrame data into a postgres table
# - do not add the DatFrame index/row numbers as a column
# - set primary key 'id' as Integer to avoid default 'bigint'

""" 
with engine.connect() as con:
    # https://gist.github.com/scaryguy/6269293
    con.execute("ALTER TABLE customers DROP CONSTRAINT customers_pkey;")
    # con.execute('ALTER TABLE customers RENAME COLUMN "Customer" TO "id";')
    con.execute('ALTER TABLE customers ADD PRIMARY KEY (id);')
sqlalchemy.exc.InternalError: (psycopg2.errors.DependentObjectsStillExist) cannot drop constraint customers_pkey on table customers because other objects depend on it
DETAIL:  constraint invoices_customer_id_fkey on table invoices depends on index customers_pkey
HINT:  Use DROP ... CASCADE to drop the dependent objects too.

 """

try:
    sales_data['customers'].to_sql('customers',
                                   engine,
                                   if_exists='append',
                                   index=False,
                                   dtype={'id': db.Integer})
except sqlalchemy.exc.IntegrityError as e:
    print(f'\nIntegrityError: {e}\n')
    pass

with engine.connect() as con:
    max_id = con.execute('SELECT MAX(id) FROM customers;')
    print(f'\nmax_id = {max_id.__dict__}')
    next_val = con.execute("SELECT nextval('customers_id_seq');")
    print(f'next_val = {next_val.__dict__}\n')
    set_val = con.execute("SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers)+1);")
    print(f'set_val = {set_val.__dict__}\n')

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


""" 
sales_data['invoices'].to_sql('invoices',
                              engine,
                              if_exists='append',
                              index=False,
                              dtype={
                                  'id': db.Integer,
                                  'customer_id': db.Integer})

sales_data['invoice line items'].to_sql('invoice line items',
                                        engine,
                                        if_exists='replace',
                                        index=False,
                                        dtype={
                                            'Line': db.Integer,
                                            'Invoice': db.Integer,
                                            'Product': db.Integer,
                                            'Units': db.Integer})

sales_data['products'].to_sql('products',
                              engine,
                              if_exists='replace',
                              index=False,
                              dtype={
                                  'Product': db.Integer,
                                  'Price': db.Integer})

# Set specified columns of DataFrame as primary keys in tables
with engine.connect() as con:
    # https://gist.github.com/scaryguy/6269293
    # con.execute('ALTER TABLE "customers" DROP CONSTRAINT "customers_pkey";')
    con.execute('ALTER TABLE "customers" RENAME COLUMN "Customer" TO "id";')
    con.execute('ALTER TABLE "customers" ADD PRIMARY KEY (id);')
    con.execute('ALTER TABLE "invoices" RENAME COLUMN "Invoice" TO "id";')
    con.execute('ALTER TABLE "invoices" ADD PRIMARY KEY (id);')
    # con.execute('ALTER TABLE "invoices" ADD CONSTRAINT "invoices_fkey" FOREIGN KEY Customer REFERENCES Customers(id);')
    con.execute('ALTER TABLE "invoice line items" RENAME COLUMN "Line" TO "id";')
    con.execute('ALTER TABLE "invoice line items" ADD PRIMARY KEY (id);')
    con.execute('ALTER TABLE "products" RENAME COLUMN "Product" TO "id";')
    con.execute('ALTER TABLE "products" ADD PRIMARY KEY (id);')
 """

print(f'\ntables in postgres DB: {engine.table_names()}')
