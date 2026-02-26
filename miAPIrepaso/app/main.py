from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal
from datetime import datetime

app = FastAPI(
    title="Repaso API",
    description="Gabriel Valencia Olvera",
    version="1.0.0"
)



class Libro(BaseModel):
    id: int
    nombre: str = Field(min_length=2, max_length=100)
    paginas: int = Field(gt=1)
    año: int = Field(gt=1450, le=datetime.now().year)
    estado: Literal["disponible", "prestado"] = "disponible"


class Usuario(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr


class Prestamo(BaseModel):
    id_prestamo: int
    libro_id: int
    usuario: Usuario
    estado: Literal["prestado", "devuelto"]



Libros: List[Libro] = []
Prestamos: List[Prestamo] = []


@app.get("/",tags=["Inicio"])
async def bienvenida():
    return {"mensaje": "¡Bienvenido a mi API"}


@app.post("/v1/libros/", status_code=status.HTTP_201_CREATED)
async def registrar_libro(libro: Libro):

    for l in Libros:
        if l.id == libro.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID ya existe"
            )

    Libros.append(libro)
    return libro



@app.get("/v1/libros/", status_code=status.HTTP_200_OK)
async def listar_libros():
    return {
        "total": len(Libros),
        "libros": Libros
    }



@app.get("/v1/libros/buscar/{nombre}")
async def buscar_libro(nombre: str):

    resultados = [l for l in Libros if l.nombre.lower() == nombre.lower()]

    if not resultados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nombre no válido o libro no encontrado"
        )

    return resultados


@app.post("/v1/prestamos/", status_code=status.HTTP_201_CREATED)
async def registrar_prestamo(libro_id: int, usuario: Usuario):

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




@app.put("/v1/prestamos/devolver/{id_prestamo}", status_code=status.HTTP_200_OK)
async def devolver_libro(id_prestamo: int):

    for prestamo in Prestamos:

        if prestamo.id_prestamo == id_prestamo:

            if prestamo.estado == "devuelto":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El préstamo ya fue cerrado"
                )

            prestamo.estado = "devuelto"

            for libro in Libros:
                if libro.id == prestamo.libro_id:
                    libro.estado = "disponible"

            return {
                "mensaje": "Libro devuelto correctamente",
                "prestamo": prestamo
            }

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="El registro de préstamo no existe"
    )


@app.delete("/v1/prestamos/{id_prestamo}", status_code=status.HTTP_200_OK)
async def eliminar_prestamo(id_prestamo: int):

    for index, prestamo in enumerate(Prestamos):

        if prestamo.id_prestamo == id_prestamo:
            Prestamos.pop(index)
            return {"mensaje": "Préstamo eliminado correctamente"}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="El registro de préstamo no existe"
    )