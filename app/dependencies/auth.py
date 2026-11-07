
import jwt

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from app.db.database import SessionDep
from app.core.config import SECRET_KEY, ALGORITHM
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obtener_usuario_actual(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep
):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la autenticación",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        if username is None:
            raise error

    except jwt.InvalidTokenError:
        raise error

    usuario = session.exec(
        select(Usuario).where(Usuario.username == username)
    ).first()

    if usuario is None:
        raise error

    return usuario


CurrentUser = Annotated[Usuario, Depends(obtener_usuario_actual)]
