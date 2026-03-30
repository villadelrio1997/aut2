import streamlit as st
import json
from datetime import datetime

# -------------------------------
# Configuración de la página
# -------------------------------
st.set_page_config(page_title="Programación Docente - Cuadrantes Dinámicos", layout="wide")
st.title("📐 Gestor de Programación Docente (LOMLOE / Decreto 209 Murcia)")

# -------------------------------
# Inicialización de session_state
# -------------------------------
if "fase_actual" not in st.session_state:
    st.session_state.fase_actual = "Contexto"

if "datos_centro" not in st.session_state:
    st.session_state.datos_centro = {
        "nombre": "",
        "localidad": "",
        "codigo": "",
        "niveles": []
    }

if "perfil_grupo" not in st.session_state:
    st.session_state.perfil_grupo = {
        "num_alumnos": 20,
        "necesidades_especificas": "",
        "entorno_socioeconomico": "Medio",
        "puntos_fuertes": "",
        "puntos_debiles": ""
    }

# Simulación de JSON con criterios y saberes (basado en el decreto)
if "curriculum_json" not in st.session_state:
    st.session_state.curriculum_json = {
        "materia": "Ciencias de la Naturaleza",
        "curso": "4º de Primaria",
        "competencias_especificas": [
            {
                "id": "CE1",
                "texto": "Utilizar dispositivos y recursos digitales de forma segura...",
                "criterios": ["1.1. Utilizar dispositivos y recursos digitales..."]
            },
            {
                "id": "CE2",
                "texto": "Plantear y dar respuesta a cuestiones científicas sencillas...",
                "criterios": [
                    "2.1. Formular preguntas y realizar predicciones razonadas...",
                    "2.2. Buscar y seleccionar información...",
                    "2.3. Realizar experimentos guiados..."
                ]
            }
        ],
        "saberes_basicos": [
            "Iniciación a la actividad científica: observación, clasificación, experimentación.",
            "La vida en nuestro planeta: ecosistemas, biodiversidad, cadenas alimentarias.",
            "Materia, fuerzas y energía: mezclas, magnetismo, máquinas simples."
        ]
    }

if "rúbrica" not in st.session_state:
    st.session_state.rúbrica = {
        "criterio_1": {"porcentaje": 30, "niveles": ["Insuficiente", "Suficiente", "Notable", "Sobresaliente"]},
        "criterio_2": {"porcentaje": 40, "niveles": ["Insuficiente", "Suficiente", "Notable", "Sobresaliente"]},
        "criterio_3": {"porcentaje": 30, "niveles": ["Insuficiente", "Suficiente", "Notable", "Sobresaliente"]}
    }

# -------------------------------
# Funciones de renderizado por área
# -------------------------------
def render_control_superior():
    """Área 1: slider de fases (máquina de estados global)"""
    fases = ['Contexto', 'Planificación', 'Diseño SdA', 'Evaluación']
    idx = fases.index(st.session_state.fase_actual)
    seleccion = st.select_slider(
        "📌 Fase del proceso",
        options=fases,
        value=st.session_state.fase_actual,
        key="fase_slider"
    )
    if seleccion != st.session_state.fase_actual:
        st.session_state.fase_actual = seleccion
        st.rerun()

