from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL
)

def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def obtener_sesion():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(obtener_sesion)]