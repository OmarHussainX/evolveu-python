"""
NOTE:
Installation of psycopg2 failed for latest release, worked fine when specifying an older version: 2.7.6.1
Didn't test to see what the last installable version is...
https://www.reddit.com/r/learnpython/comments/aah5da/pipenv_install_psycopg2_installs_package_but_cant/
"""
from project import db


class Puppy(db.Model):

    __tablename__ = 'puppies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # One-to-one relationship (1 dog per 1 owner & vice versa)
    # If a puppy is deleted, delete the owner as well
    owner = db.relationship('Owner',
                            backref='puppies',
                            uselist=False,
                            cascade='all, delete-orphan')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"(id: {self.id}) Puppy {self.name}, owner {self.owner.name}"
        else:
            return f"(id: {self.id}) Puppy {self.name} - no owner"


class Owner(db.Model):

    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id
