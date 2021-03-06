from flask import Flask, render_template, request

app = Flask(__name__)
people = {1: {'fname': 'Bird', 'lname': 'Person', 'age': 299},
          5: {'fname': 'Rick', 'lname': 'Sanchez', 'age': 65},
          12: {'fname': 'Justin', 'lname': 'Roiland', 'age': 39}
          }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
@app.route('/admin/')
def admin():
    return render_template('admin.html')


@app.route('/person/<id>')
@app.route('/person/<id>/')
def person(id=None):
    return render_template('person.html',
                           id=id,
                           person=people.get(int(id), {'fname': 'Not', 'lname':
                                             'Given', 'age': None}))


@app.route('/info')
def info():
    print(f'\n--> Args: {request.args}\n')
# http://flask.pocoo.org/docs/1.0/api/#flask.Request.args
    return render_template('info.html',
                           parm1=request.args.get("parm1", default="parm1"),
                           parm2=request.args.get("parm2", default="parm2"),
                           parm3=request.args.get("parm3", default="parm3"),
                           )


@app.route('/update')
def update():
    return render_template('update.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

