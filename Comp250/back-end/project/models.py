from project import db


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    # One-to-many relationship (a customer may have many invoices)
    # If a customer is deleted, delete their invoices as well...
    invoices = db.relationship('Invoice',
                               uselist=True,
                               backref='customer',
                               cascade='all, delete-orphan',
                               lazy='select')

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'(# {self.id}) {self.first_name} {self.last_name}'

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    # One-to-many relationship (one product may be in many line items)
    line_items = db.relationship('LineItem',
                                 uselist=True,
                                 backref='product',
                                 lazy='select')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f'(# {self.id}) {self.name}, ${self.price}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }


class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    # 'ForeignKey' constrains entries in the invoices.customer_id column
    # to values in customers.id
    customer_id = db.Column(db.Integer,
                            db.ForeignKey('customers.id'),
                            unique=False)
    # Many-to-one relationship (many invoices may link to the same customer)
    # automatically established via 'backref' in customers.invoices
    # If desired, could use 'back_populates' on both tables to establish
    # relationship explicitly:
    # https://docs.sqlalchemy.org/en/13/orm/backref.html#relationships-backref
    # ------------------------------------------------------------------------
    # One-to-many relationship (an invoice may have many line items)
    # If an invoice is deleted, delete its line items as well...
    line_items = db.relationship('LineItem',
                                 uselist=True,
                                 backref='invoice',
                                 cascade='all, delete-orphan',
                                 lazy='select')

    def __init__(self, date, customer_id):
        self.date = date
        self.customer_id = customer_id

    def __repr__(self):
        return f'(# {self.id}) {self.date.strftime("%Y-%m-%d")} \
{self.customer_id}'

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date.strftime("%Y-%m-%d"),
            'customer_id': self.customer_id
        }


class LineItem(db.Model):
    __tablename__ = 'line_items'
    id = db.Column(db.Integer, primary_key=True)
    units = db.Column(db.Integer, nullable=False)
    invoice_id = db.Column(db.Integer,
                           db.ForeignKey('invoices.id'),
                           unique=False)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('products.id'),
                           unique=False)

    def __init__(self, invoice_id, product_id, units):
        self.invoice_id = invoice_id
        self.product_id = product_id
        self.units = units

    def __repr__(self):
        return f'(# {self.id}) {self.invoice_id} {self.product_id} \
{self.units}'

    def serialize(self):
        return {
            'id': self.id,
            'units': self.units,
            'invoice_id': self.invoice_id,
            'product_id': self.product_id
        }
