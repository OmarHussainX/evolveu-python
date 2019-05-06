"""
sales_data.xlsx MUST have four worksheets (in any order) named:
'customers', 'invoices', 'invoice line items', 'products'

The data will be validated to ensure that it has:
* 10 - 15 _unique_ clients
* 3 - 4 invoices per client
* 1 - 5 items per invoice
* invoices for one month only
* $15,000 (+/- 1,500) of invoices per month
"""

import openpyxl


# Set a bunch of flags, check them at the end to determine whether
# or not the data set is valid
clients_not_repeated = True
client_count_in_range = True
client_invoice_count_in_range = True
invoices_for_one_month = True
invoices_per_month_in_range = True


# Load worksheets
# Set 'data_only' so that the _results_ of formulae are accessible
wb = openpyxl.load_workbook('sales_data.xlsx', data_only=True)
client_sheet = wb['customers']
invoices_sheet = wb['invoices']
inv_line_items_sheet = wb['invoice line items']
products_sheet = wb['products']


# Create list of customer #
# - check for duplicates
# - check if there are between 10 and 15 clients
client_list = []
for col in client_sheet.iter_cols(min_row=2, max_col=1,
                                  max_row=client_sheet.max_row):
    for cell in col:
        if not (cell.value is None):
            client_list.append(cell.value)

clients_not_repeated = len(client_list) == len(set(client_list))
client_count_in_range = 10 <= len(client_list) <= 15


# Ensure there are 3 - 4 invoices per client:
# - using client # as key, build up a list of invoices, and then
#   check that each client has 3 - 4 invoices
# - build up a list of the month of issue for each invoice, and then
#   check that all invoices were issued in the same month
invoices_per_client = {}
invoices_month = []
for i in range(2, invoices_sheet.max_row+1):
        if not (invoices_sheet.cell(i, 3).value is None):
            if invoices_sheet.cell(i, 3).value in invoices_per_client:
                    invoices_per_client[invoices_sheet.cell(i, 3).value]\
                        .append(invoices_sheet.cell(i, 1).value)
            else:
                    invoices_per_client[invoices_sheet.cell(i, 3).value] = \
                        [invoices_sheet.cell(i, 1).value]
            invoices_month.append(invoices_sheet.cell(i, 2).value
                                  .strftime("%B"))

invoices_for_one_month = len(set(invoices_month)) == 1

for invoices in invoices_per_client.values():
    print(f'invoices, count: {invoices}, {len(invoices)}')
    if len(invoices) < 3 or len(invoices) > 4:
        client_invoice_count_in_range = False


# Ensure there are 1 - 5 items per invoice:
# - using invoice # as key, build up a list of invoices, and then
#   check that each client has 3 - 4 invoices
# - add up the line totals for each invoice to get the total of all
#   invoices issued, and then ensure it is valid
items_per_invoice = {}
invoices_total = 0
for i in range(2, inv_line_items_sheet.max_row+1):
        if not (inv_line_items_sheet.cell(i, 2).value is None):
            if inv_line_items_sheet.cell(i, 2).value in items_per_invoice:
                    items_per_invoice[inv_line_items_sheet.cell(i, 2).value]\
                        .append(inv_line_items_sheet.cell(i, 3).value)
            else:
                    items_per_invoice[inv_line_items_sheet.cell(i, 2).value] =\
                        [inv_line_items_sheet.cell(i, 3).value]
            invoices_total += inv_line_items_sheet.cell(i, 6).value

invoices_per_month_in_range = (15000-1500) <= invoices_total <= (15000+1500)

for line_items in items_per_invoice.values():
    print(f'line_items, count: {line_items}, {len(line_items)}')
    if len(line_items) < 1 or len(line_items) > 5:
        client_invoice_count_in_range = False
