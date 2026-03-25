import streamlit as st
from fpdf import FPDF
from datetime import datetime
import base64

# --- CONFIGURACIÓN DE PANTALLA ---
st.set_page_config(page_title="MENFA WELL SIM V13 - CERTIFICATION", layout="wide")

# --- FUNCIÓN PARA GENERAR EL PDF ---
def crear_certificado(nombre_usuario, puntaje):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # Marco estético
    pdf.set_line_width(2)
    pdf.rect(10, 10, 277, 190)
    
    # Encabezado
    pdf.set_font('Arial', 'B', 30)
    pdf.cell(0, 40, 'CERTIFICADO DE COMPETENCIA', ln=True, align='C')
    
    pdf.set_font('Arial', '', 18)
    pdf.cell(0, 20, 'El proyecto educativo MENFA certifica que:', ln=True, align='C')
    
    # Nombre del Estudiante
    pdf.set_font('Arial', 'B', 25)
    pdf.cell(0, 30, nombre_usuario.upper(), ln=True, align='C')
    
    # Cuerpo del mensaje
    pdf.set_font('Arial', '', 16)
    texto = (f"Ha completado con éxito el Simulador de Cabina de Perforación v13.0, "
             f"demostrando conocimientos avanzados en Martin-Decker, Control de Pozos "
             f"y Operaciones de Cementación con un puntaje de {puntaje}%.")
    pdf.multi_cell(0, 10, texto, align='C')
    
    # Fecha y Firma (Simulada)
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    pdf.ln(20)
    pdf.set_font('Arial', 'I', 12)
    pdf.cell(0, 10, f"Emitido en Mendoza, Argentina - Fecha: {fecha_actual}", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ FINAL ---
st.title("🏆 MÓDULO DE GRADUACIÓN Y CERTIFICACIÓN")

# Requisito de nombre
nombre = st.text_input("Ingrese su nombre completo para el certificado:", placeholder="Ej: Juan Pérez")

# Simulación de puntaje del examen anterior
score_final = st.session_state.get('score', 0)
total_preguntas = 3 # Según el examen de la V12
porcentaje = int((score_final / total_preguntas) * 100) if total_preguntas > 0 else 0

st.metric("Tu Calificación Final", f"{porcentaje}%")

if porcentaje >= 100:
    st.success("¡Felicidades! Has alcanzado la excelencia técnica.")
    if nombre:
        pdf_data = crear_certificado(nombre, porcentaje)
        st.download_button(
            label="🎓 DESCARGAR MI CERTIFICADO (PDF)",
            data=pdf_data,
            file_name=f"Certificado_MENFA_{nombre.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Por favor, ingresa tu nombre para habilitar la descarga.")
else:
    st.error("Necesitas un puntaje del 100% en el examen para obtener la certificación.")
    st.info("Regresa a la pestaña de EXAMEN y revisa tus respuestas.")

# --- BARRA LATERAL DE PROYECTO ---
with st.sidebar:
    st.header("MENFA Project v13")
    st.write("Responsable: Fabricio")
    st.write("Estado: Listo para Implementación")
    st.divider()
    st.caption("Este simulador es propiedad intelectual del proyecto educativo MENFA.")
import streamlit as st
import random

# --- CONFIGURACIÓN DE PANTALLA ---
st.set_page_config(page_title="MENFA WELL SIM V12 - EXAM MODE", layout="wide")

# --- BANCO DE PREGUNTAS (Basado en tus clases) ---
def generar_trivia():
    preguntas = [
        {
            "id": 1,
            "q": "¿Qué sucede con el Martin-Decker (Hook Load) cuando apoyas peso (WOB) en el fondo?",
            "options": ["Aumenta la carga", "Disminuye la carga", "Se mantiene igual"],
            "correct": "Disminuye la carga",
            "ref": "Clase 3: El peso se transfiere de la sarta al trépano."
        },
        {
            "id": 2,
            "q": "Si el volumen en los tanques (Pit Level) aumenta sin bombear, ¿qué indica?",
            "options": ["Pérdida de circulación", "Un Kick o Surgencia", "Falla en las zarandas"],
            "correct": "Un Kick o Surgencia",
            "ref": "Clase 4: Entrada de fluidos de formación al pozo."
        },
        {
            "id": 3,
            "q": "Para calcular el volumen de cemento, ¿qué diámetro es el más crítico?",
            "options": ["Diámetro Interno (ID) del Casing", "Espacio Anular (Hoyo vs OD Casing)", "Diámetro del Drill Pipe"],
            "correct": "Espacio Anular (Hoyo vs OD Casing)",
            "ref": "Clase 5: El cemento debe llenar el espacio tras el Casing."
        }
    ]
    return preguntas

# --- INTERFAZ DEL EXAMEN ---
st.title("🎓 EVALUACIÓN DE COMPETENCIAS TÉCNICAS")

if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.answered = []

tab_sim, tab_exam = st.tabs(["🕹️ SIMULADOR ACTIVO", "📝 EXAMEN FINAL"])

with tab_sim:
    st.info("Continúa operando para recolectar datos...")
    st.metric("Profundidad Actual", f"{st.session_state.get('md', 3500)} m")
    st.warning("Recuerda: El reporte IADC es la base de tu evaluación.")

with tab_exam:
    st.subheader("Cuestionario de Certificación MENFA")
    
    preguntas = generar_trivia()
    
    for p in preguntas:
        st.write(f"**{p['id']}. {p['q']}**")
        ans = st.radio(f"Seleccione una opción para la preg. {p['id']}:", p['options'], key=f"q_{p['id']}")
        
        if st.button(f"Validar Respuesta {p['id']}"):
            if ans == p['correct']:
                st.success(f"¡Correcto! {p['ref']}")
                if p['id'] not in st.session_state.answered:
                    st.session_state.score += 1
                    st.session_state.answered.append(p['id'])
            else:
                st.error("Incorrecto. Revisa el material de la clase.")

    st.divider()
    st.metric("Puntaje Total", f"{st.session_state.score} / {len(preguntas)}")
    
    if st.session_state.score == len(preguntas):
        st.balloons()
        st.success("🎉 ¡Certificación MENFA Aprobada! Estás listo para el Rig Floor.")
        
