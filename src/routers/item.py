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

    """
    以下のようにトランザクションを明確に張ることも可能。
    一件の処理では上記で足りるが、複数処理が絡みデータの整合性を担保するために下記のように実装することもある。
    ブロックを抜けると自動的にcloseされたことになり、flush()で一時送信していたデータが保存される。
    
    with db as session:
        item = Item(**item_data.dict())
        print(session)
        session.add(item)
        session.flush()
    """
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

    # 複数取得の場合はscalars()を使用する。
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

    """
    一件取得の場合は、scalar()で取得可能
    以下と同じ結果となる。
    item = db.execute(select(Item).where(Item.id == item_id)).scalar()
    item = db.scalars(select(Item).where(Item.id == item_id)).first()
    """
    item = db.scalar(select(Item).where(Item.id == item_id))
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item