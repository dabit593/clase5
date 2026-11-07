from sqlmodel import select

from models.usuario import Usuario
from schemas.usuario import UsuarioCreate
from core.security import hash_password, verify_password


def registrar_usuario(data: UsuarioCreate, session):
    usuario_existente = session.exec(
        select(Usuario).where(Usuario.username == data.username)
    ).first()

    if usuario_existente:
        return None

    correo_existente = session.exec(
        select(Usuario).where(Usuario.email == data.email)
    ).first()

    if correo_existente:
        return None

    usuario = Usuario(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password)
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


def autenticar_usuario(username: str, password: str, session):
    usuario = session.exec(
        select(Usuario).where(Usuario.username == username)
    ).first()

    if usuario is None:
        return None

    if not verify_password(password, usuario.hashed_password):
        return None

    return usuario
