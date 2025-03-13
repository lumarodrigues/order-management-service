import requests
from sqlalchemy.orm import Session
from oms.models import Order, OrderItem
from oms.schemas import OrderRequest
from fastapi import HTTPException
import sys
import os


def remove_from_stock(product_id, quantity):
    endpoint = f"http://127.0.0.1:8000/api/v1/products/{product_id}/remove-from-stock/"
    data = {
        "quantity": quantity
    }

    try:
        response = requests.patch(endpoint, json=data)
        if response.status_code == 200:
            print(f"Estoque do produto {product_id} removido com sucesso!")
            return True
        elif response.status_code == 400:
            raise HTTPException(status_code=400, detail=f"Error: {response.json()['error']}")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error ao atualizar estoque.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao tentar atualizar estoque.")


async def create_order(order: OrderRequest, db: Session):
    new_order = Order(customer_name=order.customer_name, address=order.address)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    order_items = []

    for item in order.items:
        endpoint = f"http://127.0.0.1:8000/api/v1/products/{item.product_id}/"
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                product = response.json()
                if product['stock'] >= item.quantity:
                    success = remove_from_stock(item.product_id, item.quantity)
                    if success:
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
                        detail=f"Produto {item.product_name} (SKU: {item.product_sku}) - Não há estoque suficiente."
                    )
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Produto não encontrado."
                )
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar produto: {e}")
            raise HTTPException(status_code=500, detail="Erro de comunicação com endpoint.")

    db.add_all(order_items)
    db.commit()

    return {
        "order_id": new_order.id,
        "status": "Pedido criado com sucesso!",
        "items": order.items
    }

def get_orders(db: Session):
    return db.query(Order).all()

def get_order(order_id: int, db: Session):
    return db.query(Order).filter(Order.id == order_id).first()
