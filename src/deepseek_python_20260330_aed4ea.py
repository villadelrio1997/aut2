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

# Datos del centro
if "datos_centro" not in st.session_state:
    st.session_state.datos_centro = {
        "nombre": "",
        "localidad": "",
        "codigo": "",
        "niveles": []
    }

# Perfil del grupo
if "perfil_grupo" not in st.session_state:
    st.session_state.perfil_grupo = {
        "num_alumnos": 20,
        "necesidades_especificas": "",
        "entorno_socioeconomico": "Medio",
        "puntos_fuertes": "",
        "puntos_debiles": ""
    }

# Planificación
if "planificacion" not in st.session_state:
    st.session_state.planificacion = {
        "num_ud": 9,
        "inicio_curso": datetime(2025, 9, 15),
        "fin_curso": datetime(2026, 6, 20),
        "trimestres": ["1er trimestre", "2º trimestre", "3er trimestre"],
        "unidades_trim1": "",
        "unidades_trim2": "",
        "unidades_trim3": "",
        "conexiones": []
    }

# Diseño SdA
if "diseno_sda" not in st.session_state:
    st.session_state.diseno_sda = {
        "contexto": "",
        "pregunta": "",
        "actividades": "",
        "agrupamientos": {"individual": False, "parejas": False, "pequenos_grupos": False, "gran_grupo": False},
        "producto_nombre": "",
        "criterios_producto": ""
    }

# Evaluación
if "evaluacion" not in st.session_state:
    st.session_state.evaluacion = {
        "rubrica": {
            "criterio_1": {"porcentaje": 30, "niveles": ["Insuficiente", "Suficiente", "Notable", "Sobresaliente"]},
            "criterio_2": {"porcentaje": 40, "niveles": ["Insuficiente", "Suficiente", "Notable", "Sobresaliente"]},
            "criterio_3": {"porcentaje": 30, "niveles": ["Insuficiente", "Suficiente", "Notable", "Sobresaliente"]}
        },
        "instrumentos": []
    }

# Documento editable (para la fase Validación)
if "documento_texto" not in st.session_state:
    st.session_state.documento_texto = ""

# Historial del chat (fase Validación)
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [{"role": "assistant", "content": "Hola, soy tu asistente de redacción. Puedes pedirme sugerencias para mejorar el documento."}]

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

# -------------------------------
# Funciones auxiliares
# -------------------------------
def generar_borrador_desde_fases():
    """Genera un documento en Markdown a partir de los datos recogidos en las fases."""
    centro = st.session_state.datos_centro
    perfil = st.session_state.perfil_grupo
    plan = st.session_state.planificacion
    diseno = st.session_state.diseno_sda
    eval_data = st.session_state.evaluacion

    doc = f"""# Programación Didáctica - {centro['nombre']}

## 1. Contexto
- **Centro:** {centro['nombre']} ({centro['localidad']}) - Código: {centro['codigo']}
- **Nivel:** Educación Primaria
- **Grupo:** {perfil['num_alumnos']} alumnos/as
- **Nivel socioeconómico:** {perfil['entorno_socioeconomico']}
- **Necesidades específicas:** {perfil['necesidades_especificas']}
- **Puntos fuertes:** {perfil['puntos_fuertes']}
- **Puntos débiles:** {perfil['puntos_debiles']}

## 2. Planificación
- **Número de unidades didácticas:** {plan['num_ud']}
- **Periodo:** {plan['inicio_curso'].strftime('%d/%m/%Y')} - {plan['fin_curso'].strftime('%d/%m/%Y')}
- **Distribución trimestral:** {', '.join(plan['trimestres'])}
- **Unidades por trimestre:**
  - **1er trimestre:** {plan['unidades_trim1']}
  - **2º trimestre:** {plan['unidades_trim2']}
  - **3er trimestre:** {plan['unidades_trim3']}
- **Conexiones interdisciplinares:** {', '.join(plan['conexiones'])}

## 3. Situación de Aprendizaje (SdA)
### Contexto y motivación
{diseno['contexto']}

### Pregunta guía
{diseno['pregunta']}

### Actividades
{diseno['actividades']}

### Agrupamientos
- Trabajo individual: {'Sí' if diseno['agrupamientos']['individual'] else 'No'}
- Parejas: {'Sí' if diseno['agrupamientos']['parejas'] else 'No'}
- Pequeños grupos: {'Sí' if diseno['agrupamientos']['pequenos_grupos'] else 'No'}
- Gran grupo: {'Sí' if diseno['agrupamientos']['gran_grupo'] else 'No'}

### Producto final
**Nombre:** {diseno['producto_nombre']}
**Criterios de calidad:** {diseno['criterios_producto']}

## 4. Evaluación
### Rúbrica y pesos
| Criterio | Peso (%) | Niveles |
|----------|----------|---------|
"""
    for key, val in eval_data['rubrica'].items():
        doc += f"| {key.replace('_', ' ').title()} | {val['porcentaje']} | {' | '.join(val['niveles'])} |\n"

    doc += f"""
### Instrumentos de evaluación
{', '.join(eval_data['instrumentos']) if eval_data['instrumentos'] else 'No definidos'}

---
*Documento generado automáticamente a partir de los datos introducidos en las fases anteriores.*
"""
    return doc

