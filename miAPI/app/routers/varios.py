

import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter

router = APIRouter(tags=["Varios"])




#Endpoints
@router.get("/")
async def bienvenida():
    return {"mensaje": "¡Bienvenido a mi API"}


@router.get("/HolaMundo")
async def Hola():
    await asyncio.sleep(4)#simulacion de una peticion
    return {"mensaje": "¡Hola Mundo FastAPI!",
            "estatus":"200"
            }      
@router.get("/v1/parametroOb/{id}")
async def consultaUno(id:int):
    return{"se encontro usuario": id}

@router.get("/v1/parametroOp/")
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje":"Usuario encontrado","usuario":usuario}
        return{"mensaje":"usuario no encontrado","usuario":id}
    else:
        return{"mensaje":"No se proporciono id"}   



