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


if __name__ == '__main__':
    app.run(debug=True)
