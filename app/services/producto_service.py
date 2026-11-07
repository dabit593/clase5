from sqlmodel import select

from app.models.producto import Producto
from app.schemas.producto import ProductoCreate


def obtener_productos(user_id: int, session):
    consulta = select(Producto).where(
        Producto.user_id == user_id
    )

    return session.exec(consulta).all()


def obtener_producto(id_producto: int, user_id: int, session):
    return session.exec(
        select(Producto).where(
            Producto.id == id_producto,
            Producto.user_id == user_id
        )
    ).first()


def crear_producto(data: ProductoCreate, user_id: int, session):
    producto = Producto(
        **data.model_dump(),
        user_id=user_id
    )

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return producto
