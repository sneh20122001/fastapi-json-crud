from fastapi import FastAPI, HTTPException
from typing import List
from models import Item, ItemResponse
from utils import read_data, write_data, get_next_id 

app = FastAPI(
    title = "FastAPI JSON CRUD",
    description = "A simple FastAPI application for performing CRUD operations on JSON data.",
    version = "1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI JSON CRUD application!"}


###################### Create ######################
@app.post("/items/", response_model=ItemResponse, status_code=201)
def create_item(item: Item):
    data = read_data()

    new_item = item.dict()
    new_item['id'] = get_next_id(data)

    data.append(new_item)
    write_data(data)

    return new_item

###################### Read ######################
@app.get("/items/",response_model=List[ItemResponse])
def read_items():
    return read_data()

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int):

    data = read_data()
    for item in data:
        if item['id'] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

###################### Update ######################
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: Item):
    data = read_data()

    for index, existing_item in enumerate(data):
        if existing_item['id'] == item_id:
            data[index]["name"] = item.name
            data[index]["description"] = item.description
            data[index]["price"] = item.price

            write_data(data)
            return data[index]
        
    raise HTTPException(status_code=404, detail="Item not found")

###################### Delete ######################
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    data = read_data()

    for index, existing_item in enumerate(data):
        if existing_item['id'] == item_id:
            deleted_item = data.pop(index)
            write_data(data)
            return {"message": "Item deleted", "item": deleted_item}
        
    raise HTTPException(status_code=404, detail="Item not found")