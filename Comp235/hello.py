from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS


app = Flask(__name__)
# CORS(app)


# dictionary which can be viewed via the '/info' route and updated
# via the '/update' route
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


# displays the person with 'id' from 'people' dictionary
# if 'id' is not present in the dictionary, a default missing person
# is returned
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

    # renders a page displaying the URL parameters passed to this route
    # return render_template('info.html',
    #                        parm1=request.args.get("parm1", default="parm1"),
    #                        parm2=request.args.get("parm2", default="parm2"),
    #                        parm3=request.args.get("parm3", default="parm3"))

    # simply returns the URL parameters passed to this route
#     return (f'parm1={request.args.get("parm1", default="parm1_default")}, \
# parm2={request.args.get("parm2", default="parm2_default")}, \
# parm3={request.args.get("parm3", default="parm3_default")}')

    # http://flask.pocoo.org/docs/1.0/api/#flask.json.jsonify
    # 'jsonify()' creates an HTTP '200 OK' repsonse to indicate that
    # the request to this route has succeeded
    # the argument to 'jsonify()' is converted to JSON and then turned into
    # a Response object with 'application/json' mimetype
    resp = jsonify(people)
    print(f'--> \'200 OK\' Response object (containing JSON data), sent from\
\'/info()\' route:\n\
resp:\n{resp}\n\
type of resp: {type(resp)}\n\
resp.response:\n{resp.response}\n\
type of resp.response : {type(resp.response )}\n')
    return resp, 200


@app.route('/update', methods=['GET', 'POST'])
def update():
    # return render_template('update.html')
    content = request.get_json()
    # print('Update:', request, content)
    print(f'content: {content}, type: {type(content)}')

    # get id of person sent by front-end: first (and only) key
    id = int(next(iter(content.keys())))
    # grab person data: first (and only) list entry
    new_person = list(content.values())[0]

    print(f'id: {id}, type: {type(id)}')
    print(f'new_person: {new_person}, type: {type(new_person)}')

    #   - if the id exists in the 'people', overwrite the person's data
    #   - othwerwise add the new person to 'people'
    #     same operation in both cases...
    if id in people:
        print(f'{people[id]["fname"]} {people[id]["lname"]} with id {id}, already exists')
    else:
        print(f'adding {new_person["fname"]} {new_person["lname"]} with id {id}')

    people[id] = new_person

    return jsonify({'worked': 'yes'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
