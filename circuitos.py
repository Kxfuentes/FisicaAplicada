"""Funciones para resolver circuitos básicos de resistencias."""

from __future__ import annotations

from typing import Iterable


def _validar_resistencias(resistencias: Iterable[float]) -> list[float]:
    valores = [float(r) for r in resistencias]
    if not valores:
        raise ValueError("Debes proporcionar al menos una resistencia.")
    if any(r <= 0 for r in valores):
        raise ValueError("Todas las resistencias deben ser mayores que cero.")
    return valores


def resistencia_serie(resistencias: Iterable[float]) -> float:
    """Suma resistencias conectadas en serie."""
    valores = _validar_resistencias(resistencias)
    return float(sum(valores))


def resistencia_paralelo(resistencias: Iterable[float]) -> float:
    """Calcula la resistencia equivalente en paralelo."""
    valores = _validar_resistencias(resistencias)
    return float(1.0 / sum(1.0 / r for r in valores))


def corriente_total(voltaje: float, resistencia_equivalente: float) -> float:
    """Aplica la ley de Ohm: I = V / R."""
    resistencia_equivalente = float(resistencia_equivalente)
    if resistencia_equivalente <= 0:
        raise ValueError("La resistencia equivalente debe ser mayor que cero.")
    return float(voltaje) / resistencia_equivalente


def voltajes_en_serie(voltaje_total: float, resistencias: Iterable[float]) -> list[float]:
    """Distribuye la caída de voltaje en un circuito en serie."""
    valores = _validar_resistencias(resistencias)
    req = resistencia_serie(valores)
    i_total = corriente_total(voltaje_total, req)
    return [i_total * r for r in valores]


def corrientes_en_paralelo(voltaje_total: float, resistencias: Iterable[float]) -> list[float]:
    """Calcula la corriente en cada rama paralela."""
    valores = _validar_resistencias(resistencias)
    return [float(voltaje_total) / r for r in valores]


def resolver_circuito(tipo: str, resistencias: Iterable[float], voltaje: float) -> dict:
    """
    Resuelve un circuito de resistencias en serie o paralelo.

    `tipo` debe ser 'serie' o 'paralelo'.
    """
    tipo_normalizado = tipo.strip().lower()
    valores = _validar_resistencias(resistencias)
    voltaje = float(voltaje)

    if tipo_normalizado == "serie":
        req = resistencia_serie(valores)
        i_total = corriente_total(voltaje, req)
        distribucion = voltajes_en_serie(voltaje, valores)
        etiqueta = "voltajes_por_resistencia"
    elif tipo_normalizado == "paralelo":
        req = resistencia_paralelo(valores)
        i_total = corriente_total(voltaje, req)
        distribucion = corrientes_en_paralelo(voltaje, valores)
        etiqueta = "corrientes_por_rama"
    else:
        raise ValueError("El tipo de circuito debe ser 'serie' o 'paralelo'.")

    return {
        "tipo": tipo_normalizado,
        "resistencia_equivalente": req,
        "corriente_total": i_total,
        etiqueta: distribucion,
    }


def parsear_resistencias_desde_texto(texto: str) -> list[float]:
    """Convierte una cadena separada por comas o saltos de línea a resistencias."""
    texto_normalizado = texto.replace("\n", ",")
    partes = [parte.strip() for parte in texto_normalizado.split(",") if parte.strip()]
    if not partes:
        raise ValueError("No se encontraron resistencias válidas en el texto.")
    return _validar_resistencias(float(parte) for parte in partes)
