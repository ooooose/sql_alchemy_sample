from fastapi import FastAPI
from src.routers import item

app = FastAPI()
app.include_router(item.router)


@app.get("/")
async def home():
    return {"message": "hello sql-alchemy-sample"}
