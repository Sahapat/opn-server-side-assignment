from pydantic import BaseModel
from bson.objectid import ObjectId

class Customer(BaseModel):
    id: str
    name: str

    @staticmethod
    def create(name: str):
        customer = Customer(
            id=f'Customer-'+str(ObjectId()),
            name=name
        )
        return customer