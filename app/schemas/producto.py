from sqlmodel import SQLModel

class ProductoCreate(SQLModel):
    name: str
    description: str
    price: float
    stock:int