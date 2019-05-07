from validate_sales_data import validate_sales_data
from pathlib import Path
import openpyxl

merged_file = 'merged_sales_data.xlsx'


def merge_sales_data(file1, file2):
    """
    Receives references to two sales data spreadsheets which contain
    validated data, and intelligently (checks for clients common to
    the two data sets) merges them into a new spreadsheet
    """

    def copy_sheet(source, target, rows, cols):
        """
        Helper function
        Copies an entire worksheet from 'source' to 'target'
        """
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                    target.cell(i, j).value = source.cell(i, j).value

    new_wb = openpyxl.Workbook()
    ws_clients = new_wb.active
    ws_clients.title = 'customers'
    ws_invoices = new_wb.create_sheet('invoices')
    ws_line_items = new_wb.create_sheet('invoice line items')
    ws_products = new_wb.create_sheet('products')

    wb = openpyxl.load_workbook(file1, data_only=True)

    copy_sheet(wb['customers'], ws_clients, wb['customers'].max_row,
               wb['customers'].max_column)

    copy_sheet(wb['invoices'], ws_invoices, wb['invoices'].max_row,
               wb['invoices'].max_column)

    copy_sheet(wb['invoice line items'], ws_line_items,
               wb['invoice line items'].max_row,
               wb['invoice line items'].max_column)

    copy_sheet(wb['products'], ws_products, wb['products'].max_row,
               wb['products'].max_column)

    new_wb.save(merged_file)


def main():
    # print(f'\n---------- {__file__} ----------')
    print(f'\n== This will merge two sales data spreadsheets into \
\'{merged_file}\' ==\n')

    file1 = input("Enter first file (hit enter for 'sales_data.xlsx')\n> ")
    if file1 == "":
        file1 = 'sales_data.xlsx'
    print(f'First file: {file1}\n')

    file_path1 = Path(file1)
    if not file_path1.is_file():
        print(f'ERROR: file \'{file1}\' not found')
        return

    if not validate_sales_data(file1):
        print(f'ERROR: file \'{file1}\' contains invalid data - see \
\'validate_sales_data_report.txt\' for details')
        return

#     file2 = input("Enter second file\n> ")
#     print(f'Second file: {file2}\n')

#     file_path2 = Path(file2)
#     if not file_path2.is_file():
#         print(f'ERROR: file \'{file2}\' not found')
#         return

#     if not validate_sales_data(file2):
#         print(f'ERROR: file \'{file2}\' contains invalid data - see \
# \'validate_sales_data_report.txt\' for details')
#         return

    merge_sales_data(file1, None)

if __name__ == '__main__':
    main()
