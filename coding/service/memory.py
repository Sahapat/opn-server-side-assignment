from typing import Dict
from domain.model import Customer, Cart, Product

class MemoryDb():
    def __init__(self):
        self.customer: Dict[str, Customer] = {}
        self.cart: Dict[str, Cart] = {}
        self.product: Dict[str, Product] = {}

memoryDbDefault = MemoryDb()
