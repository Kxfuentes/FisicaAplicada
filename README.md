# Calculadora de Electrostática y Circuitos

Aplicación en Python con interfaz gráfica en Streamlit para resolver:

- fuerza neta sobre una carga objetivo causada por `n` cargas puntuales en 2D,
- circuitos eléctricos con resistencias en serie y en paralelo,
- resistencia equivalente, corriente total y distribución de corrientes o voltajes.

La app fue pensada para que el profesor pueda abrirla directamente desde su navegador mediante Streamlit Cloud, sin instalar nada.

## Organización del proyecto

```text
.
├── app.py
├── electrostatica.py
├── circuitos.py
├── requirements.txt
└── README.md
```

- `electrostatica.py`: funciones para ley de Coulomb, fuerza entre cargas y fuerza neta.
- `circuitos.py`: funciones para resistencias en serie, paralelo, resistencia equivalente y corriente total.
- `app.py`: interfaz gráfica con Streamlit.
- `requirements.txt`: dependencias del proyecto.

## Funcionalidades

### 1. Cargas puntuales

- ingreso interactivo de la carga objetivo y de `n` cargas puntuales;
- posiciones como pares ordenados `(x, y)`;
- cálculo del vector fuerza neta `⟨Fx, Fy⟩` en Newtons;
- cálculo de la magnitud total de la fuerza;
- tabla con el aporte individual de cada carga;
- entrada alternativa por texto estructurado.

Formato de texto:

```text
q1,2e-6,1,0
q2,-3e-6,0,2
```

Cada línea representa:

```text
nombre,carga,x,y
```

### 2. Circuitos eléctricos

- resistencias en serie;
- resistencias en paralelo;
- cálculo de resistencia equivalente;
- cálculo de corriente total;
- distribución de voltajes en serie;
- distribución de corrientes en ramas paralelas;
- entrada alternativa por texto estructurado.

Ejemplo de texto:

```text
10, 20, 30
```

## Soporte para ejercicios en texto o imagen

La aplicación permite:

- ingresar directamente los valores cuando el ejercicio está descrito en texto;
- subir una imagen del problema como referencia visual dentro de la interfaz.

En esta versión, la imagen se usa como apoyo visual y los datos numéricos se introducen manualmente en los campos de la app.

## Instalación local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en GitHub y Streamlit Cloud

### 1. Subir el proyecto a GitHub

1. Crea un repositorio nuevo en GitHub.
2. Sube los archivos `app.py`, `electrostatica.py`, `circuitos.py`, `requirements.txt` y `README.md`.
3. Verifica que todo quede en la rama principal (`main`).

Comandos típicos:

```bash
git init
git add .
git commit -m "Proyecto de electrostática y circuitos con Streamlit"
git branch -M main
git remote add origin TU_URL_DEL_REPOSITORIO
git push -u origin main
```

### 2. Publicar en Streamlit Cloud

1. Inicia sesión en [Streamlit Cloud](https://streamlit.io/cloud) con tu cuenta de GitHub.
2. Selecciona **Create app**.
3. Elige tu repositorio.
4. Selecciona la rama `main`.
5. Selecciona el archivo principal `app.py`.
6. Pulsa **Deploy**.

Al finalizar tendrás:

- un enlace público a la app para que el profesor la abra en su navegador;
- un enlace al repositorio de GitHub para revisar el código fuente.

## Enlaces de entrega

Completa esta sección cuando publiques el proyecto:

- Repositorio en GitHub: `PENDIENTE`
- Aplicación en Streamlit Cloud: `PENDIENTE`

## Autor

Proyecto académico desarrollado en Python, NumPy y Streamlit.
