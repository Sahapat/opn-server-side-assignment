from typing import List
from domain.model import Cart as CartModel, CartProduct, CartState
from .exception import ProductNotFound, CustomerNotFound
from .memory import MemoryDb, memoryDbDefault

class Cart:
    def __init__(self, cart: CartModel, memoryDb: MemoryDb):
        self.memoryDb = memoryDb
        self.cart = cart

    @staticmethod
    def create(customer_id: int, db: MemoryDb = None):
        memoryDb = memoryDbDefault if db is None else db
        if memoryDb.customer.get(customer_id, None) is None:
            raise CustomerNotFound(f'Customer id: {customer_id} not found')
        cart = CartModel.create(customer_id=customer_id)
        memoryDb.cart[cart.id] = cart
        return Cart(cart=cart, memoryDb=memoryDb)

    def add(self, product_id: int, quantity: int):
        pass

    def update(self, product_id: int, quantity: int):
        pass

    def has(self, product_id: str):
        pass

    def remove(self, product_id: str):
        pass

    def destroy(self):
        self._cart = self.cart
        self._cart.state = CartState.cancelled
        self.cart = None

    def count(self):
        pass

    def total(self):
        pass

    def addDiscount(self):
        pass

    def removeDiscount(self):
        pass

    def addFreebie(self):
        pass

    def isEmpty(self) -> bool:
        return len(self.cart.cart_products) == 0
    
        
