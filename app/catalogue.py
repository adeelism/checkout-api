from app.types import Product

# Product Catalogue: unit prices and bundle offers
CATALOGUE: dict[str, Product] = {
    "001": {"name": "Silver Label", "unit_price": 100, "offer": {"quantity": 3, "price": 200}},
    "002": {"name": "Gold Label", "unit_price": 80, "offer": {"quantity": 2, "price": 120}},
    "003": {"name": "Platinum Label", "unit_price": 50, "offer": None},
    "004": {"name": "Diamond Label", "unit_price": 50, "offer": None},
}
