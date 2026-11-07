from sqlmodel import SQLModel, Field


class UsuarioCreate(SQLModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(max_length=100)
    password: str = Field(min_length=8)


class UsuarioLogin(SQLModel):
    username: str
    password: str


class UsuarioPublic(SQLModel):
    id: int
    username: str
    email: str


class Token(SQLModel):
    access_token: str
    token_type: str
