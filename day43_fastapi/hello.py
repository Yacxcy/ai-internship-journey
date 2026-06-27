from fastapi import FastAPI
from pydantic import BaseModel

class CreateItem(BaseModel):
    name:str
    price:float


app = FastAPI(title = "Hello API")
@app.get("/")
def root():
    return {"hello":"world"}


@app.get("/items/{item_id}")
def get_item(item_id:int,q:str= None):
    return {"item_id":item_id,"q":q}


@app.post("/items/")
def create_item(item:CreateItem):
    return {"created":item.model_dump()}