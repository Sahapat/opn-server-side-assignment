from bson.objectid import ObjectId
from typing import List, Dict, Tuple
from pydantic import BaseModel
from .promotion import Promotion
from enum import Enum

class CartState(str, Enum):
    created = 'created'
    confirmed = 'confirm'
    cancelled = 'cancelled'

class CartProduct(BaseModel):
    id: str
    product_id: str
    quantity: int

class Cart(BaseModel):
    id: str
    state: CartState
    customer_id: str
    cart_products: List[CartProduct]
    promotions: List[Promotion]

    @staticmethod
    def create(customer_id: str):
        cart = Cart(
            id = f'Cart-'+str(ObjectId()),
            state = CartState.created,
            customer_id=customer_id,
            cart_products={},
            promotions=[]
        )
        return cart

