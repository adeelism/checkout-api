from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel

from app.pricing import UnknownProductError, calculate_total

app = FastAPI(
    title="Checkout API",
    description="A simple checkout API for calculating total prices with bundle offers.",
    version="1.0.0",
)


class CheckoutResponse(BaseModel):
    price: int


@app.post("/checkout", response_model=CheckoutResponse)
def checkout(product_ids: list[str] = Body(...)):
    try:
        total = calculate_total(product_ids)
    except UnknownProductError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return CheckoutResponse(price=total)
