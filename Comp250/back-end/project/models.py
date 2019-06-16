from project import db


class Customer(db.Model):

    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    # One-to-many relationship (a customer may have many invoices)
    # If a customer is deleted, delete their invoices as well...
    invoices = db.relationship('Invoices',
                               uselist=True,
                               backref='customer',
                               cascade='all, delete-orphan',
                               lazy='select')

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'(# {self.id}) {self.first_name} {self.last_name.name}'
"""
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
 """


class Invoice(db.Model):

    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    # 'ForeignKey' constrains entries in the invoices.customer_id column
    # to values in customers.id
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    # Many-to-one relationship (many invoices may link to the same customer)
    # automatically established via 'backref' in customers.invoices
    # If desired, could use 'back_populates' on both tables to establish
    # relationship explicitly:
    # https://docs.sqlalchemy.org/en/13/orm/backref.html#relationships-backref

    def __init__(self, date, puppy_id):
        self.date = date

    def __repr__(self):
        return f'(# {self.id}) {self.date.strftime("%Y-%m-%d")}'
