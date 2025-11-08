import os
import streamlit as st
from google import genai 

# --- Configuración y Estilización de la Página ---

# Usa un emoji más acorde al nuevo estilo
st.set_page_config(
    page_title="Gemini Code Assistant", 
    page_icon="✨", 
    layout="wide"
)

# Estilos CSS personalizados (más sencillos ahora que usamos el tema claro)
st.markdown("""
<style>
/* Los colores principales se definen ahora en config.toml. 
   Aquí ajustamos elementos específicos que no respeta el tema. */

/* Título Principal: Usamos el color del tema */
.stTitle {
    text-align: center;
    font-size: 3.2em;
    font-weight: 700;
    color: #C2185B; /* Rosa Fuerte para que resalte */
}

/* Botón Principal de Envío */
.stButton>button {
    background-color: #fc3737ff; /* Rojo */
    color: white;
    border-radius: 15px; 
    padding: 12px 28px;
    font-size: 1.3em;
    border: none;
    font-weight: bold;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
}
.stButton>button:hover {
    background-color: #F48FB1; /* Un tono más suave al pasar el mouse */
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

/* Cuadro de Información (st.info) - Más delicado */
.stAlert.info {
    /* Fondo cambiado a un tono rosado oscuro o malva que contraste con el fondo negro */
    background-color: #ff7ca8ff !important; 
    /* Texto blanco para que contraste con el fondo rosado oscuro */
    color: white !important; 
    /* Barra lateral izquierda cambiada a un rosa brillante */
    border-left: 5px solid #FF80AB !important; 
    border-radius: 10px;
    padding: 15px; 
    font-size: 1.1em; 
}

/* Caja de Resultado */
.result-box {
    padding: 25px;
    border-radius: 15px;
    border-left: 10px solid #ff7ca8ff; /* Borde Rosa Oscuro */
    background-color: #262730; /* Fondo  para el código */
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)


# --- Interfaz de Usuario: Barra Lateral (Sidebar) para la Configuración ---

with st.sidebar:
    st.markdown("## ⚙️ Configuración API", unsafe_allow_html=True) 
    
    # El fondo es ahora el secondaryBackgroundColor (#FCE4EC) de config.toml
    
    # 1. Validación de la API Key
    api_key = st.text_input(
        "Ingresa tu Clave API de Gemini:", 
        type="password", 
        placeholder="GEMINI_API_KEY",
        key="api_key_input" 
    )
    
    # 2. Selector de Modelo 
    modelo_seleccionado = st.selectbox(
        "Modelo de Gemini:",
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-pro"],
        index=0, 
        help="Gemini 2.5 Flash es rápido y económico, ideal para tareas de código."
    )
    
    st.markdown("---")
    st.caption("Obtén tu clave en Google AI Studio.")


# --- Funciones de Lógica de la Solicitud (sin cambios) ---

def generar_respuesta(prompt, tarea, model_name, api_key):
    """Genera la respuesta de Gemini con instrucciones específicas para la tarea."""
    if not prompt:
        return "⚠️ Por favor, ingresa una descripción o pega el código para continuar."
        
    if not api_key:
        return "🛑 **Error de Autenticación:** Por favor, ingresa tu clave API en la barra lateral."

    # 1. Adaptar el prompt según la tarea seleccionada (Implementación completa)
    if tarea == "Generar código corto":
        instruccion = f"Genera un código corto y conciso, solo el código, basado en esta solicitud: {prompt}"
        
    elif tarea == "Generar código extenso/detallado":
        instruccion = f"Genera un código extenso y detallado, incluyendo comentarios, ejemplos de uso y explicaciones, basado en esta solicitud: {prompt}"
        
    elif tarea == "Corregir código existente":
        instruccion = f"Analiza y corrige el siguiente código. En la respuesta, primero explica brevemente los errores y la solución, y luego proporciona el código corregido en un bloque de código Markdown:\n\n{prompt}"
        
    elif tarea == "Explicar código":
        instruccion = f"Analiza el siguiente código y explica detalladamente qué hace, cómo funciona cada parte y su propósito. Utiliza un tono educativo y claro:\n\n{prompt}"
        
    else:
        instruccion = prompt 


    try:
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model=model_name, 
            contents=instruccion
        )
        return response.text
    
    except Exception as e:
        if "API key" in str(e):
             return "❌ **Error de la API:** La clave proporcionada no es válida. Por favor, revísala."
        return f"❌ **Error al llamar a la API:** {str(e)}"


# --- Lógica Principal de Streamlit (Página Principal) ---

st.markdown('<h1 class="stTitle">✨ Asistente de Código Avanzado con Gemini</h1>', unsafe_allow_html=True)
st.info("Elige una tarea y describe el código que necesitas. ¡Tu clave API se ingresa en la barra lateral! ➡️")

# Diseño en dos columnas para los controles principales
col_select, col_empty = st.columns([1, 3])

with col_select:
    opcion_tarea = st.selectbox(
        "Selecciona la tarea que deseas realizar:",
        ["Generar código corto", "Generar código extenso/detallado", "Corregir código existente", "Explicar código"]
    )

# 2. Área de Entrada de Texto (Única para todo)
if opcion_tarea in ["Corregir código existente", "Explicar código"]:
    placeholder_text = "Pega tu código Python/JS/etc. aquí y/o describe lo que debe corregir/explicar..."
else:
    placeholder_text = "Ej. Una función en Python para calcular el área de un círculo y manejar errores."
    
prompt = st.text_area(
    f"✍️ **Entrada para la Tarea: {opcion_tarea}**",
    placeholder=placeholder_text,
    height=250 
)

# Coloca el botón de envío al final
st.markdown("---")
enviar = st.button(" Enviar Solicitud a Gemini", use_container_width=True) 


# --- Lógica de la Respuesta ---

if enviar:
    with st.spinner(f"✨ Ejecutando la tarea: {opcion_tarea} con {modelo_seleccionado}..."): 
        respuesta = generar_respuesta(prompt, opcion_tarea, modelo_seleccionado, api_key)
        
        st.markdown(f'<div class="result-box"><h3>✨ Resultado de la Tarea: {opcion_tarea}</h3>', unsafe_allow_html=True) 
        
        with st.expander("Ver Respuesta Detallada", expanded=True):
            st.markdown(respuesta) 
            
        st.markdown('</div>', unsafe_allow_html=True)
        
elif not enviar and not prompt:
    st.caption("Esperando tu primera solicitud...")