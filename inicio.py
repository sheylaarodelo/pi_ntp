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
st.title("🗺️ Proyecto Integrador - Análisis Detallado de Accidentes Viales en el Área Metropolitana")

# 3. Descripción general
st.markdown("""
Bienvenidos a nuestra aplicación web interactiva para el **Análisis de la Accidentalidad Vial** en diversos municipios del Valle de Aburrá, incluyendo **Medellín, Bello, Barbosa, Envigado y Sabaneta**, entre otros.

Este sistema está diseñado para explorar y visualizar los datos clave de cada siniestro:

* **Ubicación y Tiempo:** Dirección exacta, **Ciudad** donde ocurrió, **Fecha** y **Hora** precisa.
* **Tipología:** El **Día** de la semana y el **Tipo de Accidente** (choque, atropello, volcamiento, etc.).
* **Impacto:** La **Gravedad** del siniestro, incluyendo el número de **muertos y heridos**.

Nuestro objetivo es identificar patrones de riesgo por municipio, hora y día, para apoyar la planificación de la seguridad vial en la región.

---
""")

# 4. Tecnologías utilizadas
st.subheader("🛠️ Tecnologías de Desarrollo y Análisis")
st.markdown("""
        - 🐍 **Python + Streamlit** – Backend, creación de dashboards interactivos y despliegue rápido.
        - 🐼 **Pandas** – Manipulación, limpieza y análisis de datos de siniestros.
        - 📈 **Plotly/Plotly Express** – Generación de visualizaciones de datos (mapas, gráficos de barras, etc.).
        - 📊 **Datos Abiertos de Medellín** – Fuente de datos oficial de accidentalidad.
""")

st.markdown(""" """)

# 5. Cómo ejecutar el proyecto (Instrucciones adaptadas para un proyecto Python puro)
st.subheader("🚀 ¿Cómo ejecutar la aplicación?")
st.markdown("""
        1. Clonar el repositorio.
        2. Crear un entorno virtual.
        3. Instalar las dependecias del archivo "requirements.txt". 
        4. Ejecuta en la terminal el siguiente comando:
          `streamlit run inicio.py`

""")

st.markdown("---")

# 6. Sección de información del estudiante/integrantes con diseño de tres columnas
col1, col2, col3 = st.columns([1, 2, 3])


with col2:
    st.markdown(""" """)

# Columna derecha: Información del estudiante
with col3:
    st.markdown('<h3 style="margin-top: 50px;">👩‍💻 Integrantes del Proyecto 👩‍💻</h3>', unsafe_allow_html=True)
    st.markdown(""" """)
    # NOTA: He mantenido tu información de contacto original, solo cambié el texto
    st.markdown('<p style="font-size: 16px;">🗿 **Sheyla** <span style="color: #FF6600; font-weight: bold; "></span></p>', unsafe_allow_html=True)
    st.markdown(""" """)
    st.markdown('<p style="font-size: 16px;">🗿 **Edgarly** <span style="color: #FF6600; font-weight: bold;"></p>', unsafe_allow_html=True)
    st.markdown(""" """)
    st.markdown('<p style="font-size: 16px;">🗿 **Ana Sofia** <span style="color: #FF6600; font-weight: bold;"></span></p>', unsafe_allow_html=True)
    st.markdown(""" """)
    st.markdown(""" """)
    st.markdown(""" """)
    st.caption("✅ Proyecto de Análisis de Datos para la Seguridad Vial ❤️")

st.markdown("---")

