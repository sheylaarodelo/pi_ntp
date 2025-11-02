import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_icon="🚨",
    layout="wide"
)

# --- CONFIGURACIÓN Y CARGA DE DATOS ---

# Cargar datos con el delimitador y la codificación correctos
archivo_csv = 'data/AMVA_Accidentalidad_20191022_2.csv' 
try:
    # Usamos punto y coma como separador y codificación para manejar la 'Ñ' y los acentos
    df = pd.read_csv(archivo_csv, sep=';', encoding='latin1')
except FileNotFoundError:
    st.error(f"Error: El archivo CSV no se encontró en la ruta '{archivo_csv}'.")
    st.stop()

# --- Limpieza y preparación de datos (CORRECCIONES CLAVE DE KEYERROR) ---

# 1. Limpiar los nombres de columna: Eliminar espacios y caracteres no ASCII
df.columns = [col.strip() for col in df.columns]

# 2. Renombrar explícitamente las columnas problemáticas
df.rename(columns={
    # Correcciones de GRAVEDAD (soluciona KeyError)
    'GRAVEDA\xbaOSSADA\xbaOSS': 'GRAVEDAD', 
    'GRAVEDAºOSSADAºOSS': 'GRAVEDAD', 
    
    # Correcciones de DIRECCIÓN (soluciona KeyError)
    'DIRECCIÓN': 'DIRECCION', 
    'DIRECCI\xcaN': 'DIRECCION', 
    'DIRECCION ': 'DIRECCION',
    
    # Correcciones de DÍA DE LA SEMANA
    'D\xcdA DE LA SEMANA': 'DÍA DE LA SEMANA', 
    'D\xcdA DE LA SEMANA ': 'DÍA DE LA SEMANA',
    'DIA DE LA SEMANA': 'DÍA DE LA SEMANA',
    
    # Correcciones de DISEÑO y MUNICIPIO
    'DISE\xcaO': 'DISEÑO',
    'MUNICIPIO ': 'MUNICIPIO'
    
}, errors='ignore', inplace=True) 

# Verificación de la columna 'GRAVEDAD' después del renombrado (Seguridad extra)
if 'GRAVEDAD' not in df.columns:
    gravedad_col_candidates = [col for col in df.columns if 'GRAVEDAD' in col.upper() or 'OSSADA' in col.upper()]
    if gravedad_col_candidates:
        df.rename(columns={gravedad_col_candidates[0]: 'GRAVEDAD'}, inplace=True)
    else:
        st.error("Error Crítico: No se pudo identificar la columna de 'GRAVEDAD'.")
        st.stop()
    
# Convertir FECHA y HORA
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
# Asumiendo que HORA está en formato "hh:mm:ss AM/PM"
df['HORA_ACCIDENTE'] = pd.to_datetime(df['HORA'], format='%I:%M:%S %p', errors='coerce').dt.time
df['HORA_DIA'] = pd.to_datetime(df['HORA'], format='%I:%M:%S %p', errors='coerce').dt.hour 

# Eliminar filas con valores nulos o 'SIN INFORMACIÓN' en columnas clave
df = df.dropna(subset=['FECHA', 'MUNICIPIO', 'COMUNA', 'CLASE', 'GRAVEDAD'])
df = df[df['COMUNA'] != 'SIN INFORMACI\xcaN'] 

# --- SIDEBAR: FILTROS ---

st.sidebar.title("🔧 Configuración del Dashboard")
st.sidebar.header("🎯 Filtros de Accidentes")

# Filtro por municipio
municipio_seleccionado = st.sidebar.selectbox(
    "📍 Municipio:",
    ["Todos"] + sorted(df["MUNICIPIO"].unique())
)

# Filtro por clase de accidente
clase = st.sidebar.selectbox(
    "💥 Clase de Accidente:",
    ["Todos"] + sorted(df["CLASE"].unique())
)

# Filtro por gravedad
gravedad = st.sidebar.selectbox(
    "💔 Gravedad (Estado de las personas):",
    ["Todos"] + sorted(df["GRAVEDAD"].unique())
)

