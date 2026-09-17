from typing import TypedDict

class Offer(TypedDict):
    quantity: int
    price: int

class Product(TypedDict):
    name: str
    unit_price: int
    offer: Offer | None
