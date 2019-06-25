from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
