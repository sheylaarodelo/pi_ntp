import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(
    page_title="Análisis de Accidentes en Medellín",
    page_icon="🚨",
    layout="wide"
)

# 2. Título principal
st.title("🎓 Proyecto Integrador - Análisis Detallado de Accidentes Viales en el Área Metropolitana")

# 3. Descripción general (Se mantiene a ancho completo)
st.markdown("""
Bienvenidos a nuestra aplicación web interactiva para el **Análisis de la Accidentalidad Vial** en diversos municipios del Valle de Aburrá, incluyendo **Medellín, Bello, Barbosa, Envigado y Sabaneta**, entre otros.

Este sistema está diseñado para explorar y visualizar los datos clave de cada siniestro:

* **Ubicación y Tiempo:** Dirección exacta, **Ciudad** donde ocurrió, **Fecha** y **Hora** precisa.
* **Tipología:** El **Día** de la semana y el **Tipo de Accidente** (choque, atropello, volcamiento, etc.).
* **Impacto:** La **Gravedad** del siniestro, incluyendo el número de **muertos y heridos**.

Nuestro objetivo es identificar patrones de riesgo por municipio, hora y día, para apoyar la planificación de la seguridad vial en la región.
""")

st.markdown("---")

# 4. Tecnologías utilizadas (Se coloca a ancho completo)
st.subheader("🛠️ Tecnologías de Desarrollo y Análisis")
st.markdown("""
    - 🐍 **Python + Streamlit** – Backend, creación de dashboards interactivos y despliegue rápido.
    - 🐼 **Pandas** – Manipulación, limpieza y análisis de datos de siniestros.
    - 📈 **Plotly/Plotly Express** – Generación de visualizaciones de datos (mapas, gráficos de barras, etc.).
    - 📊 **Datos Abiertos de Medellín** – Fuente de datos oficial de accidentalidad.
""")

st.markdown(""" """)

# 5. Cómo ejecutar el proyecto (Se coloca a ancho completo)
st.subheader("🚀 ¿Cómo ejecutar la aplicación?")
st.markdown("""
    1. Clonar el repositorio.
    2. Crear un entorno virtual.
    3. Instalar las dependecias del archivo "requirements.txt".
    4. Ejecuta en la terminal el siguiente comando:
      `streamlit run inicio.py`
""")

st.markdown("---")

# 6. Sección de integrantes (Ahora de nuevo abajo y a ancho completo)
st.markdown('<h3 style="text-align: center;">👩‍💻 Integrantes del Proyecto 👩‍💻</h3>', unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: center; gap: 40px; margin-top: 20px;">
    <p style="font-size: 16px;">🗿 **Sheyla**</p>
    <p style="font-size: 16px;">🗿 **Edgarly**</p>
    <p style="font-size: 16px;">🗿 **Ana Sofia**</p>
</div>
""", unsafe_allow_html=True)

st.markdown(""" """)
st.markdown('<p style="text-align: center; font-size: 0.8rem; color: #aaa;">✅ Proyecto de Análisis de Datos para la Seguridad Vial ❤️</p>', unsafe_allow_html=True)

st.markdown("---") # Separador final