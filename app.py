"""Interfaz gráfica principal del proyecto usando Streamlit."""

from __future__ import annotations

import streamlit as st

from circuitos import (
    parsear_resistencias_desde_texto,
    resolver_circuito,
)
from electrostatica import fuerza_neta, parsear_cargas_desde_texto


st.set_page_config(page_title="Electrostática y Circuitos", page_icon="⚡", layout="wide")


def mostrar_imagen_subida() -> None:
    st.caption(
        "Puedes subir una imagen del ejercicio como referencia visual. "
        "La app mostrará la imagen y tú ingresas los valores en los campos interactivos."
    )
    archivo = st.file_uploader(
        "Sube una imagen del problema (opcional)", type=["png", "jpg", "jpeg"]
    )
    if archivo is not None:
        st.image(
            archivo,
            caption="Imagen de referencia del ejercicio",
            use_container_width=True,
        )


def interfaz_electrostatica() -> None:
    st.header("Problemas de cargas puntuales")
    st.write(
        "Calcula la fuerza neta sobre una carga objetivo a partir de *n* cargas puntuales en 2D."
    )
    mostrar_imagen_subida()

    modo = st.radio(
        "Modo de entrada",
        ["Entradas interactivas", "Texto estructurado"],
        horizontal=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        q_obj = st.number_input(
            "Carga objetivo q₀ (C)",
            value=1e-6,
            format="%.8e",
            help="Usa Coulombs. Ejemplo: 2e-6",
        )
    with col2:
        st.write("Posición de la carga objetivo")
        x_obj = st.number_input("x₀ (m)", value=0.0, key="x_obj")
        y_obj = st.number_input("y₀ (m)", value=0.0, key="y_obj")

    cargas = []

    if modo == "Entradas interactivas":
        n = st.number_input("Número de cargas puntuales", min_value=1, value=2, step=1)
        for i in range(int(n)):
            with st.expander(f"Carga {i + 1}", expanded=True):
                nombre = st.text_input("Nombre", value=f"q{i + 1}", key=f"nombre_{i}")
                q = st.number_input(
                    "Magnitud de la carga (C)",
                    value=1e-6,
                    format="%.8e",
                    key=f"q_{i}",
                )
                x = st.number_input("x (m)", value=float(i + 1), key=f"x_{i}")
                y = st.number_input("y (m)", value=0.0, key=f"y_{i}")
                cargas.append({"nombre": nombre, "carga": q, "posicion": (x, y)})
    else:
        texto = st.text_area(
            "Pega una carga por línea con el formato nombre,carga,x,y",
            value="q1,2e-6,1,0\nq2,-3e-6,0,2",
            height=160,
        )
        try:
            cargas = parsear_cargas_desde_texto(texto)
            st.success(f"Se cargaron {len(cargas)} cargas correctamente.")
        except ValueError as error:
            st.error(str(error))

    if st.button("Calcular fuerza neta", type="primary"):
        try:
            resultado = fuerza_neta(
                q_objetivo=q_obj,
                posicion_objetivo=(x_obj, y_obj),
                cargas=cargas,
            )
            st.subheader("Resultados")
            c1, c2, c3 = st.columns(3)
            c1.metric("Fx (N)", f"{resultado['Fx']:.6e}")
            c2.metric("Fy (N)", f"{resultado['Fy']:.6e}")
            c3.metric("|F| (N)", f"{resultado['magnitud']:.6e}")

            st.write(
                f"Vector fuerza neta: ⟨{resultado['Fx']:.6e}, {resultado['Fy']:.6e}⟩ N"
            )

            if resultado["detalles"]:
                st.subheader("Aporte de cada carga")
                st.dataframe(resultado["detalles"], use_container_width=True)
        except ValueError as error:
            st.error(str(error))


def interfaz_circuitos() -> None:
    st.header("Problemas de circuitos eléctricos")
    st.write(
        "Resuelve circuitos de resistencias en serie o paralelo, con resistencia equivalente, "
        "corriente total y distribución de voltajes o corrientes."
    )
    mostrar_imagen_subida()

    tipo = st.selectbox("Tipo de circuito", ["Serie", "Paralelo"])
    modo = st.radio(
        "Modo de entrada",
        ["Entradas interactivas", "Texto estructurado"],
        horizontal=True,
        key="modo_circuitos",
    )

    voltaje = st.number_input("Voltaje de la fuente (V)", min_value=0.0, value=12.0)
    resistencias = []

    if modo == "Entradas interactivas":
        n = st.number_input(
            "Número de resistencias", min_value=1, value=3, step=1, key="n_resistencias"
        )
        cols = st.columns(3)
        for i in range(int(n)):
            with cols[i % 3]:
                r = st.number_input(
                    f"R{i + 1} (Ω)",
                    min_value=0.001,
                    value=float(10 * (i + 1)),
                    key=f"r_{i}",
                )
                resistencias.append(r)
    else:
        texto = st.text_area(
            "Pega las resistencias separadas por comas o saltos de línea",
            value="10, 20, 30",
            height=120,
            key="texto_resistencias",
        )
        try:
            resistencias = parsear_resistencias_desde_texto(texto)
            st.success(f"Se cargaron {len(resistencias)} resistencias correctamente.")
        except ValueError as error:
            st.error(str(error))

    if st.button("Resolver circuito", type="primary"):
        try:
            resultado = resolver_circuito(tipo, resistencias, voltaje)
            st.subheader("Resultados")
            c1, c2 = st.columns(2)
            c1.metric("Resistencia equivalente (Ω)", f"{resultado['resistencia_equivalente']:.6f}")
            c2.metric("Corriente total (A)", f"{resultado['corriente_total']:.6f}")

            if resultado["tipo"] == "serie":
                st.write("Caída de voltaje en cada resistencia")
                datos = [
                    {"Resistencia": f"R{i + 1}", "Voltaje (V)": valor}
                    for i, valor in enumerate(resultado["voltajes_por_resistencia"])
                ]
            else:
                st.write("Corriente en cada rama")
                datos = [
                    {"Rama": f"R{i + 1}", "Corriente (A)": valor}
                    for i, valor in enumerate(resultado["corrientes_por_rama"])
                ]

            st.dataframe(datos, use_container_width=True)
        except ValueError as error:
            st.error(str(error))


def main() -> None:
    st.title("Calculadora de Electrostática y Circuitos")
    st.write(
        "Selecciona el tipo de problema, ingresa los datos y obtén resultados numéricos "
        "listos para entregar o verificar."
    )

    opcion = st.sidebar.radio(
        "Menú",
        ["Cargas puntuales", "Circuitos eléctricos"],
    )

    with st.sidebar:
        st.markdown("### Notas")
        st.markdown("- Electroestática en 2D con ley de Coulomb.")
        st.markdown("- Circuitos de resistencias en serie y paralelo.")
        st.markdown("- Se admite entrada manual, por texto y referencia mediante imagen.")

    if opcion == "Cargas puntuales":
        interfaz_electrostatica()
    else:
        interfaz_circuitos()


if __name__ == "__main__":
    main()
