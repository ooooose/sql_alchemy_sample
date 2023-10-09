from datetime import datetime
from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(None, example='ふしぎなアメ')
    description: str = Field(None, example='食べるとレベルが１アップする')

class Item(ItemBase):
    pass

class ItemOrm(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True