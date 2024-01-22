from typing import Dict
from pydantic import BaseModel
from enum import Enum

class PromotionTypeEnum(str, Enum):
    Discount = 'discount',
    Freebie = 'freebie'

class Promotion(BaseModel):
    type: PromotionTypeEnum
    attribute: Dict
