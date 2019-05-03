import openpyxl

wk = openpyxl.load_workbook('sales_data.xlsx')

inv_wksheet = wk['Invoices']
line_items_wksheet = wk['Inv Line Items']
products_wksheet = wk['Product']


# Issue with using max_row as iteration limit:
#    spreadsheet has *several* empty rows...
# TODO: check for empty rows while iterating, and skip
#   (this will allows for the possibility of empty rows
#   interspersed amongst populated ones)
rows = inv_wksheet.max_row
columns = inv_wksheet.max_column


# Iterate over rows in worksheet, build dictionary of:
#   invoice Date with Invoice_ID as key
dates_by_inv = {}
for i in range(2,47+1):
        dates_by_inv[str(inv_wksheet.cell(i,2).value)] = inv_wksheet.cell(i,3).value

print('\ninvoice Date with Invoice_ID as key')
print(dates_by_inv)


# Iterate over rows in worksheet, build dictionary with Invoice_ID as key.
# Each key has as value a list of dictionaries, with:
#   Product_ID as key & Units as value
line_items_by_inv = {}
for i in range(2,66+1):
        if line_items_wksheet.cell(i,1).value in line_items_by_inv:
                line_items_by_inv[line_items_wksheet.cell(i,1).value].append({str(line_items_wksheet.cell(i,2).value): int(line_items_wksheet.cell(i,3).value)})
        else:
                line_items_by_inv[line_items_wksheet.cell(i,1).value] = [{str(line_items_wksheet.cell(i,2).value): int(line_items_wksheet.cell(i,3).value)}]

print('\nlist of invoice line items with Invoice_ID as key')
print(line_items_by_inv)


# Iterate over rows in worksheet, build dictionary of:
#   unit Price with Product_ID as key
products_by_id = {}
for i in range(2,9+1):
        products_by_id[str(products_wksheet.cell(i,1).value)] = int(products_wksheet.cell(i,3).value)
        
print('\nunit Price with Product_ID as key')
print(products_by_id)
