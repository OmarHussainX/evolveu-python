from flask import jsonify, request, url_for
from project import app, db
from project.models import Customer, Product, Invoice, LineItem


@app.route('/')
def index():
    return f'<h1>Comp250 Flask server</h1>\n'


# ------------------------------------------------------------
@app.route('/customers')
def customers():
    """ Get list of all customers """
    customers = Customer.query.all()
    return jsonify([customer.serialize() for customer in customers])


@app.route('/customers/<int:id>')
def customer_by_id(id):
    """ Get customer with # 'id' """
    try:
        customer = Customer.query.filter_by(id=id).first()

        # Endpoint is valid, but resource itself does not exist
        if customer is None:
            return jsonify({'id': None,
                            'status': 'error',
                            'message': f'no customer with id {id}'
                            }), 404

        return jsonify(customer.serialize())

    # Server encountered situation it doesn't know how to handle
    except Exception as e:
        return (str(e)), 500


@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    """ Delete customer with # 'id' """
    try:
        customer = Customer.query.filter_by(id=id).first()

        if customer is None:
            return jsonify({'id': None,
                            'status': 'error',
                            'message': f'no customer with id {id}'
                            }), 404

        db.session.delete(customer)
        db.session.commit()
        return jsonify({'customer': customer.serialize(),
                        'message': 'successfully deleted'}), 201

    except Exception as e:
        return (str(e)), 500


@app.route('/customers', methods=['PUT'])
def update_customer():
    """ Update an existing customer """
    data = request.get_json()

    if data is None:
        return jsonify({'status': 'error',
                        'message': 'JSON data expected, not found'
                        }), 400

    try:
        if 'id' not in data:
            return jsonify({'status': 'error',
                            'message': 'JSON data missing required key (id)'
                            }), 400

        else:
            customer = Customer.query.filter_by(id=data['id']).first()

            if customer is None:
                return jsonify({'id': None,
                                'status': 'error',
                                'message': f'no customer with id {data["id"]}'
                                }), 404

            customer.first_name = data.get('first_name', customer.first_name)
            customer.last_name = data.get('last_name', customer.last_name)
            db.session.commit()

            return jsonify({'customer': customer.serialize(),
                            'uri': url_for('customer_by_id',
                                           id=customer.id,
                                           _external=True)}), 201

    except Exception as e:
        return jsonify({'status': 'error',
                        'message': str(e)}), 500


@app.route('/customers', methods=['POST'])
def add_customer():
    """ Add new customer """
    data = request.get_json()

    if data is None:
        return jsonify({'status': 'error',
                        'message': 'JSON data expected, not found'
                        }), 400

    try:
        if all(k in data for k in ('first_name', 'last_name')):
            new_customer = Customer(data['first_name'], data['last_name'])
            db.session.add(new_customer)
            db.session.commit()
            return jsonify({'customer': new_customer.serialize(),
                            'uri': url_for('customer_by_id',
                                           id=new_customer.id,
                                           _external=True)}), 201

        else:
            return jsonify({'status': 'error',
                            'message': 'JSON data missing required key(s)'
                            }), 400

    except Exception as e:
        return jsonify({'status': 'error',
                        'message': str(e)}), 500


# ------------------------------------------------------------
@app.route('/products')
def products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])


# ------------------------------------------------------------
@app.route('/lineitems')
def line_items():
    line_items = LineItem.query.all()
    return jsonify([line_item.serialize() for line_item in line_items])


# ------------------------------------------------------------
@app.route('/invoices')
def invoices():
    invoices = db.session.query(Invoice).all()
    return jsonify([invoice.serialize() for invoice in invoices])


@app.route('/invoices/<int:id>')
def invoice_by_id(id):
    try:
        invoice = Invoice.query.filter_by(id=id).first()

        if invoice is None:
            return jsonify({'id': None}), 404

        return jsonify(invoice.serialize())

    except Exception as e:
        return (str(e)), 500


# ------------------------------------------------------------
@app.route('/invoicedetails')
def invoice_details():
    """ Return a list of all invoices with their associated records - example
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
    cust_by_invoice = db.session.query(Invoice, Customer).\
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
            # avoid extraneous 'invoice_id' key which 'serialize()' would add
            inv_details[inv.id]['line_items'].append({
                'id': line_item.id,
                'product_id': line_item.product_id,
                'units': line_item.units,
            })
            inv_details[inv.id]['products'].append(Product.query.filter_by(
                id=line_item.product_id).first().serialize())

    # NOTE: Unable to select only desired columns using
    # .options(load_only('col1', 'col2'))
    # or deferred columns in models...
    # https://docs.sqlalchemy.org/en/13/orm/loading_columns.html#load-only-and-wildcard-options
    #
    # Therefore, manually removed extraneous keys from 'inv_details' dictionary
    return jsonify(inv_details)


@app.route('/invoicedetails/<int:id>')
def invoice_details_by_id(id):
    """ Return a dictionary of records related to invoice # 'id' """
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

        if (invoice is None or customer is None or line_items is None):
            return jsonify({'status': 'error',
                            'message': f'unable to obtain records \
                                for invoice # {id}'
                            }), 404

        return jsonify(inv_details)

    except Exception as e:
        return (str(e)), 500


# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
