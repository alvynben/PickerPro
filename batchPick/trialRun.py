import pandas as pd
import numpy as np
import datetime as dt
import random as rand
from collections import Counter
import itertools
from ast import literal_eval
import statistics
import matplotlib.pyplot as plt

# Constants
CSV_FILE_NAME = "trial_data.csv"

# Utils
def get_unique_count(df: pd.DataFrame, col_name: pd.Index):
    return len(df[col_name].unique())

# Extract Data
df = pd.read_csv(CSV_FILE_NAME)
print(df.head(10))

# Transform Data
print(df.iloc[2])

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
# print(invoice_to_weight.loc[invoice_to_weight["DocumentNo."] == "BCMSO-026974"])
# print(invoice_to_weight.get_group("BCMSO-026974").sum()["Quantity"])

# Apply Knapsack Algorithm on Invoices
total_no_of_invoices: int = len(df.index)
invoices_remaining: int = total_no_of_invoices
MAX_QUANTITY = 40
current_quantity = 0
current_batch = []
all_batches = []
prev_invoice = df.iloc[0]['Document No.']

while invoices_remaining:
    row_to_check = total_no_of_invoices - invoices_remaining
    current_invoice = df.iloc[row_to_check]['Document No.']
    bound_to_overflow = False
    if current_invoice != prev_invoice:
        bound_to_overflow = current_quantity + invoice_to_weight.get_group(current_invoice).sum()["Quantity"] > MAX_QUANTITY
        print(current_quantity + invoice_to_weight.get_group(current_invoice).sum()["Quantity"])
        print("current invoice: ", current_invoice, " prev invoice: ", prev_invoice)
        print("bound to overflow: ", bound_to_overflow)
        prev_invoice = current_invoice
    
    
    if not bound_to_overflow and current_quantity + df.iloc[row_to_check]['Quantity'] <= MAX_QUANTITY:
        current_batch.append(df.iloc[row_to_check]['Document No.'])
        invoices_remaining -= 1
        current_quantity += df.iloc[row_to_check]['Quantity']
    else:
        # add edited batch to all_batches
        invoices_remaining -=1
        all_batches.append(current_batch)
        current_batch = []
        current_quantity = 0

print(all_batches)
for batch in all_batches:
    print(len(batch))
        

# Apply Pathing on Group of Items
