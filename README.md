# Calculadora de Electrostática y Circuitos

Aplicación en Python con interfaz gráfica en Streamlit para resolver:

- fuerza neta sobre una carga objetivo causada por n cargas puntuales en 2D,
- circuitos eléctricos con resistencias en serie y en paralelo,
- resistencia equivalente, corriente total y distribución de corrientes o voltajes.


## Organización del proyecto


.
├── app.py
├── electrostatica.py
├── circuitos.py
├── requirements.txt


- electrostatica.py: funciones para ley de Coulomb, fuerza entre cargas y fuerza neta.
- circuitos.py: funciones para resistencias en serie, paralelo, resistencia equivalente y corriente total.
- app.py: interfaz gráfica con Streamlit.
- requirements.txt: dependencias del proyecto.

## Funcionalidades

### 1. Cargas puntuales

- ingreso interactivo de la carga objetivo y de n cargas puntuales;
- posiciones como pares ordenados (x, y);
- cálculo del vector fuerza neta ⟨Fx, Fy⟩ en Newtons;
- cálculo de la magnitud total de la fuerza;
- tabla con el aporte individual de cada carga;
- entrada alternativa por texto estructurado.

Formato de texto:


q1,2e-6,1,0
q2,-3e-6,0,2


Cada línea representa:


nombre,carga,x,y


### 2. Circuitos eléctricos

- resistencias en serie;
- resistencias en paralelo;
- cálculo de resistencia equivalente;
- cálculo de corriente total;
- distribución de voltajes en serie;
- distribución de corrientes en ramas paralelas;
- entrada alternativa por texto estructurado.

Ejemplo de texto:

10, 20, 30


