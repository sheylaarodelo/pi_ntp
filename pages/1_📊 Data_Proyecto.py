import streamlit as st
import requests
import pandas as pd
import altair as alt

# =================================================================
# 1. CONFIGURACIÓN
# =================================================================

# URL de tu Mock API de Tareas (¡Esta URL debe ser la tuya!)
API_URL = "https://690b668e6ad3beba00f4c783.mockapi.io/api/v1/tasks"

# =================================================================
# 2. FUNCIONES DE INTERACCIÓN CON LA API
# =================================================================

@st.cache_data(ttl=60) # Carga los datos y los guarda en caché por 60 segundos
def get_tasks():
    """Realiza la solicitud GET a la API y devuelve los datos."""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error al obtener los datos. Código de estado: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")
        return None

def post_task(title, description, priority, complete, due_date):
    """Realiza la solicitud POST a la API para crear una nueva tarea."""

    # Prepara el cuerpo (payload) de la solicitud
    new_task = {
        "taskTitle": title,
        "description": description,
        "priority": priority,       # Se envía como string
        "isComplete": complete,     # Se envía como string 'false' o 'true'
        "dueDate": due_date
    }

    # Envía la solicitud POST
    response = requests.post(API_URL, json=new_task)

    if response.status_code == 201: # 201 = Created (Creado)
        st.success("✅ Tarea agregada exitosamente. Recargando datos...")
    else:
        st.error(f"❌ Error al agregar tarea. Código de estado: {response.status_code}")
        st.json(response.json()) # Muestra el error de la API si lo hay

# =================================================================
# 3. INTERFAZ Y LÓGICA DE STREAMLIT
# =================================================================

# Título y encabezado
st.title("✅ Mi Aplicación de Tareas (Mock API)")
st.caption("Datos obtenidos y gestionados desde una API simulada en mockapi.io")

# Obtener los datos
tasks_data = get_tasks()

if tasks_data:
    df = pd.DataFrame(tasks_data)

    # Aseguramos que la columna 'priority' sea numérica para la gráfica
    df['priority'] = pd.to_numeric(df['priority'], errors='coerce')

    # --- BARRA LATERAL (Formulario POST) ---
    st.sidebar.header("➕ Agregar Nueva Tarea")

    with st.sidebar.form("new_task_form"):
        title = st.text_input("Título de la Tarea")
        description = st.text_area("Descripción")

        # Slider para la Prioridad
        priority_num = st.slider("Prioridad (1=Alta, 3=Baja)", min_value=1, max_value=3, value=2)

        # Campo para la Fecha
        date_obj = st.date_input("Fecha Límite")

        submitted = st.form_submit_button("Crear Tarea")

        if submitted:
            if title:
                # Convertimos datos a string antes de enviar
                due_date_str = date_obj.strftime("%Y-%m-%d")
                # Inicialmente siempre es 'false' (pendiente)
                post_task(title, description, str(priority_num), 'false', due_date_str)
                # Forzar la recarga de la aplicación para ver el cambio
                st.cache_data.clear() # Limpia la caché para obtener los datos nuevos
                st.rerun()
            else:
                st.warning("El título de la tarea no puede estar vacío.")

    # --- CUERPO PRINCIPAL (Filtros y Datos) ---

    st.header(f"Total de Tareas Cargadas: {len(df)}")

    # 1. Filtro Interactivo
    st.subheader("🔎 Filtrar Tareas")

    completion_filter = st.selectbox(
        "Filtrar por Estado:",
        options=['Mostrar Todo', 'Pendientes', 'Completadas'],
        index=0
    )

    df_filtered = df.copy()

    if completion_filter == 'Pendientes':
        df_filtered = df_filtered[df_filtered['isComplete'] == 'false']
    elif completion_filter == 'Completadas':
        df_filtered = df_filtered[df_filtered['isComplete'] == 'true']

    # 2. Mostrar la tabla filtrada
    st.dataframe(
        df_filtered,
        use_container_width=True,
        column_order=['id', 'taskTitle', 'description', 'priority', 'isComplete', 'dueDate']
    )

    # 3. Gráfica de Resumen
    st.header("📊 Resumen de Tareas por Prioridad")

    # Contar tareas por prioridad
    priority_counts = df['priority'].value_counts().reset_index()
    priority_counts.columns = ['Prioridad', 'Número de Tareas']

    # Crear el gráfico de barras con Altair
    chart = alt.Chart(priority_counts).mark_bar().encode(
        x=alt.X('Prioridad:O', sort='-y'),
        y='Número de Tareas:Q',
        color=alt.Color('Prioridad:N', scale=alt.Scale(range=['#e45757', '#f4a761', '#59a14f'])), # Colores personalizados
        tooltip=['Prioridad', 'Número de Tareas']
    ).properties(
        title='Conteo de Tareas por Nivel de Prioridad'
    ).interactive() # Permite hacer zoom y pan

    st.altair_chart(chart, use_container_width=True)

