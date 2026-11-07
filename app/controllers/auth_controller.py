from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import SessionDep
from app.schemas.usuario import UsuarioCreate, Token
from app.services import usuario_service
from app.core.security import crear_token

router = APIRouter(tags=["Auth"], prefix="/auth")

@router.post("/register")
def registrar(data: UsuarioCreate, session: SessionDep):
    usuario = usuario_service.registrar_usuario(data, session)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario ya existe"
        )

    return usuario

@router.post("/login", response_model=Token)
def login(
    data: UsuarioCreate,
    session: SessionDep
):
    usuario = usuario_service.autenticar_usuario(
        data.username,
        data.password,
        session
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = crear_token({"sub": usuario.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }