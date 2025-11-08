import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Explicación del Dashboard de Accidentalidad Vial", page_icon="🚨", layout="centered")

# Encabezado elegante para el nuevo tema
st.markdown("""
<div style="background: linear-gradient(90deg, #A83333, #D44E4E); padding: 20px; border-radius: 12px; text-align: center;">
    <h1 style="color: white;">🚨 Análisis de Accidentes Viales en Medellín</h1>
</div>
""", unsafe_allow_html=True)

st.markdown(""" """)
st.markdown("## 📍 ¿Qué contiene el archivo csv?")
st.markdown("""
La base de datos contiene información detallada sobre **accidentes viales** en municipios del **Valle de Aburrá** (Medellín, Bello, Envigado, Sabaneta, Barbosa, etc.), con los siguientes campos clave que se visualizan en la tabla de datos:

- 📅 **FECHA**
- ⏰ **HORA**
- 🏙️ **MUNICIPIO**
- 🏘️ **COMUNA / BARRIO**
- 💥 **CLASE** de Accidente (Choque, Atropello, Volcamiento, etc.)
- 🚑 **GRAVEDAD** (Estado de las personas: Heridos, Daños, Muertos)
- 🗺️ **DIRECCIÓN**
""")

st.markdown("---")

st.markdown("## 🎛️ ¿Qué filtros se pueden aplicar?")
st.markdown("""
Desde la barra lateral llamada **"Configuración del Dashboard"** se pueden aplicar los siguientes filtros interactivos, tal como aparecen en la interfaz:

- 🏙️ **Municipio**
- 💥 **Clase de Accidente**
- 🚑 **Gravedad (Estado de las personas)**
- 🗓️ **Día de la Semana**
- 🏘️ **Comuna**
- 📅 **Rango de Fechas** (ejemplo: 2015/01/01 - 2018/12/31)
- 🔍 **Buscar por Dirección/Barrio**
""")

st.markdown("---")

st.markdown("## 📈 ¿Qué análisis visual se presenta?")
st.markdown("""
El dashboard genera las siguientes **visualizaciones de tendencias y causas**:

- 📊 **Distribución de Accidentes por Clase**: Conteo total por tipo de siniestro (Choque, Atropello, etc.).
- 🗓️ **Accidentes por Día de la Semana**: Frecuencia por día (Lunes a Domingo).
- 🏘️ **Distribución de Accidentes por Comuna**: Mapa de árbol (Treemap) con el total de accidentes por comuna.
- 📐 **Accidentes según el Diseño Vial**: Gráfico de pastel que muestra la proporción por lugar de ocurrencia (Tramo de Vía, Intersección, Glorieta, etc.).
- 🚨 **Gravedad de Accidentes por Clase**: Conteo de Heridos, Daños y Muertos por cada tipo de accidente.
- ⏰ **Frecuencia de Accidentes por Hora del Día**: Gráfico que muestra los picos de accidentalidad a lo largo de las 24 horas.
- 📉 **Tendencia Mensual de Accidentes**: Gráfico de líneas que muestra la evolución de la frecuencia de siniestros a lo largo del tiempo.
""")

st.markdown("---")

st.markdown("## ✅ ¿Para qué sirve este dashboard?")
st.markdown("""
Esta herramienta tiene como objetivo principal:

🚨 Identificar **puntos y momentos de riesgo** (días, horas, comunas) de alta accidentalidad.  
🧠 Entender el **impacto** real de los siniestros (Heridos/Muertos) por clase de accidente.  
📈 Apoyar la **planificación de la seguridad vial** basándose en patrones temporales y geográficos.
""")