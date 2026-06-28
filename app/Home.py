import streamlit as st

st.set_page_config(
    page_title="PI Minería de Datos 1 — Usuarios de Streaming",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Análisis de Usuarios de una Plataforma de Streaming")
st.subheader("Proyecto Integrador — Minería de Datos 1")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### Información del proyecto
    - **Materia:** Minería de Datos 1
    - **Comisión:** Turno Tarde, Nodo
    - **Integrantes:** Emilio Cabaña
    - **Fecha:** Lunes 29 de Junio
    """)
with col2:
    st.markdown("""
    ### Enlaces
    - 🔗 **Repositorio GitHub:** _(completar con la URL pública)_
    - 📄 **Informe final:** disponible en `reports/informe_final.pdf`
    """)

st.markdown("---")

st.markdown("""
### Contexto

Este proyecto desarrolla un análisis de datos **reproducible y comunicable** sobre un dataset
de usuarios de una plataforma de streaming. El dataset original presentaba problemas de calidad
(valores faltantes, duplicados, categorías inconsistentes, valores imposibles y valores imposibles) que
fueron diagnosticados y corregidos con decisiones **justificadas por evidencia**.

El recorrido completo es: **inspección inicial → calidad y limpieza → análisis exploratorio (EDA)
→ escalamiento y PCA → conclusiones**. Cada etapa está documentada en su notebook correspondiente
y resumida en esta aplicación para público general.

Usá el menú lateral para navegar por las secciones: **Dataset**, **EDA**, **PCA** y **Conclusiones**.
""")

st.info("Esta aplicación comunica resultados para público general. La evidencia técnica completa "
        "está en el repositorio (notebooks, log ETL e informe).")