# Filtro por día de la semana
dia_semana = st.sidebar.selectbox(
    "🗓️ Día de la Semana:",
    ["Todos"] + sorted(df["DÍA DE LA SEMANA"].str.strip().unique())
)

# Filtro por Comuna
comuna = st.sidebar.selectbox(
    "🏘️ Comuna:",
    ["Todos"] + sorted(df["COMUNA"].unique())
)

# Filtro por Rango de Fechas
min_fecha = df['FECHA'].min().date() if not df['FECHA'].empty else None
max_fecha = df['FECHA'].max().date() if not df['FECHA'].empty else None

if min_fecha and max_fecha:
    fecha_rango = st.sidebar.date_input(
        "📅 Rango de Fechas:",
        value=[min_fecha, max_fecha],
        min_value=min_fecha,
        max_value=max_fecha
    )
else:
    st.warning("No hay datos de fecha válidos para filtrar.")
    st.stop()

# --- APLICAR FILTROS ---

df_filtrado = df.copy()

# Filtro de texto (opcional)
direccion = st.sidebar.text_input("🔍 Buscar por Dirección/Barrio:")
if direccion:
    # Usa 'DIRECCION' (sin acento) aquí
    df_filtrado = df_filtrado[
        df_filtrado["DIRECCION"].str.contains(direccion, case=False, na=False) |
        df_filtrado["BARRIO"].str.contains(direccion, case=False, na=False)
    ]

# Filtros Selectbox
if municipio_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["MUNICIPIO"] == municipio_seleccionado]

if clase != "Todos":
    df_filtrado = df_filtrado[df_filtrado["CLASE"] == clase]

if gravedad != "Todos":
    df_filtrado = df_filtrado[df_filtrado["GRAVEDAD"] == gravedad]

if dia_semana != "Todos":
    df_filtrado = df_filtrado[df_filtrado["DÍA DE LA SEMANA"].str.strip() == dia_semana]

if comuna != "Todos":
    df_filtrado = df_filtrado[df_filtrado["COMUNA"] == comuna]

# Filtro de Fechas
if fecha_rango and len(fecha_rango) == 2:
    start_date = pd.to_datetime(fecha_rango[0])
    end_date = pd.to_datetime(fecha_rango[1])
    df_filtrado = df_filtrado[
        (df_filtrado['FECHA'] >= start_date) & (df_filtrado['FECHA'] <= end_date)
    ]

# --- VISTA PRINCIPAL ---

st.markdown("""
<div style="background: linear-gradient(90deg, #8B0000, #B22222); 
             padding:10px; 
             border-radius:10px; 
             text-align:center;">
    <h1 style="color:white;">🚨Análisis de Siniestros Viales en Medellín🚨</h1>
</div>
""", unsafe_allow_html=True)

if not df_filtrado.empty:
    st.markdown(f"**Total de Registros:** {len(df_filtrado)} | **Rango de Fechas:** {fecha_rango[0].strftime('%Y-%m-%d')} a {fecha_rango[1].strftime('%Y-%m-%d')}")

    # Mostrar DataFrame filtrado (CORREGIDO: Usa 'DIRECCION' sin acento)
    st.markdown("<h2 style='text-align: center;'>📁 Datos Filtrados</h2>", unsafe_allow_html=True)
    st.dataframe(df_filtrado[['FECHA', 'HORA', 'MUNICIPIO', 'COMUNA', 'BARRIO', 'CLASE', 'GRAVEDAD', 'DIRECCION']], use_container_width=True)
else:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")
    st.stop()


# --------------------------
# --- GRÁFICOS AVANZADOS ---
# --------------------------

st.markdown("<h2 style='text-align: center;'>📈 Visualización de Tendencias y Causas</h2>", unsafe_allow_html=True)

# Fila 1 de gráficos
col1, col2 = st.columns(2)

# Gráfico 1: Número de Accidentes por Clase
df_clase = df_filtrado.groupby('CLASE').size().reset_index(name='Total Accidentes')
fig_clase = px.bar(df_clase, x='CLASE', y='Total Accidentes', color='CLASE',
                   title="Distribución de Accidentes por Clase",
                   labels={'CLASE': 'Clase de Accidente', 'Total Accidentes': 'Frecuencia'})
