from fastapi import FastAPI
from src.routers import item

app = FastAPI()

# itemのルーティングを読み込み
app.include_router(item.router)


@app.get("/")
async def home():
    return {"message": "hello sql-alchemy-sample"}
