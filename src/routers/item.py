from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.item import Item
from src.schemas.item import Item as ItemCreate, ItemOrm

from src.db import get_db

router = APIRouter()


@router.post("/items", response_model=ItemOrm)
async def create_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    """
    Itemを一件Insertするためのエンドポイント
    """

    item = Item(**item_data.dict())
    # データの追加
    db.add(item)
    # データの登録
    db.commit()
    # 一時データのリフレッシュ
    db.refresh(item)
    return item

@router.post("/item_list", response_model=List[ItemOrm])
async def create_item_list(item_data_list: List[ItemCreate], db: Session = Depends(get_db)):
    """
    複数まとめてItemをInsertするためのエンドポイント
    """

    item_list = [Item(
        name=item.name,
        description=item.description,
        ) for item in item_data_list]
    db.add_all(item_list)
    db.commit()
    return item_list


@router.get("/items", response_model=List[ItemOrm])
async def get_items(db: Session = Depends(get_db)):
    """
    Itemを全件取得するためのエンドポイント
    """
    
    items = db.scalars(select(Item)).all()
    """
    もしくは以下のように記載してもOk。
    items = db.execute(select(Item)).scalars().all()
    """
    return items


@router.get("/items/{item_id}", response_model=ItemOrm)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    ID指定したItemを取得するエンドポイント
    """

    item = db.scalars(select(Item).where(Item.id == item_id)).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item