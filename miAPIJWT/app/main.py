#Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel,Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime , timedelta
from passlib.context import CryptContext


#Instancia del servidor
app = FastAPI(title=" API con JWT",
              description="Gabriel Valencia Olvera",
              version="1.0.0"
              )


# Configuración JWT

SECRET_KEY = "mi_clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #máximmo 30 minutos

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#TB ficticia
usuarios=[
    {"id":1,"nombre":"juan","edad":21},
    {"id":2,"nombre":"Pepe","edad":31},
    {"id":3,"nombre":"Diego","edad":21},
]

#TB ficticia con un usuario y contraseña

fake_users_db = {
    "Gabriel":{
        "username":"Gabriel",
        "hashed_password": pwd_context.hash("1234")
    }
}

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Usuario incorrecto")

    if not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

#modelo de validacion pydantic

class usuario_create(BaseModel):
    id: int = Field(..., gt=0, description="Identificador")
    nombre: str = Field(..., min_length=3, max_length=50, example="Gabriel")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")






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
    usuarios.append(usuario.dict())
    return{
        "mensaje": "Usuario agregado",
        "usuario": usuario
    }


@app.put("/V1/usuarios/", tags=['CRUD HTTP'])
async def actualizar_usuario(id:int, usuario_actualizado:dict, 
                             current_user: str = Depends(get_current_user)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuario.update(usuario_actualizado)
            return{
                "mensaje": "Usuario actualizado",
                "usuario": usuario
            }
    raise HTTPException(status_code=400, detail="Usuario no encontrado")



@app.delete("/V1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, 
                          current_user: str = Depends(get_current_user)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return{
                "mensaje": "Usuario eliminado correctamente",
                "usuario": usuario
            } 
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )