from pydantic import BaseModel
from .config import Config
from bson.objectid import ObjectId

class Product(BaseModel):
    id: str
    name: str
    price: int

    @staticmethod
    def create(name:str, price: float):
        product = Product(
            id=f'Product-'+str(ObjectId()),
            name=name,
            price=int(price * Config().precision)
        ) 
        return product
    