#Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
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


#modelo de validacion pydantic

class usuario_create(BaseModel):
    id: int = Field(..., gt=0, description="Identificador")
    nombre: str = Field(..., min_length=3, max_length=50, example="Gabriel")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")




#segudirdad HTTP Basic

security= HTTPBasic()

def verificar_Peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "Gabriel")
    passAuth = secrets.compare_digest(credenciales.password, "123456")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no Autorizadas"
        )
    return credenciales.username



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
async def leer_usuarios ():
    return{
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
    }


@app.post("/V1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:usuario_create):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje": "Usuario agregado",
        "usuario": usuario
    }


@app.put("/V1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def actualizar_usuario(id:int, usuario_actualizado:dict):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuario.update(usuario_actualizado)
            return{
                "mensaje": "Usuario actualizado",
                "usuario": usuario
            }
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )

@app.delete("/V1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, userAuth:str= Depends(verificar_Peticion)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return{
                "mensaje": f"Usuario eliminado correctamente por: {userAuth}",
                "usuario": usuario
            } 
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )