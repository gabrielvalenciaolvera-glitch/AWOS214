from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal
from datetime import datetime
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title="examen 2P",
    description="gabriel valencia"
)
@app.get("/",tags=["Inicio"])
async def bienvenida():
    return {"mensaje": "¡Bienvenido a mi API"}



class Ticket(BaseModel):
    id: int
    usuario: str = Field(min_length=5)
    descripcion: str = Field(min_length=26, max_length=200)
    prioridad: Literal["baja", "media","Alta"] = "baja"
    estado: Literal["pendiente", "resuelto"] = "pendiente"



class Resuelto(BaseModel):
    id_prestamo: int
    Ticket_id: int
    estado: Literal["Pendiente", "resuelto"]



security= HTTPBasic()

def verificar_Peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "soporte")
    passAuth = secrets.compare_digest(credenciales.password, "4321")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no Autorizadas"
        )
    return credenciales.username

Tickets: List[Ticket] = []
Resueltos: List[Resuelto] = []



@app.post("/v1/ticket/", status_code=status.HTTP_201_CREATED)
async def registrar_ticket(Ticket: Ticket):

    for l in Tickets:
        if l.id == Ticket.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID ya existe"
            )

    Tickets.append(Ticket)
    return Ticket


@app.get("/v1/ticket/", status_code=status.HTTP_200_OK)
async def listar_tickets():
    return {
        "total": len(Tickets),
        "Tickets": Tickets
    }

@app.get("/v1/ticket/buscar/{id}")
async def buscar_ticket(id: str, userAuth:str= Depends(verificar_Peticion)):

    resultados = [l for l in Tickets if l.id.lower() == id.lower()]

    if not resultados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID no válido o ticket no encontrado"
        )

    return resultados



@app.put("/v1/ticket/",status_code=status.HTTP_204_NO_CONTENT)
async def Actualizar_Ticket(Ticket:Ticket, userAuth:str= Depends(verificar_Peticion)):
    for l in Tickets:
        if l.id == Ticket.id:
            Tickets.append(Ticket)
            return{
                "mensaje":"Ticket Actualizado",
                "Usuario":Ticket
            }
        raise HTTPException(
            status_code=400,
            detail="El id no existe"
        )   
    
@app.delete("/v1/Ticket/")
async def Eliminar_Ticket(Ticket:Ticket):
    for l in Tickets:
        if l.id == Ticket.id:
            Tickets.pop(Ticket)
            return{
                "mensaje":"Ticket Eliminado",
                "Ticket Elminado":Ticket
            }
        raise HTTPException(
            status_code=400,
            detail="Id no existente"
        )







