from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.item import Item
from src.schemas.item import Item as ItemCreate, ItemOrm

from src.db import get_db

router = APIRouter()


@router.post("/items", response_model=ItemOrm)
async def create_item(item_data: ItemCreate, db: Session = Depends(get_db)) -> ItemOrm:
    item = Item(**item_data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/items", response_model=List[ItemOrm])
async def get_items(db: Session = Depends(get_db)) -> List[ItemOrm]:
    items = db.scalars(select(Item)).all()
    return items


@router.get("/items/{item_id}", response_model=ItemOrm)
async def get_item(item_id: int, db: Session = Depends(get_db)) -> ItemOrm:
    item = db.scalars(select(Item).where(Item.id == item_id)).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item