def render_columna_izquierda(fase):
    """Área 2 (columna izquierda): contenido según fase"""
    with st.container():
        st.subheader("📂 Recursos y metadatos")
        st.divider()
        
        if fase == "Contexto":
            st.markdown("#### 🏫 Datos del centro")
            st.session_state.datos_centro["nombre"] = st.text_input(
                "Nombre del centro",
                value=st.session_state.datos_centro["nombre"],
                key="ctx_nombre"
            )
            st.session_state.datos_centro["localidad"] = st.text_input(
                "Localidad",
                value=st.session_state.datos_centro["localidad"],
                key="ctx_localidad"
            )
            st.session_state.datos_centro["codigo"] = st.text_input(
                "Código de centro",
                value=st.session_state.datos_centro["codigo"],
                key="ctx_codigo"
            )
            uploaded_file = st.file_uploader("Subir documento de centro (PDF, DOCX)", type=["pdf", "docx"])
            if uploaded_file:
                st.success(f"Archivo '{uploaded_file.name}' cargado correctamente.")
                
        elif fase == "Planificación":
            st.markdown("#### 🗓️ Temporalización")
            st.number_input("Número de unidades didácticas", min_value=1, max_value=15, value=9, key="plan_ud")
            st.date_input("Inicio del curso", value=datetime(2025, 9, 15), key="plan_inicio")
            st.date_input("Fin del curso", value=datetime(2026, 6, 20), key="plan_fin")
            st.multiselect(
                "Distribución por trimestres",
                options=["1er trimestre", "2º trimestre", "3er trimestre"],
                default=["1er trimestre", "2º trimestre", "3er trimestre"],
                key="plan_trimestres"
            )
            
        elif fase == "Diseño SdA":
            st.markdown("#### 📋 Visor de currículo")
            with st.expander("📌 Competencias específicas y criterios", expanded=True):
                for ce in st.session_state.curriculum_json["competencias_especificas"]:
                    st.markdown(f"**{ce['id']}** – {ce['texto'][:80]}...")
                    for crit in ce["criterios"]:
                        st.markdown(f"- {crit}")
                    st.divider()
            with st.expander("🧠 Saberes básicos"):
                for saber in st.session_state.curriculum_json["saberes_basicos"]:
                    st.markdown(f"- {saber}")
                    
        elif fase == "Evaluación":
            st.markdown("#### 📊 Configuración de evaluación")
            st.info("Define aquí los instrumentos de evaluación (exámenes, rúbricas, listas de control...)")
            st.text_input("Nombre del instrumento", key="eval_instrumento")
            st.slider("Peso (%)", 0, 100, 50, key="eval_peso")

def render_columna_central(fase):
    """Área 3 (columna central): contenido principal según fase"""
    with st.container():
        if fase == "Contexto":
            st.subheader("👥 Perfil del grupo y entorno")
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.perfil_grupo["num_alumnos"] = st.number_input(
                    "Número de alumnos/as", min_value=1, max_value=40,
                    value=st.session_state.perfil_grupo["num_alumnos"], key="perf_num"
                )
                st.session_state.perfil_grupo["entorno_socioeconomico"] = st.selectbox(
                    "Nivel socioeconómico",
                    ["Bajo", "Medio-bajo", "Medio", "Medio-alto", "Alto"],
                    index=2, key="perf_entorno"
                )
            with col2:
                st.session_state.perfil_grupo["necesidades_especificas"] = st.text_area(
                    "Necesidades específicas de apoyo educativo",
                    value=st.session_state.perfil_grupo["necesidades_especificas"],
                    key="perf_necesidades"
                )
            st.session_state.perfil_grupo["puntos_fuertes"] = st.text_area(
                "Puntos fuertes del grupo", key="perf_fuertes"
            )
            st.session_state.perfil_grupo["puntos_debiles"] = st.text_area(
                "Puntos débiles o áreas de mejora", key="perf_debiles"
            )
            st.divider()
            st.markdown("#### 🌍 Análisis del entorno")
            st.text_area("Recursos del entorno (bibliotecas, museos, empresas, naturaleza...)")
            
        elif fase == "Planificación":
            st.subheader("📅 Secuenciación y unidades")
            st.divider()
            st.markdown("**Distribución de unidades por trimestre**")
            tabs = st.tabs(["1er trimestre", "2º trimestre", "3er trimestre"])
            with tabs[0]:
                st.text_area("Unidades didácticas (1er trimestre)", placeholder="UD1: ...\nUD2: ...")
            with tabs[1]:
                st.text_area("Unidades didácticas (2º trimestre)")
            with tabs[2]:
                st.text_area("Unidades didácticas (3er trimestre)")
            st.divider()
            st.markdown("**Conexiones interdisciplinares**")
            st.multiselect("Áreas con las que se relaciona", 
                           ["Matemáticas", "Lengua", "Educación Física", "Plástica", "Música", "Valores"])
            
        elif fase == "Diseño SdA":
            st.subheader("🧩 Situación de Aprendizaje (SdA)")
            st.divider()
            tabs_sda = st.tabs(["📖 Inicio / Motivación", "⚙️ Desarrollo / Actividades", "🏆 Producto final"])
            with tabs_sda[0]:
                st.text_area("Contexto y situación real", placeholder="¿Qué problema o reto se plantea?")
                st.text_area("Pregunta guía o desafío")
            with tabs_sda[1]:
                st.text_area("Secuencia de actividades", height=200)
                st.markdown("**Agrupamientos:**")
                st.checkbox("Trabajo individual")
                st.checkbox("Parejas")
                st.checkbox("Pequeños grupos")
                st.checkbox("Gran grupo")
            with tabs_sda[2]:
                st.text_input("Nombre del producto final", placeholder="Ej. Infografía, maqueta, exposición...")
                st.text_area("Criterios de calidad del producto")
                
        elif fase == "Evaluación":
            st.subheader("📋 Tabla de rúbricas y pesos")
            st.divider()
            st.markdown("#### Matriz de evaluación (porcentajes)")
            # Representación visual de rúbricas y pesos
            for key, val in st.session_state.rúbrica.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{key.replace('_', ' ').title()}**")
                    st.caption(" | ".join(val["niveles"]))
                with col2:
                    nuevo_peso = st.number_input("Peso (%)", min_value=0, max_value=100,
                                                 value=val["porcentaje"], key=f"peso_{key}", step=5)
                    st.session_state.rúbrica[key]["porcentaje"] = nuevo_peso
                st.divider()
            # Gráfico de barras simple con st.progress
            total = sum(v["porcentaje"] for v in st.session_state.rúbrica.values())
            st.metric("Suma total de pesos", f"{total}%", delta=None)
            if total != 100:
                st.warning("⚠️ La suma de los pesos debe ser 100%.")
            else:
                st.success("✅ Distribución correcta")
                
