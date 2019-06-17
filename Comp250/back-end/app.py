from flask import jsonify
from project import app, db
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
    invoices = Invoice.query.all()
    return jsonify([invoice.serialize() for invoice in invoices])


@app.route('/lineitems')
def line_items():
    line_items = LineItem.query.all()
    return jsonify([line_item.serialize() for line_item in line_items])


if __name__ == '__main__':
    app.run(debug=True)
