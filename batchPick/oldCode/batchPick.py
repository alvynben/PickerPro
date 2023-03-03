import pandas as pd
import pathlib
import json
import itertools
from ast import literal_eval
import matplotlib.pyplot as plt
import numpy as np

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
FILE_NAME = 'newdf_lines.csv'
SPECIFIED_DATE = '12/13/2018'

df = pd.read_csv(f"{CURRENT_DIRECTORY}/{FILE_NAME}")
# Run algo based on paramete
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
# print(json.dumps(json.loads(str(listOfInvoices).replace("\'", "\"")), indent=2))

list_locs = list(df['Coord'].apply(lambda t: literal_eval(t)).values)
list_locs.sort()
# List of unique coordinates
max_x = 0
max_y = 0
all_x = []
all_y = []
for k,_ in itertools.groupby(list_locs):
    # print(k)
    all_x.append(k[0])
    all_y.append(k[1])
    if k[0] > max_x:
        max_x = k[0]
    if k[1] > max_y:
        max_y = k[0]

# print(max_x, max_y) # x = 52, y = 22.75

# plt.style.use('_mpl-gallery')

fig, ax = plt.subplots()

for a,b in [(15.25,16.5), (19.5,20.75), (22.75,24), (26,28), (29.25, 31.25), (32.5,34.5),(35.75,37.75),(39.0,41.0),(42.25,44.25),(45.5,47.5),(48.75,50.75),(52.0,54.0) ]:
    x = np.array([a,a,b,b,a])
    y = np.array([6.0,23.0,23.0,6.0,6.0])

    ax.step(x, y, linewidth=2.5)

x = np.array(all_x)
y = np.array(all_y)
sizes = np.random.uniform(15, 80, len(x))
colors = np.random.uniform(15, 80, len(x))
ax.scatter(x,y,s=sizes, c=colors,vmin=0,vmax=100)



ax.set(xlim=(10, 60), xticks=np.arange(10, 60),
       ylim=(5, 25), yticks=np.arange(5, 25))

plt.show()
    


