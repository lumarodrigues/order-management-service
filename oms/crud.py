from sqlalchemy.orm import Session
from oms.models import Order, OrderItem
from oms.schemas import OrderRequest
from fastapi import HTTPException
from pymongo import MongoClient
import sys
import os


client = MongoClient('mongodb://localhost:27017')
db_nosql = client['ecommerce_db']
product_collection = db_nosql['product']

async def create_order(order: OrderRequest, db: Session):
    new_order = Order(customer_name=order.customer_name, address=order.address)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    order_items = []

    for item in order.items:
        product = product_collection.find_one({"sku": item.product_sku})
        print(f"Produto {item} encontrado")
        print(product)


        if product and product['stock'] >= item.quantity:
            product_collection.update_one(
                {"sku": item.product_sku},
                {"$inc": {"stock": -item.quantity}}
            )

            order_item = OrderItem(
                product_sku=item.product_sku,
                quantity=item.quantity,
                unit_price=item.unit_price,
                product_name=item.product_name,
                order_id=new_order.id
            )

            order_items.append(order_item)

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Product {item.product_name} (SKU: {item.product_sku}) - Not enough stock."
            )

    db.add_all(order_items)
    db.commit()

    return {
        "order_id": new_order.id,
        "status": "Order created successfully!",
        "items": order.items
    }

def get_orders(db: Session):
    return db.query(Order).all()

def get_order(order_id: int, db: Session):
    return db.query(Order).filter(Order.id == order_id).first()
