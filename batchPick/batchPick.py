from turtle import delay
from typing import List
import pandas as pd
import pathlib
import json
import itertools
from ast import literal_eval
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnchoredText
from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image
import numpy as np
from parse import map

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
FILE_NAME = 'df_lines.csv'
SPECIFIED_DATE = '12/13/2018'
BATCHING = True

if BATCHING:
    IMAGE_NAME = "picker.png"
    ROUTES_FILE = "batchRoutes"
    LOCS_FILE = "batchLocs"
else:
    IMAGE_NAME = "picker.png"
    ROUTES_FILE = "singleRoutes"
    LOCS_FILE = "singleLocs"

df = pd.read_csv(f"{CURRENT_DIRECTORY}/{FILE_NAME}")
picker = Image.open(f"{CURRENT_DIRECTORY}/picker.png")
width, height = picker.size
picker = picker.resize((width // 25, height // 25))
# Run algo based on parameteIf True, resize the figure to match the given image size.
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


# x = np.array(all_x)
# y = np.array(all_y)
# sizes = np.random.uniform(15, 80, len(x))
# colors = np.random.uniform(15, 80, len(x))
# ax.scatter(x,y,s=sizes, c=colors,vmin=0,vmax=100)

def drawOccupancyGrid(mapData: List[List[int]]):
    pass

for i in range(7167):
    fig, ax = plt.subplots(figsize=(20,20))
    fig.set_facecolor("yellow")
    line1, line2, line3 = [0,0,0]
    ax.set(xlim=(0, 150), xticks=[],
        ylim=(0, 150), yticks=[])
    ax.imshow(map.map)

    # TODO: Draw new warehouses
    # for a,b in [(13.25,15.25), (17.5, 19.5), (20.75, 22.75), (24,26), (28,30), (32.5,34.5),(35.75,37.75),(39.0,41.0),(42.25,44.25),(45.5,47.5),(48.75,50.75),(52.0,54.0) ]:
    #     x = np.array([a,a,b,b,a])
    #     y = np.array([6.0,23.0,23.0,6.0,6.0])

    #     line1 = ax.step(x, y, linewidth=2.5, color='black',zorder=1)
    #     ax.fill(x,y,'white',zorder=0)

    f = open(f"{CURRENT_DIRECTORY}/{LOCS_FILE}{i}.txt","r")
    lines = f.read().splitlines()
    batch_routes = []
    new_x = []
    new_y = []
    for line in lines:
        lineSplit = line.split(",")
        new_x.append(float(lineSplit[0]))
        new_y.append(float(lineSplit[1]))
    f.close()
    x = np.array(new_x)
    y = np.array(new_y)
    sizes = np.random.uniform(15, 80, len(x))
    colors = np.random.uniform(15, 80, len(x))
    line2 = ax.scatter(x,y,s=sizes, c=colors,vmin=0,vmax=150)

    f = open(f"{CURRENT_DIRECTORY}/{ROUTES_FILE}{i}.txt","r")
    lines = f.read().splitlines()
    batch_routes = []
    prevX = -1
    prevY = -1
    for line in lines:
        lineSplit = line.split(",")
        if min(abs(prevX - float(lineSplit[0])), abs(prevY - float(lineSplit[1]))) == 0:
            continue
        batch_routes.append([float(lineSplit[0]), float(lineSplit[1])])
        prevX, prevY = float(lineSplit[0]), float(lineSplit[1])
    f.close()

    rn = AnchoredText(f"PBatch No: {i}", prop=dict(size=15), frameon=True, loc='upper right')
    rn.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    rn.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(rn)


    

    plt.axis('off')

    legend_elements = [Line2D([0], [0], color='black', lw=4, label='Shelf'),
                    Line2D([0], [0], marker='o', color='w', label='Item to Pick',
                            markerfacecolor='g', markersize=15),
                    Line2D([0], [0], color='red', lw=4, label='Route Taken')]
    ax.legend(handles=legend_elements)

    count = 0
    for i in range(1,len(batch_routes)):
        start = batch_routes[i - 1]
        end = batch_routes[i]

        # x = np.array([start[0], end[0]])
        # y = np.array([start[1], end[1]])
        # line3 = ax.step(x, y, linewidth = 1, color="red")
        at = 0
        x,y = start
        dx,dy = end[0] - x, end[1] - y
        noOfFrames = int(max(abs(dx),abs(dy)))
        for j in range(1,noOfFrames + 1):
            line3 = ax.arrow(x, y, j * dx / noOfFrames, j * dy / noOfFrames, color="red", linewidth=3.5, head_width=0.3, length_includes_head=True)
            # im1 = fig.figimage(picker, xo=x+(j * dx / noOfFrames) * fig., yo=y+(j * dy / noOfFrames), origin="lower")
            im1 = plt.imshow(picker,extent=[x+(j * dx / noOfFrames),x+(j * dx / noOfFrames)+2,y+(j * dy / noOfFrames),y+(j * dy / noOfFrames)+2])
            if (j == noOfFrames) and (y + dy != 5.5):
                if at:
                    at.remove()
                count += 1
                at = AnchoredText(f"Packages collected: {count}", prop=dict(size=15), frameon=True, loc='upper left')
                at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
                at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
                ax.add_artist(at)
            plt.pause(0.05)
            line3.remove()
            im1.remove()

    for i in range(1,len(batch_routes)):
        start = batch_routes[i - 1]
        end = batch_routes[i]
        x,y = start
        dx,dy = end[0] - x, end[1] - y
        line3 = ax.arrow(x, y, dx, dy, color="red", linewidth=3.5, head_width=0.3, length_includes_head=True)
    
    rn.remove()


    plt.show(block=False)
    plt.close()
    


