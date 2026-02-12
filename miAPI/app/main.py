#Importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

#Instancia del servidor
app = FastAPI(title="MI primera fukin API",
              description="Gabriel Valencia Olvera, la mejor fukin API",
              version="1.0.0"
              )

#TB ficticia
usuarios=[
    {"id":1,"nombre":"juan","edad":21},
    {"id":2,"nombre":"Pepe","edad":31},
    {"id":3,"nombre":"Diego","edad":21},
]

#Endpoints
@app.get("/",tags=["Inicio"])
async def bienvenida():
    return {"mensaje": "¡Bienvenido a mi API"}


@app.get("/HolaMundo", tags=["Bienvenida Asincrona"])
async def Hola():
    await asyncio.sleep(4)#simulacion de una peticion
    return {"mensaje": "¡Hola Mundo FastAPI!",
            "estatus":"200"
            }      
@app.get("/v1/usuario/{id}",tags=["Parametro Obligatorio"])
async def consultaUno(id:int):
    return{"se encontro usuario": id}

@app.get("/v1/usuarios/",tags=["Parametro Opcional"])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje":"Usuario encontrado","usuario":usuario}
        return{"mensaje":"usuario no encontrado","usuario":id}
    else:
        return{"mensaje":"No se proporciono id"}   


    