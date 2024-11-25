from pydantic import BaseModel
from typing import List

class OrderItemRequest(BaseModel):
    product_sku: str
    quantity: int
    unit_price: float
    product_name: str

class OrderRequest(BaseModel):
    customer_name: str
    address: str
    items: List[OrderItemRequest]
