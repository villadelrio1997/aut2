import streamlit as st
import time

# Configuración de la página (Ancho completo)
st.set_page_config(layout="wide", page_title="AUT2 - Murcia Copilot MVP", page_icon="🚀")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .area-box {
        border: 1px solid #dcdcdc;
        border-radius: 10px;
        padding: 15px;
        background-color: #f9f9f9;
        min-height: 400px;
    }
    .stProgress > div > div > div > div {
        background-color: #2e7d32;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA Y ESTADO (ÁREA 1) ---
st.title("🚀 AUT2: Asistente de Programación Regional")
st.caption("Región de Murcia - Decreto 209/2022 | Nivel: Primaria")

# Barra de progreso de la Programación
progreso = st.sidebar.select_slider(
    "Fase de la Programación",
    options=["Contexto", "Planificación", "Diseño SdA", "Evaluación"],
    value="Diseño SdA"
)

# --- LAYOUT DE 3 COLUMNAS (ÁREAS 2, 3 y 4) ---
col_recursos, col_lienzo, col_copiloto = st.columns([1, 2, 1])

# --- ÁREA 2: GESTOR DE RECURSOS (Izquierda) ---
with col_recursos:
    st.subheader("📚 Recursos")
    with st.container(border=True):
        st.write("**Materia:** Ciencias de la Naturaleza")
        st.write("**Curso:** 4.º Primaria")
        
        tab1, tab2 = st.tabs(["Currículo", "Metodologías"])
        
        with tab1:
            st.success("✅ Criterio 3.1: Identificar problemas ambientales...")
            st.success("✅ Criterio 3.2: Propuestas de conservación...")
            st.caption("Descriptores: STEM2, CD1, CC1")
        
        with tab2:
            st.info("💡 Metodología: Aprendizaje-Servicio")
            st.info("💡 Producto: Sistema de Riego Reciclado")

# --- ÁREA 3: LIENZO DE TRABAJO (Centro) ---
with col_lienzo:
    st.subheader(f"📝 {progreso}") # El título cambia según el slider
    
    container = st.container()
    with container:
        if progreso == "Contexto":
            st.info("🎯 Configuración del entorno de aprendizaje")
            col_cent1, col_cent2 = st.columns(2)
            col_cent1.text_input("Nombre del Centro", value="CEIP Huerta de Murcia")
            col_cent2.multiselect("Prioridades PEC", ["Medio Ambiente", "Digitalización", "Inclusión"], ["Medio Ambiente"])
            st.text_area("Descripción del grupo", "4º Primaria, 25 alumnos, 2 ACNEAE...")

        elif progreso == "Planificación":
            st.write("📅 **Cronograma Trimestral**")
            st.table({
                "Unidad": ["U1: Los Seres Vivos", "U2: La Energía", "U3: Materia"],
                "Semanas": ["1-4", "5-8", "9-12"],
                "Criterios": ["3.1, 3.2", "4.1", "1.1"]
            })

        elif progreso == "Diseño SdA":
            st.markdown("### Reto: 'Misión Sostenible'")
            fases_sda = st.tabs(["1. Inicio", "2. Desarrollo", "3. Producto"])
            with fases_sda[0]:
                st.write("• Asamblea sobre residuos en el Segura.")
            with fases_sda[1]:
                st.write("• Taller de reciclaje y diseño de riego.")
            with fases_sda[2]:
                st.write("• Prototipo funcional en el huerto escolar.")

        elif progreso == "Evaluación":
            st.write("📊 **Matriz de Evaluación Normativa**")
            st.checkbox("Criterio 3.1 - Observación directa (40%)", value=True)
            st.checkbox("Criterio 3.2 - Producto final (60%)", value=True)
            st.button("Generar Informe PDF oficial")
# --- ÁREA 4: COPILOTO IA (Derecha) ---
with col_copiloto:
    st.subheader("🤖 Copiloto")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hola Manuel, he analizado el Decreto 209/2022 y tu contexto. ¿Quieres que ajustemos el reto de la Huerta para incluir una actividad DUA?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Escribe aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.spinner("Consultando normativa y base metodológica..."):
            time.sleep(2) # Simulación de pensamiento
            respuesta = "Hecho. He añadido una 'Estación de Audio' para la investigación (Pauta DUA 1.1) y he vinculado el Criterio 3.2 de la Región de Murcia. ¿Te parece bien?"
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
            st.chat_message("assistant").write(respuesta)
            st.balloons() # Efecto visual para la presentación