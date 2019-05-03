import openpyxl

wk = openpyxl.load_workbook('sales_data.xlsx')

inv_wksheet= wk['Invoices']
line_items_wksheet= wk['Inv Line Items']

print(inv_wksheet.max_row)

rows = inv_wksheet.max_row
columns = inv_wksheet.max_column

dates_by_inv={}

for i in range(2,47+1):
        dates_by_inv[inv_wksheet.cell(i,2).value] = inv_wksheet.cell(i,3).value
        
# print(dates_by_inv)

line_items_by_inv={}
for i in range(2,66+1):
        # line_items_by_inv[line_items_wksheet.cell(i,1).value] = line_items_wksheet.cell(i,2).value
        if line_items_wksheet.cell(i,1).value in line_items_by_inv:
                line_items_by_inv[line_items_wksheet.cell(i,1).value].append({str(line_items_wksheet.cell(i,2).value): line_items_wksheet.cell(i,3).value})
        else:
                line_items_by_inv[line_items_wksheet.cell(i,1).value] = [{str(line_items_wksheet.cell(i,2).value): line_items_wksheet.cell(i,3).value}]

print(line_items_by_inv)










# #FIND OUT VALUE OF A CEL 
# #workbook level 
# wk = openpyxl.load_workbook('data.xlsx')
# #inv_wksheeteet level
# sh = wk['Sheet1']
# #get value of a cell
# print(sh['A3'].value)
# print(sh['B4'].value)

# #another method to fetch value
# c1 = sh.cell(1,1) #first you create cell value # row 1, column 1
# print(c1.value)

# # READ ALL THE DATA IN AN EXCEL FILE  
# #find how many rows there are

# rows = sh.max_row #finds out how many rows there are
# columns = sh.max_column
# print(rows)
# print(columns)

# for i in range(1,rows+1):
#     for j in range(1, columns+1):
#         c = sh.cell(i,j)
#         print(c.value)
