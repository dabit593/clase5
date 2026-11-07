from sqlmodel import select

from models.producto import Producto
from schemas.producto import ProductoCreate


def obtener_productos(session):
    consulta = select(Producto)
    return session.exec(consulta).all()


def obtener_producto(id_producto: int, session):
    return session.exec(
        select(Producto).where(Producto.id == id_producto)
    ).first()


def crear_producto(data: ProductoCreate, session):
    producto = Producto(**data.model_dump())

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return producto


def actualizar_producto(id_producto: int, data: ProductoCreate, session):
    producto = obtener_producto(id_producto, session)

    if producto is None:
        return None

    producto.nombre = data.nombre
    producto.descripcion = data.descripcion
    producto.precio = data.precio
    producto.stock = data.stock

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return producto


def eliminar_producto(id_producto: int, session):
    producto = obtener_producto(id_producto, session)

    if producto is None:
        return None

    session.delete(producto)
    session.commit()

    return producto
