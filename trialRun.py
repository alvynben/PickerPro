import pandas as pd
import numpy as np
import datetime as dt
import random as rand
from collections import Counter
import itertools
from ast import literal_eval
import statistics
import matplotlib.pyplot as plt
from batchPick.utils.parse import inventory
from batchPick.utils.parse import map as warehouseMap
from batchPick.types.typing import MemberOfBatch, Location, OrderDetail
from typing import List
from findPath import findPath

# Constants
CSV_FILE_NAME = "batchPick/trainingData/trial_data.csv"


# Utils
def get_unique_count(df: pd.DataFrame, col_name: pd.Index):
    return len(df[col_name].unique())


# Extract Data
df = pd.read_csv(CSV_FILE_NAME)

# Transform Data
invoice_to_weight = pd.DataFrame(df, columns=["Document No.", "Quantity"]).groupby(
    "Document No."
)

# Apply Knapsack Algorithm on Invoices
total_no_of_orders: int = len(df.index)
orders_remaining: int = total_no_of_orders
MAX_QUANTITY = 48
current_quantity = 0
current_batch: List[MemberOfBatch] = []
all_batches: List[List[MemberOfBatch]] = []
prev_invoice = df.iloc[0]["Document No."]

while orders_remaining or current_batch:
    if not orders_remaining:
        all_batches.append(current_batch)
        current_batch = []
        current_quantity = 0
        break

    row_to_check = total_no_of_orders - orders_remaining
    current_invoice = df.iloc[row_to_check]["Document No."]
    bound_to_overflow = False
    if current_invoice != prev_invoice:
        bound_to_overflow = (
            current_quantity
            + invoice_to_weight.get_group(current_invoice).sum()["Quantity"]
            > MAX_QUANTITY
        )

    if not bound_to_overflow:
        current_batch.append(
            {
                "sku_no": df.iloc[row_to_check]["No."],
                "quantity": df.iloc[row_to_check]["Quantity"],
            }
        )
        prev_invoice = current_invoice
        orders_remaining -= 1
        current_quantity += df.iloc[row_to_check]["Quantity"]
    else:
        # add edited batch to all_batches
        all_batches.append(current_batch)
        current_batch = []
        current_quantity = 0

# Apply Pathing on Group of Orders
all_locs: List[Location] = []
for batch in all_batches:
    locs = list(
        map(
            lambda x: {
                "coord": warehouseMap.get_coordinates(
                    inventory.get_item_location(x["sku_no"])
                ),
                "quantity": x["quantity"],
            },
            batch,
        )
    )
    batch = list(map(lambda x: inventory.get_item_location(x["sku_no"]), batch))
    all_locs.append(locs)

all_locs = [
    [
        {"coord": (8, 71), "qty": 2},
        {"coord": (12, 59), "qty": 1},
        {"coord": (5, 25), "qty": 3},
        {"coord": (6, 8), "qty": 2},
        {"coord": (14, 12), "qty": 1},
        {"coord": (16, 25), "qty": 1},
        {"coord": (17, 61), "qty": 2},
    ],
    [
        {"coord": (15, 13), "qty": 12},
        {"coord": (17, 29), "qty": 1},
        {"coord": (7, 13), "qty": 4},
    ],
    [
        {"coord": (16, 61), "qty": 2},
        {"coord": (12, 59), "qty": 2},
        {"coord": (13, 43), "qty": 3},
        {"coord": (5, 0), "qty": 1},
        {"coord": (6, 0), "qty": 1},
        {"coord": (14, 59), "qty": 2},
        {"coord": (2, 17), "qty": 1},
        {"coord": (14, 59), "qty": 1},
        {"coord": (14, 12), "qty": 1},
        {"coord": (11, 60), "qty": 2},
    ],
    [{"coord": (8, 76), "qty": 24}],
]
all_batches = [
    [
        "ZZASAF50GM",
        "ZZBGF1KG",
        "ZZRF600GM",
        "SAPUFCM1LTR",
        "ZZBFCLD3LTR",
        "ZZFSH1KG",
        "ZZSTP500GM",
    ],
    ["ZZKNCSBL480GM", "ZZKAPHPS6KG", "ZZMGCCS1200GM"],
    [
        "ZZCHP250GM",
        "ZZUDS1KG",
        "SPTCIO1880GM",
        "ZZNFBL3400ML",
        "ZZNFDWL5LTR",
        "DZRCD500GM",
        "MGMP3KG",
        "DZCORP500GM",
        "ZZBFCLD3LTR",
        "YWBRPUP1KG",
    ],
    ["ZZBSH2250GM"],
]

# Get all order ids in order
orders = []
for i in range(len(all_locs)):
    order_coords_idx = findPath.findPath(
        [loc["coord"] for loc in (all_locs[i])], warehouseMap.map
    )
    order_details: List[OrderDetail] = []
    for coord_idx in order_coords_idx:
        order_details.append(
            {"sku_no": all_batches[i][coord_idx], "quantity": all_locs[i][coord_idx]["qty"]}
        )
    orders.append(order_details)

# Get each order's item details
for order in orders:
    order_data = []
    for item in order:
        sku = inventory.find_item(item["sku_no"])
        order_data.append(
            [
                sku.bin_location,
                sku.id_no,
                sku.desc,
                sku.packing_size,
                sku.unit_of_measurement,
                item["quantity"],
            ]
        )
    df = pd.DataFrame(
        order_data, columns=["Bin", "No.", "Description", "Packing Size", "UOM", "Qty"]
    )
    print(df, "\n")
