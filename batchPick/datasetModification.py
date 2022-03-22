import pandas as pd
import pathlib
import random


CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
FILE_NAME = 'df_lines.csv'

df = pd.read_csv(f"{CURRENT_DIRECTORY}/{FILE_NAME}")

# extract unique SKU and store in dictionary
SKUtoDate = {}
listOfSKU = df['SKU'].unique()
for SKU in range(len(listOfSKU)):
    itemDetails = dict()
    itemDetails['referenceID'] = df.loc[df['SKU'] == listOfSKU[SKU], 'ReferenceID'].values[0]
    itemDetails['location'] = df.loc[df['SKU'] == listOfSKU[SKU], 'Location'].values[0]
    itemDetails['alley_no'] = df.loc[df['SKU'] == listOfSKU[SKU], 'Alley_Number'].values[0]
    itemDetails['cellule'] = df.loc[df['SKU'] == listOfSKU[SKU], 'Cellule'].values[0]
    itemDetails['coordinates'] = df.loc[df['SKU'] == listOfSKU[SKU], 'Coord'].values[0]
    itemDetails['alley_cell'] = df.loc[df['SKU'] == listOfSKU[SKU], 'AlleyCell'].values[0]
    SKUtoDate[listOfSKU[SKU]] = itemDetails


def Insert_row(row_number, df, row_value):
    start_upper = 0
    end_upper = row_number
    start_lower = row_number
    end_lower = df.shape[0]
    upper_half = [*range(start_upper, end_upper, 1)]
    lower_half = [*range(start_lower, end_lower, 1)]
    lower_half = [x.__add__(1) for x in lower_half]
    index_ = upper_half + lower_half
    df.index = index_
    df.loc[row_number] = row_value
    df = df.sort_index()
    return df

#adding artificial data
rangeValues = 3
counter = 1
for row in range(len(df.index)):
    case = random.randint(1, 4)
    if case == 1 or case == 2 or case == 4:
        pass
    else:
        iteration = random.randint(2, rangeValues)
        for newrow in range(iteration):
            temp = row
            orderNo,Date = df['OrderNumber'].iloc[temp],df['DATE'].iloc[temp]
            SKUInput = listOfSKU[random.randint(1,len(listOfSKU)-1)]
            Pcs = random.randint(1,2)
            rowValue = [counter,Date,orderNo,SKUInput,Pcs,SKUtoDate[SKUInput]['referenceID'],SKUtoDate[SKUInput]['location'],
                            SKUtoDate[SKUInput]['alley_no'],SKUtoDate[SKUInput]['cellule'],
                            SKUtoDate[SKUInput]['coordinates'],SKUtoDate[SKUInput]['alley_cell']]
            if temp > df.index.max() + 1:
                pass
            else:
                df = Insert_row(temp, df, rowValue)
            temp += 1
    counter += 1

df.to_csv('newdf_lines.csv',columns=['S/N', 'DATE', 'OrderNumber', 'SKU','PCS','ReferenceID','Location','Alley_Number','Cellule',
                                     'Coord','AlleyCell'])
print("Generated")



