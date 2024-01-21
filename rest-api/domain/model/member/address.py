from pydantic import BaseModel

class MemberAddress(BaseModel):
    id: str
    member_id: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
