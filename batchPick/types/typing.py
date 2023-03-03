from typing import TypedDict, Tuple

class MemberOfBatch(TypedDict):
    sku_no: str
    quantity: int

class Location(TypedDict):
    coord: Tuple
    quantity: int

class OrderDetail(TypedDict):
    sku_no: str
    quantity: int