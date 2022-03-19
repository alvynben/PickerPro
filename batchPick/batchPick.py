import pandas
import pathlib
import json

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
FILE_NAME = 'df_lines.csv'
SPECIFIED_DATE = '12/13/2018'

df = pandas.read_csv(f"{CURRENT_DIRECTORY}/{FILE_NAME}")

# Split all orders into groups by their date
listOfDates = df["DATE"].unique()
ordersToDate = {}
for date in listOfDates:
    ordersToDate[date] = df[df["DATE"] == date]

# Split all orders in SPECIFIED_DATE into a list of invoices
day = ordersToDate[SPECIFIED_DATE]
listOfInvoices = []
for orderNumber in day["OrderNumber"].unique():
    orders = day[day["OrderNumber"] == orderNumber]
    invoice = {}
    invoice["OrderNumber"] = orderNumber
    invoice["items"] = []
    for index,order in orders.iterrows():
        item = {}
        item["SKU"] = order["SKU"]
        item["PCS"] = order["PCS"]
        item["Alley_Number"] = order["Alley_Number"]
        item["Cellule"] = order["Cellule"]
        item["Coord"] = order["Coord"]
        item["AlleyCell"] = order["AlleyCell"]
        invoice["items"].append(item)
    listOfInvoices.append(invoice)

# To display format of how invoices are stored using pretty printed JSON
# print(json.dumps(json.loads(str(listOfInvoices).replace("\'", "\"")), indent=2))
    


