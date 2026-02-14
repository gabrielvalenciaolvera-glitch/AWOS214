#Importaciones
from fastapi import FastAPI, status, HTTPException
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
@app.get("/v1/parametroOb/{id}",tags=["Parametro Obligatorio"])
async def consultaUno(id:int):
    return{"se encontro usuario": id}

@app.get("/v1/parametroOp/",tags=["Parametro Opcional"])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje":"Usuario encontrado","usuario":usuario}
        return{"mensaje":"usuario no encontrado","usuario":id}
    else:
        return{"mensaje":"No se proporciono id"}   

@app.get("/v1/usuarios/",tags=["CRUD HTTP"])
async def leer_usuarios():
    return{
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
    }



@app.post("/v1/usuarios/",tags=["CRUD HTTP"],status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return  {
        "mensaje":"Usuario Agregado",
        "Usuario":usuario
        
    }

@app.put("/v1/usuarios/",tags=["CRUD HTTP"],status_code=status.HTTP_204_NO_CONTENT)
async def Actualizar_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usuarios.append(usuario)
            return{
                "mensaje":"usuario Actualizado",
                "Usuario":usuario
            }
        raise HTTPException(
            status_code=400,
            detail="El id no existe"
        )   
    
@app.delete("/v1/usuarios/",tags=["CRUD HTTP"])
async def Eliminar_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usuarios.pop(usuario)
            return{
                "mensaje":"usuario Eliminado",
                "Usuario Elminado":usuario
            }
        raise HTTPException(
            status_code=400,
            detail="Id no existente"
        )