from flask import jsonify
from project import app, db
from project.models import Customer, Product, Invoice, LineItem


@app.route('/')
def index():
    return f'<h1>Comp250 Flask server</h1>\n'


@app.route('/customers')
def customers():
    # Grab a list of all customers from DB & convert to JSON
    customers = Customer.query.all()
    print(f'---------- customers:\n{customers}')
    return jsonify([customer.serialize() for customer in customers])


@app.route('/products')
def products():
    # Grab a list of all products from DB & convert to JSON
    products = Product.query.all()
    print(f'---------- products:\n{products}')
    return jsonify([product.serialize() for product in products])


@app.route('/invoices')
def invoices():
    # Grab a list of all invoices from DB & convert to JSON
    invoices = Invoice.query.all()
    print(f'---------- invoices:\n{invoices}')
    return jsonify([invoice.serialize() for invoice in invoices])


@app.route('/lineitems')
def line_items():
    # Grab a list of all line items from DB & convert to JSON
    line_items = LineItem.query.all()
    print(f'---------- line_items:\n{line_items}')
    return jsonify([line_item.serialize() for line_item in line_items])


if __name__ == '__main__':
    app.run(debug=True)
