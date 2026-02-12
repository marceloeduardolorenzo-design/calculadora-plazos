import streamlit as st
import pandas as pd
from datetime import date, timedelta

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Calculadora de Plazos", page_icon="📅")

st.title("📅 Calculadora de Plazos Administrativos")
st.markdown("---")

# LISTA DE FERIADOS ARGENTINA 2026 (Fijos, trasladables y puentes)
feriados_2026 = [
    "2026-01-01", "2026-02-16", "2026-02-17", "2026-03-23", 
    "2026-03-24", "2026-04-02", "2026-04-03", "2026-05-01", 
    "2026-05-25", "2026-06-15", "2026-06-20", "2026-07-09", 
    "2026-07-10", "2026-08-17", "2026-10-12", "2026-11-23", 
    "2026-12-07", "2026-12-08", "2026-12-25"
]
feriados_dt = pd.to_datetime(feriados_2026).date

# --- LÓGICA DEL NEGOCIO ---
def es_habil(fecha):
    """Devuelve True si es día hábil, False si es finde o feriado"""
    if fecha.weekday() >= 5: return False # 5=Sab, 6=Dom
    if fecha in feriados_dt: return False
    return True

def siguiente_dia_habil(fecha):
    """Busca el próximo día hábil a partir de una fecha dada"""
    fecha += timedelta(days=1)
    while not es_habil(fecha):
        fecha += timedelta(days=1)
    return fecha

def calcular_fecha_fin(fecha_inicio, dias_habiles):
    """Suma días hábiles considerando que el día de inicio CUENTA (restamos 1)"""
    if dias_habiles <= 0: return fecha_inicio
    
    # Restamos 1 porque la fecha de inicio es el "Día 1"
    dias_a_sumar = dias_habiles - 1
    dia_actual = fecha_inicio
    dias_contados = 0
    
    # Si por error el usuario pone inicio en un feriado, avanzamos al primer hábil
    # (Opcional: puedes quitar este bloque si prefieres que de error)
    while not es_habil(dia_actual):
         dia_actual += timedelta(days=1)

    while dias_contados < dias_a_sumar:
        dia_actual += timedelta(days=1)
        if es_habil(dia_actual):
            dias_contados += 1
            
    return dia_actual

# --- INTERFAZ ---
col1, col2 = st.columns(2)
with col1:
    fecha_base = st.date_input("Selecciona Fecha de Inicio", date(2026, 2, 18))
    
st.write("### Cronograma Calculado:")

# Definición de Etapas
etapas_data = [
    {"nombre": "Período de publicación", "dias": 7},
    {"nombre": "Período de presentación de postulantes", "dias": 5},
    {"nombre": "Periodo de evaluación", "dias": 10},
    {"nombre": "Período de notificación orden de mérito", "dias": 3},
    {"nombre": "Período de reconsideración", "dias": 2},
]

resultados = []
fecha_cursor = fecha_base

# Validación inicial visual
if not es_habil(fecha_base):
    st.error("⚠️ ¡Atención! La fecha de inicio seleccionada es un Sábado, Domingo o Feriado.")

for etapa in etapas_data:
    # 1. Calcular fin de la etapa actual
    fin = calcular_fecha_fin(fecha_cursor, etapa["dias"])
    
    resultados.append({
        "Etapa": etapa["nombre"],
        "Duración": f"{etapa['dias']} días",
        "Inicio": fecha_cursor.strftime('%d/%m/%Y (%A)'),
        "Fin": fin.strftime('%d/%m/%Y (%A)')
    })
    
    # 2. La siguiente etapa comienza el SIGUIENTE día hábil
    fecha_cursor = siguiente_dia_habil(fin)

# Mostrar Tabla
df = pd.DataFrame(resultados)
st.table(df)
