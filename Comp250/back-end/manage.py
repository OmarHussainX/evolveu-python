"""
1. Create 'sales' database in PostgreSQL

2. Using Flask-Script...
https://flask-migrate.readthedocs.io/en/latest/

...create tables with columns & relationships as defined in python models,
by executing datatabase migration commands which can be accessed by running the
'manage.py' script:

python manage.py db init
python manage.py db migrate -m "initial migration"
python manage.py db upgrade
python manage.py db --help

3. In order to populate the database with records from sales_data.xlsx, run:
python db_load_data.py
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# WHY CAN THE IMPORT NOT BE FROM 'project'?
# from project import app, db
from app import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
