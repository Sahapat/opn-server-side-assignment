from typing import Optional
from datetime import date
from pydantic import BaseModel
from enum import Enum

class GenderEnum(str, Enum):
    Male = 'male'
    Female = 'female'
    NotSpecify = 'none'

class Member(BaseModel):
    id: str
    name: str
    password: str
    email: str
    gender: GenderEnum
    date_of_birth: date
    is_subscribe_to_news_sletter: bool
    address_id: Optional[str] = None
