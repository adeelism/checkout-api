from collections import Counter
from app.catalogue import CATALOGUE
from app.types import Product

class UnknownProductError(Exception):
    """Raised when an unknown product code is encountered."""
    pass

# Calculates the total for the coming product list by comparing against the catalogue and applying any bundle offers if applicable
def calculate_total(product_ids: list[str]) -> int:
    quantities = Counter(product_ids)
    for product_id in quantities:
        if product_id not in CATALOGUE:
            raise UnknownProductError(f"Unknown product code: {product_id}")
    total = sum(price_for_quantity(quantity, CATALOGUE[product_id]) for product_id, quantity in quantities.items())    
    return total

# helper function to determine if there is an offer on the product or not an offer on the product and calculate the total price accordingly
def price_for_quantity(quantity: int, product: Product) -> int:
    offer = product["offer"]
    if offer is None:
        return quantity * product["unit_price"]
    bundles = quantity // offer["quantity"]
    remaining_units = quantity % offer["quantity"]
    total_price = bundles * offer["price"] + remaining_units * product["unit_price"]
    return total_price

