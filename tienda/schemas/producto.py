from sqlmodel import SQLModel, Field


class ProductoCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str | None = Field(default=None, max_length=300)
    precio: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)


class ProductoRead(SQLModel):
    id: int
    nombre: str
    descripcion: str | None = None
    precio: float
    stock: int
