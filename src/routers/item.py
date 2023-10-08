from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.item import Item

from src.db import get_db

router = APIRouter()


@router.post("/items", response_model=Item)
async def create_item(item_data: Item, db: Session = Depends(get_db)):
    item = Item(**item_data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item