else:
    st.warning("No se pudieron cargar las tareas. Verifica la URL de la API o la conexión.")






# 📚 Proyecto: API Simulada para Gestión de Tareas (MockAPI)

#  🎯 Objetivo del Proyecto

# Este proyecto consiste en la creación de una **API REST simulada** utilizando la plataforma **MockAPI.io** para simular un backend funcional. Posteriormente, esta API es consumida por una aplicación frontend desarrollada con **Python y Streamlit** para demostrar la interacción completa (CRUD: Leer, Crear, Filtrar y Visualizar) con datos simulados.

# ⚙️ Creación de la API en MockAPI.io

# La API fue diseñada para gestionar una colección de tareas (`tasks`) para una aplicación de lista de pendientes (`MiAppDeTareas`).

# 1. Configuración del Proyecto

# * **Nombre del Proyecto:** `MiAppDeTareas`
# * **Prefijo de API:** `/api/v1`
# * **URL Base:** `https://690b668e6ad3beba00f4c783.mockapi.io/api/v1/tasks`

# 2. Definición del Recurso (`tasks`)

# Se creó un único recurso llamado `tasks` con el siguiente esquema de datos. MockAPI generó automáticamente un `id` y `createdAt` para cada registro.

# | Campo | Tipo de Dato | Propósito |
# | :--- | :--- | :--- |
# | **taskTitle** | `String` | Título o resumen de la tarea. |
# | **description** | `String` | Descripción detallada. |
# | **isComplete** | `String/Boolean` | Estado de la tarea (`true` o `false`). |
# | **priority** | `String/Number` | Nivel de prioridad (ej: 1, 2, 3). |
# | **dueDate** | `String/Date` | Fecha límite de finalización. |

# 3. Endpoints Disponibles

# La URL final para el consumo es: `https://base.org//tasks`. MockAPI implementa automáticamente los siguientes métodos:

# | Método | URL | Descripción |
# | :--- | :--- | :--- |
# | **GET** | `/api/v1/tasks` | Obtener todas las tareas. |
# | **GET** | `/api/v1/tasks/:id` | Obtener una tarea específica. |
# | **POST** | `/api/v1/tasks` | **Crear** una nueva tarea. |
# | **PUT** | `/api/v1/tasks/:id` | **Actualizar** una tarea existente. |
# | **DELETE** | `/api/v1/tasks/:id` | **Eliminar** una tarea. |

# 💻 Consumo de la API con Python y Streamlit

# La aplicación cliente fue desarrollada en Python utilizando la librería `streamlit` para la interfaz de usuario, `requests` para las peticiones HTTP, `pandas` para el manejo de datos y `altair` para la visualización.

# Requisitos

# Para ejecutar el proyecto, se necesitan las siguientes librerías de Python:

# ```bash
# pip install streamlit requests pandas altair