def sincronizar_documento():
    """Actualiza el documento editable con el borrador generado."""
    st.session_state.documento_texto = generar_borrador_desde_fases()

# -------------------------------
# Funciones de renderizado por fase (mantenemos las existentes)
# -------------------------------
def render_control_superior():
    """Área 1: slider de fases (máquina de estados global)"""
    fases = ['Contexto', 'Planificación', 'Diseño SdA', 'Evaluación', 'Validación']
    idx = fases.index(st.session_state.fase_actual)
    seleccion = st.select_slider(
        "📌 Fase del proceso",
        options=fases,
        value=st.session_state.fase_actual,
        key="fase_slider"
    )
    if seleccion != st.session_state.fase_actual:
        st.session_state.fase_actual = seleccion
        # Si entramos en Validación y el documento está vacío, lo generamos
        if seleccion == "Validación" and not st.session_state.documento_texto:
            sincronizar_documento()
        st.rerun()

# --- Funciones para cada fase (simplificadas para centrarnos en la nueva fase) ---
def render_columna_izquierda_contexto():
    with st.container():
        st.subheader("📂 Recursos y metadatos")
        st.divider()
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

def render_columna_central_contexto():
    with st.container():
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

def render_columna_derecha_contexto():
    with st.container():
        st.subheader("💡 Ayuda y recursos")
        st.divider()
        st.info("📌 **Contexto**: Completa los datos del centro y el perfil del grupo. Estos datos se guardan automáticamente.")
        st.markdown("""
        - El **nombre del centro** y la **localidad** son obligatorios.
        - El **perfil del grupo** debe reflejar las características reales del alumnado.
        - El **análisis del entorno** ayuda a conectar el aprendizaje con la realidad.
        """)

# (Se omiten las funciones de Planificación, Diseño SdA y Evaluación por brevedad, pero se mantienen en el código real)
# ... [resto de funciones de renderizado de las otras fases] ...

# -------------------------------
# Nuevas funciones para la fase Validación
# -------------------------------
def render_columna_izquierda_validacion():
    """Área izquierda: texto editable"""
    with st.container():
        st.subheader("📝 Editar documento")
        st.divider()
        st.markdown("**Puedes modificar directamente el texto del documento.**")
        nuevo_texto = st.text_area(
            "Contenido del documento",
            value=st.session_state.documento_texto,
            height=500,
            key="texto_editable"
        )
        if nuevo_texto != st.session_state.documento_texto:
            st.session_state.documento_texto = nuevo_texto
        if st.button("🔄 Sincronizar desde fases anteriores"):
            sincronizar_documento()
            st.success("Documento actualizado con los datos de las fases anteriores.")
        st.caption("Puedes editar el texto libremente. El asistente te ayudará a mejorarlo.")

