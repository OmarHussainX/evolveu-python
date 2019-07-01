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
        Return a list of all invoices with their associated records - example
        of returned data structure:
        '224': {
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
                'name': 'Pencil',
                'price': 10},
                {'id': 7,
                'name': 'Calculator',
                'price': 100}
            ]
        }
        ...
    """
    # obtain list of tuples:
    # [(Invoice, Customer), (Invoice, Customer), ...]
    cust_by_invoice = session.query(Invoice, Customer).\
        select_from(Invoice).\
        join(Customer, Customer.id == Invoice.customer_id).all()

    # build dictionary of invoice details, with invoice id as key
    inv_details = {}
    for (inv, cust) in cust_by_invoice:
        # add invoice record to dictionary, and
        # remove extraneous 'customer_id' key
        inv_details[inv.id] = inv.serialize()
        del inv_details[inv.id]['customer_id']

        # add customer record to dictionary
        inv_details[inv.id]['customer'] = cust.serialize()

        # obtain list of all line items related to invoice
        line_items = LineItem.query.filter_by(invoice_id=inv.id).all()

        # add line item records (and associated product records) to dictionary
        inv_details[inv.id]['line_items'] = []
        inv_details[inv.id]['products'] = []
        for line_item in line_items:
            # inv_details[inv.id]['line_items'].append(line_item.serialize())
            # avoid adding extraneous 'invoice_id' key
            inv_details[inv.id]['line_items'].append({
                'id': line_item.id,
                'product_id': line_item.product_id,
                'units': line_item.units,
            })
            inv_details[inv.id]['products'].append(Product.query.filter_by(
                id=line_item.product_id).first().serialize())

    # print(f'inv_details: {inv_details}\ntype: {type(inv_details)}')

    # NOTE: Unable to select only desired columns using
    # .options(load_only('col1', 'col2'))
    # or deferred columns in models...
    # https://docs.sqlalchemy.org/en/13/orm/loading_columns.html#load-only-and-wildcard-options
    #
    # Therefore, manually removed extraneous keys from 'inv_details' dictionary
    return jsonify(inv_details), 200


@app.route('/invoicedetails/<id>')
def invoice_details_by_id(id):
    """
    Return a dictionary of records related to invoice # 'id'
    """
    try:
        inv_details = {
            'customer': None,
            'line_items': [],
            'products': []
        }

        # Obtain invoice, add to dictionary
        invoice = Invoice.query.filter_by(id=id).first()
        inv_details.update(invoice.serialize())
        del inv_details['customer_id']

        # Obtain customer, add to dictionary
        customer = Customer.query.filter_by(id=invoice.customer_id).first()
        inv_details['customer'] = customer.serialize()

        # Obtain line items (and associated products), add to dictionary
        line_items = LineItem.query.filter_by(invoice_id=invoice.id).all()
        for line_item in line_items:
            inv_details['line_items'].append({
                'id': line_item.id,
                'product_id': line_item.product_id,
                'units': line_item.units,
            })
            inv_details['products'].append(Product.query.filter_by(
                id=line_item.product_id).first().serialize())

        if (invoice is None or
                customer is None or
                line_items is None):
            return jsonify({'id': None}), 404

        return jsonify(inv_details), 200

    # The server encountered a situation it doesn't know how to handle
    except Exception as e:
        return (str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)
