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
