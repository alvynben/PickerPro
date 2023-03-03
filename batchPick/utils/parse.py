# The following code will work iff the csv format is the same as Yong Wen's

import pandas as pd
import pathlib
from typing import List, Tuple, Union, Dict

MAP_FILE_NAME = "yw_data_map.csv"
ITEM_INVENTORY_FILE_NAME = "yw_data_item.csv"
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()


class Item:
    def __init__(self, bin_location: str, id_no: str, desc: str, packing_size: str, unit_of_measurement: str):
        self.bin_location = bin_location
        self.id_no = id_no
        self.desc = desc
        self.packing_size = packing_size
        self.unit_of_measurement = unit_of_measurement


class Inventory:
    def __init__(self):
        self.item_list: List[Item] = []
        self.item_info_map: Dict[str, Item] = {}

    def add_item(self, item: Item) -> None:
        self.item_list.append(item)
        self.item_info_map[item.id_no] = item

    def remove_item(self, id_no: str) -> None:
        item: Union[Item, None] = self.item_info_map.get(id_no)
        if item is not None:
            self.item_list.remove(item)
            del self.item_info_map[id_no]

    def find_item(self, id_no: str) -> Union[Item, None]:
        return self.item_info_map.get(id_no)

    def get_item_location(self, id_no: str) -> Union[str, None]:
        item: Union[Item, None] = self.item_info_map.get(id_no)
        if item is not None:
            return item.bin_location

    def get_item_bin_location_map(self) -> Dict[str, str]:
        item_bin_location_map = {}
        for i in self.item_list:
            item_bin_location_map[i.id_no] = i.bin_location
        return item_bin_location_map

    def get_all_items_in_bin_location(self, bin_location: str) -> List[Item]:
        return list(filter(lambda item: item.bin_location is bin_location, self.item_list))


class Map:
    def __init__(self):
        self.map: List[List[int]] = []
        self.bin_location_coordinates_map: Dict[str, Tuple[int, int]] = {}

    # This function need to be called in-order of the csv file line
    # Note: seems to not register the first csv row (it gets skipped)
    def build_map(self, csv_line: pd.Series, row_number: int):
        new_row = []
        for index, i in enumerate(csv_line):
            if type(i) is str:  # type str means it's not an empty cell, so there is a bin
                self.bin_location_coordinates_map[i] = (index, row_number)
                new_row.append(0)
            else:
                new_row.append(1)
        self.map.append(new_row)

    def get_coordinates(self, bin_location: str) -> Union[Tuple[int, int], None]:
        return self.bin_location_coordinates_map.get(bin_location)


def parseItemInventoryCSV() -> Inventory:
    print(ITEM_INVENTORY_FILE_NAME)
    df = pd.read_csv(f"{CURRENT_DIRECTORY}/{ITEM_INVENTORY_FILE_NAME}")
    inventory: Inventory = Inventory()
    for index, item in df.iterrows():
        new_item: Item = Item(
            item["Bin."], item["No."], item["Description"], item["Packing Size"], item["UOM"])
        inventory.add_item(new_item)
    return inventory


def parseMapCSV() -> Map:
    df = pd.read_csv(f"{CURRENT_DIRECTORY}/{MAP_FILE_NAME}")
    map: Map = Map()
    for index, item in df.iterrows():
        map.build_map(item, index)
    return map


inventory: Inventory = parseItemInventoryCSV()
map: Map = parseMapCSV()
