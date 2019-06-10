from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddForm(FlaskForm):

    name = StringField('Name of Puppy:')
    submit = SubmitField('Add Puppy')


class OwnerForm(FlaskForm):

    name = StringField('Name of Owner:')
    id = IntegerField('ID of Puppy to Adopt:')
    submit = SubmitField('Add Owner')


class DelForm(FlaskForm):

    id = IntegerField('ID of Puppy to Remove:')
    submit = SubmitField('Remove Puppy')