def render_columna_central_validacion():
    """Área central: chat interactivo"""
    with st.container():
        st.subheader("💬 Asistente de redacción")
        st.divider()
        # Mostrar historial del chat
        for msg in st.session_state.chat_messages:
            st.chat_message(msg["role"]).write(msg["content"])
        # Input del usuario
        prompt = st.chat_input("Escribe tu pregunta o sugerencia...")
        if prompt:
            # Añadir mensaje del usuario
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            # Generar respuesta simulada
            respuesta = generar_respuesta_asistente(prompt, st.session_state.documento_texto)
            st.session_state.chat_messages.append({"role": "assistant", "content": respuesta})
            st.rerun()
        # Botón para aplicar sugerencia (por ejemplo, la última respuesta)
        if st.session_state.chat_messages and st.session_state.chat_messages[-1]["role"] == "assistant":
            ultima_respuesta = st.session_state.chat_messages[-1]["content"]
            if st.button("📋 Aplicar sugerencia al documento"):
                # Añadimos la sugerencia al final del texto editable
                st.session_state.documento_texto += f"\n\n**Sugerencia del asistente:**\n{ultima_respuesta}"
                st.success("Sugerencia aplicada. Revisa el documento editable.")
                st.rerun()

def generar_respuesta_asistente(pregunta, documento_actual):
    """Genera una respuesta simulada basada en patrones simples."""
    pregunta_lower = pregunta.lower()
    if "mejora" in pregunta_lower and "redacción" in pregunta_lower:
        return "Te sugiero revisar la estructura del documento: introduce títulos más claros, utiliza viñetas para listas y asegura que los párrafos sean breves. ¿Quieres que te muestre un ejemplo?"
    elif "añade" in pregunta_lower and "actividades" in pregunta_lower:
        return "Puedes incluir actividades variadas: trabajo cooperativo, experimentos, uso de TIC, salidas al entorno. Por ejemplo, añade una actividad de indagación científica en la fase de Desarrollo."
    elif "evaluación" in pregunta_lower:
        return "Para mejorar la evaluación, considera rúbricas con indicadores claros, autoevaluación del alumnado y coevaluación. ¿Quieres que te proponga un ejemplo de rúbrica?"
    elif "producto final" in pregunta_lower:
        return "El producto final debe ser significativo y demostrar las competencias. Puedes pedir una infografía, una presentación oral, un prototipo, etc. ¿Necesitas ayuda para definir los criterios de calidad?"
    else:
        return "No tengo una sugerencia específica para esa consulta. Puedes pedirme ayuda para mejorar la redacción, añadir actividades, afinar la evaluación o definir el producto final."

def render_columna_derecha_validacion():
    """Área derecha: vista previa Markdown y descarga"""
    with st.container():
        st.subheader("📄 Vista previa (Markdown)")
        st.divider()
        st.markdown(st.session_state.documento_texto, unsafe_allow_html=False)
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Descargar documento (Markdown)"):
                with open("programacion_didactica.md", "w", encoding="utf-8") as f:
                    f.write(st.session_state.documento_texto)
                st.success("Descargado como 'programacion_didactica.md'")
        with col2:
            if st.button("✅ Generar documento final"):
                st.success("Documento final listo para imprimir. Revisa la vista previa y descarga el archivo.")

# -------------------------------
# Función principal de renderizado por fase
# -------------------------------
def render_by_fase(fase):
    if fase == "Contexto":
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_left:
            render_columna_izquierda_contexto()
        with col_center:
            render_columna_central_contexto()
        with col_right:
            render_columna_derecha_contexto()
    elif fase == "Planificación":
        # ... (implementación similar, omitida por brevedad)
        pass
    elif fase == "Diseño SdA":
        # ... (omitida)
        pass
    elif fase == "Evaluación":
        # ... (omitida)
        pass
    elif fase == "Validación":
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_left:
            render_columna_izquierda_validacion()
        with col_center:
            render_columna_central_validacion()
        with col_right:
            render_columna_derecha_validacion()

# -------------------------------
# Construcción del layout principal
# -------------------------------
render_control_superior()
st.divider()
render_by_fase(st.session_state.fase_actual)

# Pie de página
st.divider()
st.caption("Aplicación basada en la Arquitectura de Cuadrantes Dinámicos | Compatible con Decreto 209/2022 (Murcia)")