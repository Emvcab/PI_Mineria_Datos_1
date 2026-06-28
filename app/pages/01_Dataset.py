import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Dataset", page_icon="🗂️", layout="wide")

# Ruta robusta: relativa a este archivo (funciona local y en Streamlit Cloud)
BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw" / "streaming_users_dirty.json"
CLEAN = BASE / "data" / "processed" / "streaming_users_clean.csv"
LOG = BASE / "logs" / "pipeline_log.csv"

st.title("🗂️ Dataset")

st.markdown("""
### Descripción general
El dataset contiene registros de usuarios de una plataforma de streaming, con información
demográfica (edad, país), de suscripción (plan), de comportamiento (tiempo de visualización
mensual, género favorito, último login) y de soporte (cantidad de tickets).
""")

@st.cache_data
def cargar():
    raw = pd.read_json(RAW)
    clean = pd.read_csv(CLEAN)
    log = pd.read_csv(LOG)
    return raw, clean, log

try:
    raw, clean, log = cargar()

    c1, c2, c3 = st.columns(3)
    c1.metric("Filas originales", f"{len(raw):,}")
    c2.metric("Filas finales", f"{len(clean):,}")
    c3.metric("Retención", f"{log['Retención (%)'].iloc[-1]:.1f} %")

    st.markdown("### Resumen de calidad inicial")
    st.markdown("""
    El dataset crudo presentaba: **160 duplicados** de `user_id`, **edades imposibles** (negativas
    y >100), **valores imposibles** en tiempo de visualización (99999) y tickets (99, 150),
    **categorías inconsistentes** (ej. `básico`/`BASICO`/`Basic`) y una columna de **fechas con
    formatos mezclados** y valores inválidos.
    """)

    st.markdown("### Principales transformaciones aplicadas")
    st.markdown("""
    - Eliminación de duplicados por `user_id`.
    - Normalización de planes, países y géneros a categorías canónicas.
    - Valores imposibles y valores imposibles → nulo → imputación por mediana según plan.
    - Winsorización de la cola alta real de tiempo de visualización (IQR k=3).
    - Parseo y validación de fechas (las no recuperables quedan como nulo).
    """)

    st.markdown("### Registro de transformaciones (log ETL)")
    st.dataframe(log, use_container_width=True)

    st.markdown("### Vista previa del dataset limpio")
    st.dataframe(clean.head(20), use_container_width=True)

except Exception as e:
    st.error(f"No se pudieron cargar los datos. Verificá que los archivos existan. Detalle: {e}")
