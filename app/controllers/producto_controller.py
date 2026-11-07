from fastapi import APIRouter, HTTPException, Query, status

from app.db.database import SessionDep
from app.dependencies.auth import CurrentUser
from app.schemas.producto import ProductoCreate
from app.services import producto_service


router = APIRouter(tags=["Productos"])

@router.get("/productos")
def obtener_productos(
    current_user: CurrentUser,
    session: SessionDep
):
    return producto_service.obtener_productos(
        current_user.id,
        session
    )


@router.post(
    "/productos",
    status_code=status.HTTP_201_CREATED
)
def crear_producto(
    data: ProductoCreate,
    current_user: CurrentUser,
    session: SessionDep
):
    return producto_service.crear_producto(
        data,
        current_user.id,
        session
    )


@router.get("/productos/{id_producto}")
def obtener_producto(
    id_producto: int,
    current_user: CurrentUser,
    session: SessionDep
):
    producto = producto_service.obtener_producto(
        id_producto,
        current_user.id,
        session
    )

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return producto

