from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal
from datetime import datetime

app = FastAPI(
    title="examen 2P",
    description="gabriel valencia"
)
@app.get("/",tags=["Inicio"])
async def bienvenida():
    return {"mensaje": "¡Bienvenido a mi API"}



class Ticket(BaseModel):
    id: int
    descripcion: str = Field(min_length=26, max_length=200)
    prioridad: Literal["baja", "media","Alta"] = "baja"
    estado: Literal["pentiente", "resuelto"] = "pendiente"

class Usuario(BaseModel):
    nombre: str = Field(min_length=5)
    correo: EmailStr



class Resuelto(BaseModel):
    id_prestamo: int
    Ticket_id: int
    estado: Literal["Pendiente", "resuelto"]


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
        "libros": Tickets
    }

@app.get("/v1/ticket/buscar/{id}")
async def buscar_ticket(id: str):

    resultados = [l for l in Tickets if l.id.lower() == id.lower()]

    if not resultados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID no válido o ticket no encontrado"
        )

    return resultados


@app.post("/v1/ticket/", status_code=status.HTTP_201_CREATED)
async def resolver_Ticket(libro_id: int, usuario: Usuario):

    for libro in Libros:

        if libro.id == libro_id:

            if libro.estado == "prestado":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El libro ya está prestado"
                )

            libro.estado = "prestado"

            nuevo_prestamo = Prestamo(
                id_prestamo=len(Prestamos) + 1,
                libro_id=libro_id,
                usuario=usuario,
                estado="prestado"
            )

            Prestamos.append(nuevo_prestamo)
            return nuevo_prestamo

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Libro no encontrado"
    )














@app.delete("/v1/ticket/{id_Ticket}", status_code=status.HTTP_200_OK)
async def eliminar_Ticket(id_Ticket: int):

    for index, Ticket in enumerate(Tickets):

        if Ticket.id_Ticket == id_prestamo:
            Prestamos.pop(index)
            return {"mensaje": "Préstamo eliminado correctamente"}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="El registro de préstamo no existe"
    )

