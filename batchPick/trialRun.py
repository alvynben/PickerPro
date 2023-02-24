import pandas as pd
import numpy as np
import datetime as dt
import random as rand
from collections import Counter
import itertools
from ast import literal_eval
import statistics
import matplotlib.pyplot as plt
from parse import inventory
from parse import map as warehouseMap

# Constants
CSV_FILE_NAME = "trial_data.csv"

# Utils
def get_unique_count(df: pd.DataFrame, col_name: pd.Index):
    return len(df[col_name].unique())

# Extract Data
df = pd.read_csv(CSV_FILE_NAME)

# Transform Data

# Invoice Format
""" Posting No.                                   BCMINV-220500399
Document No.                                      BCMSO-026974
Posting Date                                         5/24/2022
Customer No.                                          C-005192
Customer Name               ISS CATERING SERVICES PTE LTD - MJ
Ship-to Name                ISS CATERING SERVICES PTE LTD - MJ
Division Code                                      CATERER/MFR
No.                                                  ZZRF600GM
Description                           ELEPHANT BALL RICE FLOUR
Packing Size                                        16 X 600GM
Qty. per Unit of Measure                                     1
UOM                                                        PKT
Quantity                                                     3
Quantity (Base)                                              3 """

invoice_to_weight = pd.DataFrame(df, columns=["Document No.", "Quantity"]).groupby("Document No.")

# Apply Knapsack Algorithm on Invoices
total_no_of_orders: int = len(df.index)
orders_remaining: int = total_no_of_orders
MAX_QUANTITY = 48
current_quantity = 0
current_batch = []
all_batches = []
prev_invoice = df.iloc[0]['Document No.']

while orders_remaining or current_batch:
    if not orders_remaining:
        all_batches.append(current_batch)
        current_batch = []
        current_quantity = 0
        break
    
    row_to_check = total_no_of_orders - orders_remaining
    current_invoice = df.iloc[row_to_check]['Document No.']
    bound_to_overflow = False
    if current_invoice != prev_invoice:
        bound_to_overflow = current_quantity + invoice_to_weight.get_group(current_invoice).sum()["Quantity"] > MAX_QUANTITY
    
    if not bound_to_overflow:
        current_batch.append(df.iloc[row_to_check]['No.'])
        prev_invoice = current_invoice
        orders_remaining -= 1
        current_quantity += df.iloc[row_to_check]['Quantity']
    else:
        # add edited batch to all_batches
        all_batches.append(current_batch)
        current_batch = []
        current_quantity = 0

# Apply Pathing on Group of Items
all_locs = []
for batch in all_batches:    
    locs = list(map(lambda x: warehouseMap.get_coordinates(inventory.get_item_location(x)), batch))
    batch = list(map(lambda x: inventory.get_item_location(x), batch))
    all_locs.append(locs)
