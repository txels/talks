from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


items_db = []
app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return items_db[skip : skip + limit]


@app.post("/items/")
async def create_item(item: Item):
    items_db.append(item)
    return item
