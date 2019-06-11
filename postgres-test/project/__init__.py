import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd
# ---------------------------
# https://stackoverflow.com/a/55495065/11245656
import csv
from io import StringIO
from sqlalchemy import create_engine, MetaData


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
# zeroth column has 'id' for postgres DB
db_data = pd.read_excel('db_data.xls',
                        sheet_name=['puppies', 'owners'],
                        index_col=0,
                        dtype=object)


print(f'\ndb_data["puppies"]:\n{db_data["puppies"]}')
print(f'\ndb_data["owners"]:\n{db_data["owners"]}')


# https://stackoverflow.com/a/55495065/11245656
def psql_insert_copy(table, conn, keys, data_iter):
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/test')
# metadata = MetaData(engine)
# metadata.drop_all()

# db_data['puppies'].to_sql('puppies', engine, method=psql_insert_copy)

db_data['puppies'].to_sql('puppies',
                          engine,
                          if_exists='replace',
                          )

db_data['owners'].to_sql('owners',
                         engine,
                         if_exists='replace',
                         )

# db_data['owners'].to_sql('owners', engine, method=psql_insert_copy)
