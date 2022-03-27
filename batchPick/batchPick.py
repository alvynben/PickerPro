import pandas as pd
import pathlib
import json

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
FILE_NAME = 'newdf_lines.csv'
SPECIFIED_DATE = '12/13/2018'

df = pd.read_csv(f"{CURRENT_DIRECTORY}/{FILE_NAME}")

# Split all items into groups by their date
listOfDates = df["DATE"].unique()
datesToItems = {}
for date in listOfDates:
    datesToItems[date] = df[df["DATE"] == date]

# Split all items in SPECIFIED_DATE into a list of invoices
day = datesToItems[SPECIFIED_DATE]
listOfInvoices = []
for orderNumber in day["OrderNumber"].unique():
    items = day[day["OrderNumber"] == orderNumber]
    invoice = {}
    invoice["OrderNumber"] = orderNumber
    invoice["items"] = []
    for index,item in items.iterrows():
        temp_item = {}
        temp_item["SKU"] = item["SKU"]
        temp_item["PCS"] = item["PCS"]
        temp_item["Alley_Number"] = item["Alley_Number"]
        temp_item["Cellule"] = item["Cellule"]
        temp_item["Coord"] = item["Coord"]
        temp_item["AlleyCell"] = item["AlleyCell"]
        temp_item["Size"] = item["Size"]
        invoice["items"].append(temp_item)
    listOfInvoices.append(invoice)

# To display format of how invoices are stored using pretty printed JSON
print(json.dumps(json.loads(str(listOfInvoices).replace("\'", "\"")), indent=2))
    


