from fastapi import APIRouter, HTTPException, status

from db.database import SessionDep
from dependencies.auth import CurrentUser
from schemas.producto import ProductoCreate, ProductoRead
from services import producto_service

router = APIRouter(tags=["Productos"], prefix="/productos")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductoRead)
def crear_producto(
    data: ProductoCreate,
    current_user: CurrentUser,
    session: SessionDep
):
    return producto_service.crear_producto(data, session)


@router.get("/", response_model=list[ProductoRead])
def obtener_productos(
    current_user: CurrentUser,
    session: SessionDep
):
    return producto_service.obtener_productos(session)


@router.get("/{id_producto}", response_model=ProductoRead)
def obtener_producto(
    id_producto: int,
    current_user: CurrentUser,
    session: SessionDep
):
    producto = producto_service.obtener_producto(id_producto, session)

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return producto


@router.put("/{id_producto}", response_model=ProductoRead)
def actualizar_producto(
    id_producto: int,
    data: ProductoCreate,
    current_user: CurrentUser,
    session: SessionDep
):
    producto = producto_service.actualizar_producto(
        id_producto,
        data,
        session
    )

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return producto


@router.delete("/{id_producto}")
def eliminar_producto(
    id_producto: int,
    current_user: CurrentUser,
    session: SessionDep
):
    eliminado = producto_service.eliminar_producto(id_producto, session)

    if eliminado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return {"mensaje": "Producto eliminado correctamente"}