def render_columna_derecha(fase):
    """Área 4 (columna derecha): mensajes de ayuda contextuales"""
    with st.container():
        st.subheader("💡 Ayuda y recursos")
        st.divider()
        if fase == "Contexto":
            st.info("📌 **Contexto**: Completa los datos del centro y el perfil del grupo. Estos datos se guardan automáticamente.")
            st.markdown("""
            - El **nombre del centro** y la **localidad** son obligatorios.
            - El **perfil del grupo** debe reflejar las características reales del alumnado.
            - El **análisis del entorno** ayuda a conectar el aprendizaje con la realidad.
            """)
        elif fase == "Planificación":
            st.info("📌 **Planificación**: Organiza temporalmente las unidades y establece conexiones interdisciplinares.")
            st.markdown("""
            - Define el número de unidades didácticas y su distribución trimestral.
            - Asegúrate de que la temporalización sea realista.
            - Las conexiones con otras áreas enriquecen las situaciones de aprendizaje.
            """)
        elif fase == "Diseño SdA":
            st.info("📌 **Diseño de SdA**: Crea una Situación de Aprendizaje completa.")
            st.markdown("""
            - **Inicio**: Plantea un reto significativo y cercano al alumnado.
            - **Desarrollo**: Secuencia actividades variadas (individuales, cooperativas, digitales).
            - **Producto final**: Define un producto tangible que evidencie el aprendizaje.
            """)
        elif fase == "Evaluación":
            st.info("📌 **Evaluación**: Define criterios, instrumentos y pesos.")
            st.markdown("""
            - Utiliza rúbricas para evaluar competencias.
            - Ajusta los pesos porcentuales para que sumen 100%.
            - Combina diferentes instrumentos (observación, pruebas, portfolios).
            """)
        st.divider()
        st.caption(f"Fase actual: **{fase}**")
        st.caption("Los datos se guardan automáticamente al navegar entre fases.")

# -------------------------------
# Construcción del layout principal
# -------------------------------
# Área 1: Control superior
render_control_superior()
st.divider()

# Áreas 2, 3, 4 en tres columnas
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_left:
    render_columna_izquierda(st.session_state.fase_actual)

with col_center:
    render_columna_central(st.session_state.fase_actual)

with col_right:
    render_columna_derecha(st.session_state.fase_actual)

# Pie de página opcional
st.divider()
st.caption("Aplicación basada en la Arquitectura de Cuadrantes Dinámicos | Compatible con Decreto 209/2022 (Murcia)")