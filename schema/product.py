from pydantic import BaseModel, Field
from typing import Annotated
from uuid import UUID

class Product(BaseModel):
    id:UUID
    sku: Annotated[ str , Field(min_length=3, max_length=36 , title="SKU", description="Stocks keeping unit", examples=["74-etuori-3d"])]
    name: str