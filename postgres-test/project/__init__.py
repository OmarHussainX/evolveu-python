import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine

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
