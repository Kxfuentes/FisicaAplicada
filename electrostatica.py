"""Funciones para resolver problemas básicos de electrostática en 2D."""

from __future__ import annotations

from math import sqrt
from typing import Iterable

import numpy as np

K = 8.9875517923e9  # N·m²/C²


def _a_vector(posicion: tuple[float, float] | list[float] | np.ndarray) -> np.ndarray:
    """Convierte una posición 2D a un vector de numpy."""
    vector = np.asarray(posicion, dtype=float)
    if vector.shape != (2,):
        raise ValueError("La posición debe tener exactamente dos componentes: (x, y).")
    return vector


def fuerza_entre_cargas(
    q_objetivo: float,
    posicion_objetivo: tuple[float, float] | list[float] | np.ndarray,
    q_fuente: float,
    posicion_fuente: tuple[float, float] | list[float] | np.ndarray,
) -> np.ndarray:
    """
    Calcula la fuerza eléctrica ejercida sobre la carga objetivo por una carga fuente.

    Retorna un vector numpy con las componentes [Fx, Fy].
    """
    r_obj = _a_vector(posicion_objetivo)
    r_src = _a_vector(posicion_fuente)
    desplazamiento = r_obj - r_src
    distancia = np.linalg.norm(desplazamiento)

    if distancia == 0:
        raise ValueError(
            "Dos cargas no pueden ocupar la misma posición al calcular la fuerza."
        )

    return K * q_objetivo * q_fuente * desplazamiento / (distancia**3)


def fuerza_neta(
    q_objetivo: float,
    posicion_objetivo: tuple[float, float] | list[float] | np.ndarray,
    cargas: Iterable[dict],
) -> dict:
    """
    Suma la fuerza causada por n cargas puntuales sobre una carga objetivo.

    Cada elemento de `cargas` debe tener las llaves:
    - nombre
    - carga
    - posicion
    """
    total = np.zeros(2, dtype=float)
    detalles = []

    for indice, carga in enumerate(cargas, start=1):
        nombre = carga.get("nombre", f"Carga {indice}")
        q_fuente = float(carga["carga"])
        posicion_fuente = carga["posicion"]
        fuerza = fuerza_entre_cargas(
            q_objetivo=q_objetivo,
            posicion_objetivo=posicion_objetivo,
            q_fuente=q_fuente,
            posicion_fuente=posicion_fuente,
        )
        total += fuerza
        detalles.append(
            {
                "nombre": nombre,
                "Fx": float(fuerza[0]),
                "Fy": float(fuerza[1]),
                "magnitud": float(np.linalg.norm(fuerza)),
            }
        )

    return {
        "Fx": float(total[0]),
        "Fy": float(total[1]),
        "magnitud": float(np.linalg.norm(total)),
        "detalles": detalles,
    }


def parsear_cargas_desde_texto(texto: str) -> list[dict]:
    """
    Convierte texto tipo CSV simple a una lista de cargas.

    Formato esperado por línea:
    nombre,carga,x,y
    """
    cargas = []
    lineas = [linea.strip() for linea in texto.splitlines() if linea.strip()]

    for indice, linea in enumerate(lineas, start=1):
        partes = [parte.strip() for parte in linea.split(",")]
        if len(partes) != 4:
            raise ValueError(
                "Cada línea debe tener 4 valores: nombre,carga,x,y. "
                f"Error en la línea {indice}."
            )

        nombre, carga, x, y = partes
        cargas.append(
            {
                "nombre": nombre or f"Carga {indice}",
                "carga": float(carga),
                "posicion": (float(x), float(y)),
            }
        )

    return cargas


def magnitud_vector(fx: float, fy: float) -> float:
    """Retorna la magnitud de un vector 2D."""
    return sqrt(fx**2 + fy**2)
