"""
NOTE: Had to
- manually create the postgres database
- run the initialisaton below to create the tables
========= Initialise database =========
export FLASK_APP=app.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade
=======================================
"""

from project import app, db
from flask import render_template, url_for, redirect
from project.forms import AddForm, OwnerForm, DelForm
from project.models import Puppy, Owner


############################################
#           VIEWS WITH FORMS
############################################

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/add', methods=['GET', 'POST'])
def add_pup():
    form = AddForm()

    # On form submission, add puppy to db and redirect
    # to puppy list view, otherwise...
    if form.validate_on_submit():
        name = form.name.data

        # Add new Puppy to database
        new_pup = Puppy(name)
        db.session.add(new_pup)
        db.session.commit()

        return redirect(url_for('list_pup'))

    # ...display add puppy form
    return render_template('add.html', form=form)


@app.route('/addowner', methods=['GET', 'POST'])
def add_owner():
    form = OwnerForm()

    # On form submission, add owner to db and redirect
    # to puppy list view, otherwise...
    if form.validate_on_submit():
        name = form.name.data
        puppy_id = form.id.data

        # Add new Puppy to database
        new_owner = Owner(name, puppy_id)
        db.session.add(new_owner)
        db.session.commit()

        return redirect(url_for('list_pup'))

    # ...display add owner form
    return render_template('addowner.html', form=form)


@app.route('/list')
def list_pup():
    # Grab a list of all puppies from the database
    # and display it
    puppies = Puppy.query.all()
    return render_template('list.html', puppies=puppies)


@app.route('/delete', methods=['GET', 'POST'])
def del_pup():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        pup = Puppy.query.get(id)
        print(f'pup to be deleted is: id#{id} --> {pup}')
        if pup is not None:
            db.session.delete(pup)
            db.session.commit()

        return redirect(url_for('list_pup'))

    return render_template('delete.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
