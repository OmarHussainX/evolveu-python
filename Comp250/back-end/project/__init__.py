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


############################################
#        LOAD RECORDS INTO DATABASE
############################################

# Load spreadsheet data into a dictionary of DataFrames
sales_data = pd.read_excel('sales_data.xlsx',
                           sheet_name=['customers',
                                       'invoices',
                                       'invoice line items',
                                       'products'],
                           dtype={
                               'Customer': db.Integer,
                               'Invoice': db.Integer,
                               'Line': db.Integer,
                               'Product': db.Integer,
                               'Units': db.Integer,
                           })

for key in sales_data:
    sales_data[key].dropna(inplace=True)
    print(f'\nsales_data["{key}"]:\n{sales_data[key]}')
    print(f'\ndata types:\n{sales_data[key].dtypes}')

engine = create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost/sales')

# Load DataFrame data into a postgres table
# - do not add the DatFrame index/row numbers as a column
# - set primary key 'id' as Integer to avoid default 'bigint'
sales_data['customers'].to_sql('customers',
                               engine,
                               if_exists='replace',
                               index=False,
                               dtype={'Customer': db.Integer})

sales_data['invoices'].to_sql('invoices',
                              engine,
                              if_exists='replace',
                              index=False,
                              dtype={
                                  'Invoice': db.Integer,
                                  'Customer': db.Integer})

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


print(f'\ntables in postgres DB: {engine.table_names()}')
