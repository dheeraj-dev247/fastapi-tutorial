from fastapi import FastAPI, Path, Query, Depends, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


TOKEN = "abcd"


def verify_token(x_token: str = Header(...)):

    if x_token != TOKEN:
        raise HTTPException(status_code=401, detail="Token is invalid or not found")
    return {"message": "Access Granted"}


@app.get("/get-token")
def get_token():
    return {"token": TOKEN}


@app.get("/secure-data")
def secure_data(result=Depends(verify_token)):
    return result


class Item(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    description: str = Field(
        default=None, max_length=200, description="This is optional"
    )


@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(..., gt=0, description="Item ID must be greater than zero"),
    q: str | None = Query(None, description="Optional search query"),
):
    return {"item_id": item_id, "q": q}


@app.post("/create-item")
def create_item(item: Item):
    return {"message": "Item created successfully", "data": Item}
