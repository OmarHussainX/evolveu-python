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


@app.route('/invoicedetails')
def invoice_details():
    """
        Example of desired data structure
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
    """
    # obtain list of tuples:
    # [(Invoice, Customer), (Invoice, Customer), ...]
    cust_by_invoice = session.query(Invoice, Customer).\
        select_from(Invoice).\
        join(Customer, Customer.id == Invoice.customer_id).all()

    # build dictionary of invoice details, with invoice id as key
    inv_details = {}
    for (inv, cust) in cust_by_invoice:
        # add invoice record to dictionary
        inv_details[inv.id] = inv.serialize()

        # add customer record to dictionary
        inv_details[inv.id]['customer'] = cust.serialize()

        # obtain list of all line items related to invoice
        line_items = LineItem.query.filter_by(invoice_id=inv.id).all()

        # add line item records (and associated product records) to dictionary
        inv_details[inv.id]['line_items'] = []
        inv_details[inv.id]['products'] = []
        for line_item in line_items:
            inv_details[inv.id]['line_items'].append(line_item.serialize())
            inv_details[inv.id]['products'].append(Product.query.filter_by(
                id=line_item.product_id).first().serialize())

    # print(f'inv_details: {inv_details}\ntype: {type(inv_details)}')

    return jsonify(inv_details), 200


if __name__ == '__main__':
    app.run(debug=True)
