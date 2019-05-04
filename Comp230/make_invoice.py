# our data model is
# table customers: $1 - id, $2 - first name, $3 - last name
# table invoices: $1 - id, $2 - customer, $ - date
# table products: $1 - id, $2 - name, $3 - price, $4 inventory
# table line sales: $1 - id, $2 - product, $ - quantity

# reports we need:
# total amount invoiced on a given date
def make_invoice (invoice_id):
        # determine customer name and invoice date from invoice_id from the invoices table
        # build a header that shows invoice id, date, and customer
        # initialize grand total as 0
        # loop through line item for this invoice id
        #   determine product name and price from the line item
        #   calculate line total
        #   add a line to invoice with product name, price, quantity and subtotal line
        #   add subtotal to grand total
        # end the grand total line with the grand total that we have already calculated
        # return what we have created



    return 0






"""
TODO

1: check for empty rows while iterating, and skip
   (this will allows for the possibility of empty rows
   interspersed amongst populated ones)
"""


import pandas as pd
import numpy as np

customers_sheet = pd.read_excel('sales_data.xlsx', sheet_name='Customers', index_col=0)

print(customers_sheet.head())
