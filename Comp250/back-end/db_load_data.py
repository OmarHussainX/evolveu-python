from project import app, db
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import pandas as pd


"""
-----------------------------------------------------------
    LOAD SPREADSHEET INTO DATAFRAME
-----------------------------------------------------------
"""
# Load worksheets into a dictionary of DataFrames
# (set certain columns as int to prevent them being treated as float)
sales_data = pd.read_excel('sales_data.xlsx',
                           sheet_name=['customers',
                                       'products',
                                       'invoices',
                                       'invoice line items'],
                           dtype={
                               'Customer': db.Integer,
                               'Product': db.Integer,
                               'Units': db.Integer,
                               'Invoice': db.Integer,
                               'Line': db.Integer
                           })

# Rename DataFrames' columns to match database's tables' fields
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

# Drop empty rows from the DataFrames
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
    'postgresql+psycopg2://postgres:postgres@localhost/sales')

# Load each DataFrame's data into a postgres table
# - do not add the DataFrame index/row numbers as a column
# - set certain columns as Integer to prevent them being set to 'bigint'
#
# NOTE: For some reason, every conversion from DataFrame to SQL table
# results in an error for the first key in each table:
#
# IntegrityError: ...duplicate key value violates unique constraint...
# ...DETAIL:  Key (id)=(...) already exists.
#
# NOTE: The IntegrityError went away when this script (to load records into
# the database from a spreadsheet) was broken out & separated from
# 'project/__init__.py' )
try:
    sales_data['customers'].to_sql('customers',
                                   engine,
                                   if_exists='append',
                                   index=False,
                                   dtype={'id': db.Integer})
except IntegrityError as e:
    print(f'\nIntegrityError: {e}\n')

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

"""
-----------------------------------------------------------
    Set primary key sequence to next highest value
-----------------------------------------------------------
"""
# https://hcmc.uvic.ca/blogs/index.php/how_to_fix_postgresql_error_duplicate_ke?blog=22
# Primary key sequence out of sync due to import process ('id' values in
# spreadsheet often do not start from 1, and skip some interim values).
# Have to manually reset the primary key index to the next largest 'id'
# value available
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
#
# NOTE: There is no need to add '+1' to the sequence - setval defaults to
# incrementing the sequence by 1 before generating the next value
# https://www.postgresql.org/docs/current/functions-sequence.html
with engine.connect() as con:
    con.execute(
        "SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers));")
    con.execute(
        "SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));")
    con.execute(
        "SELECT setval('invoices_id_seq', (SELECT MAX(id) FROM invoices));")
    con.execute(
        "SELECT setval('line_items_id_seq', \
            (SELECT MAX(id) FROM line_items));")

print(f'\ntables in postgres DB: {engine.table_names()}')
