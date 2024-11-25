from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    address = Column(String, nullable=False)
    total_price = Column(DECIMAL(10, 2), default=0.00)
    status = Column(String(10), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship('OrderItem', back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, index=True)
    product_sku = Column(String(100), nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    
    order = relationship('Order', back_populates='items')
