from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from db.database import crear_tablas
from controller.producto_controller import router as producto_router
from controller.auth_controller import router as auth_router

app = FastAPI(lifespan=crear_tablas)


@app.exception_handler(RequestValidationError)
async def error_de_datos(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Revisa los datos. Faltan campos o algún valor no es válido."
        }
    )

app.include_router(producto_router)
app.include_router(auth_router)

app.mount("/", StaticFiles(directory="frontend"), name="paginas")
