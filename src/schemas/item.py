from datetime import datetime
from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(None, example='キーボード')
    description: str = Field(None, example='PCに入力する際に使用するガジェット。')

class Item(ItemBase):
    pass

class ItemOrm(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True