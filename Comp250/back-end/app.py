from flask import jsonify
from project import app, db, session
from project.models import Customer, Product, Invoice, LineItem

@app.route('/')
def index():
    return f'<h1>Comp250 Flask server</h1>\n'


@app.route('/customers')
def customers():
    customers = Customer.query.all()
    return jsonify([customer.serialize() for customer in customers])


@app.route('/products')
def products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])


@app.route('/invoices')
def invoices():
    invoices = session.query(Invoice).all()
    print(f'session.query invoices: {invoices}, type: {type(invoices)}')
    return jsonify([invoice.serialize() for invoice in invoices])


"""
TRANSLATE THIS SQL QUERY INTO SQLALCHEMY
-- Get the customer id & name for each invoice...
select
invoices.id as invoice_id,
invoices.date as invoice_date,
customers.id as customer_id,
customers.first_name || ' ' || customers.last_name as customer_name
from invoices
inner join customers
on invoices.customer_id = customers.id
"""
@app.route('/test')
def test():
    cust_by_invoice = session.query(Invoice).\
        select_from(Invoice).\
        join(Customer, Customer.id == Invoice.customer_id).all()

    print(f'cust_by_invoice: {cust_by_invoice}\ntype: {type(cust_by_invoice)}')

    return jsonify({'test': 'please work'}), 200
    # return jsonify([customer.serialize() for customer in cust_by_invoice])


@app.route('/details')
def details():
    # invoices = session.query(Invoice).all()
    # print(f'session.query invoices: {invoices}, type: {type(invoices)}')

    # example of desired data structure
    inv_224 = {
        'id': 224,
        'date': '2019-04-02',
        'customer': {
            'id': 131,
            'first_name': 'Bob',
            'last_name': 'Sugar',
        },
        'line_items': [
            {'id': 9,
             'product_id': 7,
             'units': 7},
            {'id': 10,
             'product_id': 1,
             'units': 5}
        ],
        'products': [
            {'id': 1,
             'name': 'Pencil'},
            {'id': 7,
             'name': 'Calculator'}
        ]
    }
    return jsonify(inv_224), 200


@app.route('/invoices/<id>')
def invoice_by_id(id):
    try:
        invoice = Invoice.query.filter_by(id=id).first()

        # The endpoint is valid, but the resource itself does not exist
        if invoice is None:
            return jsonify({'id': None}), 404

        return jsonify(invoice.serialize())

    # The server encountered a situation it doesn't know how to handle
    except Exception as e:
        return (str(e)), 500


@app.route('/lineitems')
def line_items():
    line_items = LineItem.query.all()
    return jsonify([line_item.serialize() for line_item in line_items])


if __name__ == '__main__':
    app.run(debug=True)
