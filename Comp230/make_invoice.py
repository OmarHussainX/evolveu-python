import openpyxl


# table customers: $1 - id, $2 - first name, $3 - last name
# table invoices: $1 - id, $2 - customer, $ - date
# table products: $1 - id, $2 - name, $3 - price, $4 inventory
# table line sales: $1 - id, $2 - product, $ - quantity

def make_invoice(invoice_id):
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

    wb = openpyxl.load_workbook('sales_data.xlsx')

    cust_wksheet = wb['customers']
    inv_wksheet = wb['invoices']
    line_items_wksheet = wb['invoice line items']
    products_wksheet = wb['products']

    # Iterate over rows in worksheet, build dictionary of:
    #   unit Price with Product_ID as key
    products_by_id = {}
    for i in range(2, products_wksheet.max_row + 1):
            if not (products_wksheet.cell(i, 1).value is None):
                products_by_id[products_wksheet.cell(i, 1).value] = \
                    {'price': products_wksheet.cell(i, 3).value,
                     'name': products_wksheet.cell(i, 2).value}

    invoice_txt = ''

    # get customer id, invoice date
    customer_id = None
    invoice_date = None
    for i in range(2, inv_wksheet.max_row + 1):
            if not (inv_wksheet.cell(i, 1).value is None):
                if (invoice_id == inv_wksheet.cell(i, 1).value):
                    customer_id = inv_wksheet.cell(i, 3).value
                    invoice_date = inv_wksheet.cell(i, 2).value\
                        .strftime('%Y-%m-%d')

    if customer_id is None:
        return

    # get customer name
    customer_name = ''
    for i in range(2, cust_wksheet.max_row + 1):
            if not (cust_wksheet.cell(i, 1).value is None):
                if (customer_id == cust_wksheet.cell(i, 1).value):
                    customer_name = cust_wksheet.cell(i, 2).value + \
                        ' ' + cust_wksheet.cell(i, 3).value


    # get invoice line items
    line_items = {}
    for i in range(2, line_items_wksheet.max_row + 1):
        if not (line_items_wksheet.cell(i, 1).value is None):
            if (invoice_id == line_items_wksheet.cell(i, 2).value):
                line_items[line_items_wksheet.cell(i, 3).value] = \
                    line_items_wksheet.cell(i, 4).value

    invoice_txt += f'\
{customer_name} (client ID: {customer_id})\n\
{format("Invoice #  ", ">50")}\
{format(invoice_id, "<10")}\n\
{format("Invoice date  ", ">50")}\
{invoice_date}\n'

    """
    Invoice is 60 columns wide:
    12 cols: Quantity, centered
    20 cols: Item name, left-aligned
    11 cols: Unit price, right-aligned
    17 cols: Line total, right-aligned
    """
    invoice_txt += f'\n\n\
{format("Quantity", "^12")}\
{format("Item", "<20")}\
{format("Unit price", ">11")}\
{format("Line total", ">17")}\n\
{format("--------", "^12")}\
{format("----", "<20")}\
{format("----------", ">11")}\
{format("----------", ">17")}\n'

    grand_total = 0
    line_total = 0
    for k, v in line_items.items():
        line_total = v * products_by_id[k]['price']
        grand_total += line_total
        invoice_txt += f'\
{format(v, "^12")}\
{format(products_by_id[k]["name"], "20")}\
{format(products_by_id[k]["price"], ">11,.2f")}\
{format("$", ">8")}\
{format(line_total, ">9,.2f")}\n'

    invoice_txt += f'\n\n\
{format(" ", ">49")}\
{format("----------", ">11")}\n\
{format("TOTAL", ">43")}\
{format("$", ">8")}\
{format(grand_total, "9,.2f")}\n'

    print(invoice_txt)


def main():
    # print(f'\n---------- {__file__} ----------')
    make_invoice(266)


if __name__ == '__main__':
    main()
