from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

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

# Session configuration
Session = sessionmaker()
engine = create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost/sales',
    echo=True)
Session.configure(bind=engine)
session = Session()
