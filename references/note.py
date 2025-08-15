# models/item_model.py
from pydantic import BaseModel, Field

class Item(BaseModel):
    id: int = Field(...)
    name: str = Field(...)



# app/router.py
from fastapi import APIRouter

router = APIRouter()
@router.get("",response_model=Item)
def get_item(item Item):
    ...


# main.py
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)




