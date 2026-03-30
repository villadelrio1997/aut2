import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    layout="wide", 
    page_title="AUT2 - Murcia Copilot MVP", 
    page_icon="🚀"
)

# --- ESTILOS PARA SIMULAR LOS CUADRANTES ---
st.markdown("""
    <style>
    .stChatFloatingInputContainer {padding-bottom: 20px;}
    .reportview-container .main .block-container {padding-top: 1rem;}
    hr {margin: 10px 0px;}
    </style>
    """, unsafe_allow_html=True)

# --- ÁREA 1: CABECERA DE CONTROL (ARRIBA) ---
st.title("🚀 AUT2: Asistente de Programación Regional")
st.caption("Región de Murcia | Decreto 209/2022 | Nivel: Educación Primaria")

# Slider de Fases (El motor de la reactividad)
progreso = st.select_slider(
    "Fase del Flujo de Trabajo",
    options=["Contexto", "Planificación", "Diseño SdA", "Evaluación"],
    help="Mueve el slider para cambiar el modo de trabajo de todas las áreas."
)

st.divider()

# --- DEFINICIÓN DE COLUMNAS (ÁREAS 2, 3 Y 4) ---
col_recursos, col_lienzo, col_copiloto = st.columns([1, 2, 1], gap="medium")

# --- ÁREA 2: RECURSOS / INGESTA (IZQUIERDA) ---
with col_recursos:
    st.subheader("📚 Recursos")
    
    with st.container():
        if progreso == "Contexto":
            st.write("📂 **Gestor de Fuentes**")
            st.info("Sube los documentos base del centro escolar.")
            st.file_uploader("Arrastra PEC, Programación anterior...", accept_multiple_files=True)
            st.multiselect("Etiquetas de Centro", ["Línea 2", "Huerto Escolar", "Bilingüe", "Erasmus+"], ["Línea 2", "Huerto Escolar"])
            
        elif progreso == "Planificación":
            st.write("📅 **Curriculo y Tiempos**")
            st.selectbox("Materia", ["Ciencias de la Naturaleza", "Ciencias Sociales", "Lengua Castellana"])
            st.number_input("Sesiones totales del trimestre", 24, 60, 36)
            st.caption("Filtros del Decreto 209/2022 activados.")

        elif progreso == "Diseño SdA":
            st.write("🛠️ **Caja de Herramientas**")
            st.write("**Criterios (Murcia):**")
            st.checkbox("CE 3.1: Problemas ambientales", value=True)
            st.checkbox("CE 3.2: Soluciones sostenibles", value=True)
            st.divider()
            st.write("**Artefacto 6 (Metodologías):**")
            st.info("Sugerida: Aprendizaje-Servicio")
            st.button("Cambiar Metodología")

        elif progreso == "Evaluación":
            st.write("📋 **Panel de Calificación**")
            st.write("Instrumentos vinculados:")
            st.write("- Rúbrica de Producto (60%)")
            st.write("- Diario de Clase (40%)")
            st.button("Importar de Séneca/Plataforma")

# --- ÁREA 3: EL LIENZO (CENTRO) ---
with col_lienzo:
    st.subheader(f"📝 Espacio de Trabajo: {progreso}")
    
    with st.container():
        if progreso == "Contexto":
            st.markdown("### Perfil del Grupo y Centro")
            st.text_input("Nombre de la Situación (Opcional)", placeholder="Ej: Guardianes de la Huerta")
            st.text_area("Análisis del Contexto", "Centro ubicado en pedanía agrícola. Grupo de 4º con 25 alumnos. Nivel socioeconómico medio. Interés alto en actividades prácticas.")
            st.markdown("---")
            st.write("🎯 **Objetivos de Etapa vinculados:**")
            st.caption("- o) Valorar la higiene y la salud...")

        elif progreso == "Planificación":
            st.markdown("### Mapa de Saberes y Tiempos")
            st.table({
                "Unidad": ["U1: El ecosistema", "U2: Los seres vivos", "U3: Máquinas"],
                "Sesiones": [12, 12, 12],
                "Estado": ["Diseñada", "En borrador", "Pendiente"]
            })
            st.button("Reorganizar Calendario escolar")

        elif progreso == "Diseño SdA":
            st.markdown("### SdA: 'Misión Sostenible en la Huerta'")
            st.markdown("> **Reto:** Diseñar un sistema de riego por goteo con materiales reciclados.")
            
            tabs = st.tabs(["1. Motivación", "2. Investigación", "3. Acción", "4. Difusión"])
            with tabs[0]:
                st.write("Vídeo sobre la escasez de agua en la Cuenca del Segura.")
            with tabs[1]:
                st.write("Estudio de las necesidades hídricas de las hortalizas locales.")
            with tabs[2]:
                st.write("Construcción del prototipo en el huerto del colegio.")
            with tabs[3]:
                st.write("Exposición del sistema a los alumnos de 1º de Primaria.")

        elif progreso == "Evaluación":
            st.markdown("### Rúbrica Generada (Basada en Criterio 3.2)")
            st.markdown("""
            | Nivel | Descripción | Nota |
            |-------|-------------|------|
            | Excelente | Propone soluciones creativas y sostenibles | 10 |
            | Suficiente | Identifica el problema pero la solución es débil | 5 |
            """)
            st.button("💾 Exportar Memoria de Programación")

# --- ÁREA 4: COPILOTO IA (DERECHA) ---
with col_copiloto:
    st.subheader("🤖 Copiloto")
    
    # Sugerencia contextual arriba del chat
    mensajes_ayuda = {
        "Contexto": "He detectado que tu centro tiene huerto. ¿Quieres que priorice el Bloque 2 de Ciencias?",
        "Planificación": "Hay un festivo el 9 de junio. He ajustado las sesiones automáticamente.",
        "Diseño SdA": "¡Ojo! El Criterio 3.1 requiere una evidencia oral. ¿Añadimos un debate?",
        "Evaluación": "He preparado la adaptación DUA para el alumno con dificultades visuales."
    }
    st.info(mensajes_ayuda[progreso])
    
    # Simulación de Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("¿En qué puedo ayudarte?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analizando normativa..."):
                time.sleep(1)
                response = f"Como estamos en la fase de **{progreso}**, he revisado el Decreto 209/2022 y te sugiero..."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})