col1.plotly_chart(fig_clase, use_container_width=True)

# Gráfico 2: Accidentes por Día de la Semana (CORREGIDO el ValueError de 'index')
orden_dias = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']
df_dias = df_filtrado['DÍA DE LA SEMANA'].str.strip().value_counts().reindex(orden_dias).fillna(0).reset_index(name='Total Accidentes')
# 🚨 CORRECCIÓN: Renombrar 'index' a 'DÍA DE LA SEMANA'
df_dias.rename(columns={'index': 'DÍA DE LA SEMANA'}, inplace=True) 

fig_dias = px.bar(df_dias, x='DÍA DE LA SEMANA', y='Total Accidentes', color='Total Accidentes',
                   title="Accidentes por Día de la Semana",
                   labels={'DÍA DE LA SEMANA': 'Día de la Semana', 'Total Accidentes': 'Frecuencia'})
col2.plotly_chart(fig_dias, use_container_width=True)


# Fila 2 de gráficos
col3, col4 = st.columns(2)

# Gráfico 3: Distribución de Gravedad por Clase (Barras Apiladas)
fig_gravedad_clase = px.histogram(df_filtrado, x='CLASE', color='GRAVEDAD',
                                   title="Gravedad de Accidentes por Clase",
                                   labels={'CLASE': 'Clase de Accidente', 'count': 'Total de Accidentes'},
                                   category_orders={"GRAVEDAD": ["Solo Daños", "Heridos", "Muertos"]}) 
col3.plotly_chart(fig_gravedad_clase, use_container_width=True)


# Gráfico 4: Accidentes por Hora del Día (Histograma)
fig_hora = px.histogram(df_filtrado, x='HORA_DIA', nbins=24, color='GRAVEDAD',
                        title="Frecuencia de Accidentes por Hora del Día",
                        labels={'HORA_DIA': 'Hora del Día', 'count': 'Número de Accidentes'})
fig_hora.update_layout(xaxis=dict(tickmode='linear', dtick=1))
col4.plotly_chart(fig_hora, use_container_width=True)


# Fila 3 de gráficos
st.markdown("---")
col5, col6 = st.columns(2)

# Gráfico 5: Accidentes por Comuna (Mapa de Árbol o Tree Map)
df_comuna_counts = df_filtrado['COMUNA'].value_counts().reset_index()
df_comuna_counts.columns = ['COMUNA', 'Total Accidentes']
fig_treemap = px.treemap(df_comuna_counts, path=[px.Constant("Medellín"), 'COMUNA'], values='Total Accidentes',
                         title="Distribución de Accidentes por Comuna",
                         color='Total Accidentes', hover_data=['COMUNA'],
                         color_continuous_scale='Reds')
col5.plotly_chart(fig_treemap, use_container_width=True)


# Gráfico 6: Distribución de Accidentes por Diseño Vial (Gráfico de Tarta)
df_diseno = df_filtrado['DISEÑO'].value_counts().reset_index()
df_diseno.columns = ['DISEÑO', 'Total Accidentes']
fig_pie_diseno = px.pie(df_diseno, names='DISEÑO', values='Total Accidentes',
                        title="Accidentes según el Diseño Vial",
                        hole=0.3)
col6.plotly_chart(fig_pie_diseno, use_container_width=True)


# Fila 4: Tendencia Mensual de Accidentes
st.markdown("---")
df_tiempo = df_filtrado.groupby(df_filtrado['FECHA'].dt.to_period('M')).size().reset_index(name='Total Accidentes')
df_tiempo['FECHA'] = df_tiempo['FECHA'].astype(str)

fig_tiempo = px.line(df_tiempo, x='FECHA', y='Total Accidentes',
                     title="Tendencia Mensual de Accidentes",
                     labels={'FECHA': 'Mes y Año', 'Total Accidentes': 'Frecuencia'})
st.plotly_chart(fig_tiempo, use_container_width=True)