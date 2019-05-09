from validate_sales_data import validate_sales_data
from pathlib import Path
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, Fill
import pandas as pd

merged_file = 'merged_sales_data.xlsx'


def merge_sales_data(file1, file2):
    """
    Receives references to two sales data spreadsheets which contain
    validated data, and intelligently (checks for clients common to
    the two data sets) merges them into a new spreadsheet
    """

    # ----------------------------------------------------------
    def copy_sheet(source, target, source_rows_max, source_cols_max,
                   source_start_row, target_start_offset):
        """
        Helper function
        Copies an entire worksheet from 'source' to 'target',
        which are in _different_ workbooks (this precludes the use
        of 'target = wb.copy_worksheet(source)')
        """
        for i in range(source_start_row, source_rows_max + 1):
            # NOTE: skipping blank rows found in the source sheet doesn't help:
            # Even if the blank source row is skipped, the row counter must
            # advance by one, which will by necessity create a blank row in the
            # target.
            for j in range(1, source_cols_max + 1):
                target.cell(target_start_offset + i, j).value = \
                    source.cell(i, j).value
    # ----------------------------------------------------------

    # Create new (target) workbook with blank sheets
    wb_new = openpyxl.Workbook()
    ws_clients = wb_new.active
    ws_clients.title = 'customers'
    ws_invoices = wb_new.create_sheet('invoices')
    ws_line_items = wb_new.create_sheet('invoice line items')
    ws_products = wb_new.create_sheet('products')

    # Open first workbook whose data is to be merged, and then...
    wb = openpyxl.load_workbook(file1, data_only=True)

    # ...copy all worksheets of interest from source to target
    copy_sheet(wb['customers'], ws_clients, wb['customers'].max_row,
               wb['customers'].max_column, 1, 0)

    copy_sheet(wb['invoices'], ws_invoices, wb['invoices'].max_row,
               wb['invoices'].max_column, 1, 0)

    copy_sheet(wb['invoice line items'], ws_line_items,
               wb['invoice line items'].max_row,
               wb['invoice line items'].max_column, 1, 0)

    copy_sheet(wb['products'], ws_products, wb['products'].max_row,
               wb['products'].max_column, 1, 0)

    # build list of customer IDs from first workbook, and:
    # - remove header cell ('Customers')
    # - remove values from empty cells (None)
    file1_customers = [cell.value for cell in wb['customers']['A']]
    del file1_customers[0]
    file1_customers = [id for id in file1_customers if id is not None]

    # Open second workbook whose data is to be merged, and then...
    wb = openpyxl.load_workbook(file2, data_only=True)

    # ...copy all worksheets of interest from source to target,
    # taking care to:
    #   - skip the first row of the source (headers already present in target)
    #   - start writing data from the last row of the target
    #   - when merging customer data, ensure that customers common to both
    #     source spreadsheets are not repeated!
    merge_row_offset = ws_clients.max_row
    for i in range(2, wb['customers'].max_row + 1):
        if wb['customers'].cell(i, 1).value in file1_customers:
            continue
        for j in range(1, wb['customers'].max_column + 1):
                ws_clients.cell(merge_row_offset + i, j).value = \
                    wb['customers'].cell(i, j).value

    copy_sheet(wb['invoices'], ws_invoices, wb['invoices'].max_row,
               wb['invoices'].max_column, 2, ws_invoices.max_row)

    copy_sheet(wb['invoice line items'], ws_line_items,
               wb['invoice line items'].max_row,
               wb['invoice line items'].max_column, 2, ws_line_items.max_row)

    # ----------------------------------------------------------
    def worksheet_cleaner(worksheet, key_header_title, sheet_index):
        """
        Helper function
        Receives a reference to a worksheet, and the title of a key
        header in that worksheet. Deletes the worksheet and creates a
        new one at 'sheet_index' which is:
        - sorted by the key header
        - devoid of any rows where the key column is empty/NaN
        """
        data = worksheet.values
        # Get column headers from first row
        columns = next(data)[0:]

        # Create a DataFrame from the second row of data onward, and sort
        # by key header in order to 'remove' blank rows
        df = pd.DataFrame(data, columns=columns)
        df.sort_values([key_header_title], inplace=True)
        df.dropna(subset=[key_header_title], inplace=True)

        # remove current worksheet from merged workbook, and...
        # worksheet_title = worksheet.title
        wb_new.remove(worksheet)

        # ...add new worksheet with the same title, containing data from
        # the sorted and cleaned DataFrame
        worksheet = wb_new.create_sheet(worksheet.title, sheet_index)

        for row in dataframe_to_rows(df, index=False, header=True):
            worksheet.append(row)

    # ----------------------------------------------------------

    # 'Clean' each worksheet: sort by ID, and remove blank rows
    worksheet_cleaner(ws_clients, 'Customer', 0)
    worksheet_cleaner(ws_invoices, 'Invoice', 1)
    worksheet_cleaner(ws_line_items, 'Invoice', 2)

    # Apply styles
    for sheet in wb_new:
        print(f'Worksheet: {sheet.title}')
        print(f'row #1: {sheet[1]}')
        for cell in sheet[1]:
            print(f'make bold: {cell.value}')
            cell.font = Font(bold=True)

    # Save target workbook to disk
    wb_new.save(merged_file)


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
        print(f'ERROR: file \'{file1}\' contains invalid data\n\
See \'validate_sales_data_report.txt\' for details')
        return

    file2 = input("Enter second file (hit enter for 'sales_data2.xlsx')\n> ")
    if file2 == "":
        file2 = 'sales_data2.xlsx'
    print(f'Second file: {file2}\n')

    file_path2 = Path(file2)
    if not file_path2.is_file():
        print(f'ERROR: file \'{file2}\' not found')
        return

    if not validate_sales_data(file2):
        print(f'ERROR: file \'{file2}\' contains invalid data\n\
See \'validate_sales_data_report.txt\' for details')
        return

    merge_sales_data(file1, file2)

if __name__ == '__main__':
    main()
