from project import app, db
from project.models import Customer


@app.route('/')
def index():
    return f'<h1>Comp250 Flask server</h1>\n'


@app.route('/list')
def list_customers():
    pass
    # Grab a list of all customers from the database
    # and display it
    customers = Customer.query.all()
    print(f'customers: {customers}')
    return customers


if __name__ == '__main__':
    app.run(debug=True)
