import streamlit as st

st.set_page_config(page_title="Conclusiones", page_icon="✅", layout="wide")

st.title("✅ Conclusiones")

st.markdown("""
### Hallazgos principales

- **Calidad de datos:** el dataset crudo tenía problemas en las 8 columnas (duplicados, valores
  imposibles, valores imposibles, categorías inconsistentes, fechas inválidas). Tras la limpieza se conservó
  cerca del **98%** de las filas, con pérdida concentrada solo en duplicados documentados.
- **Comportamiento de usuarios:** la base es de adultos jóvenes (mediana ~33 años). El **plan de
  suscripción es el principal determinante del consumo** (Premium ≈ doble que Básico). La **edad no
  influye** en cuánto mira una persona. La preferencia de género es transversal al plan y al país.
- **Estructura de variables (PCA):** las variables numéricas son **independientes** (cada componente
  ~33%), por lo que no es posible reducir dimensiones sin perder información.
""")

st.markdown("""
### Limitaciones

- El alcance de las conclusiones está condicionado por la información disponible y por las decisiones
  documentadas durante el proceso.
- La independencia casi total entre variables sugiere un posible **origen sintético** del dataset, lo
  que limita la generalización de las relaciones observadas.
- La imputación por mediana reduce levemente la varianza real de las variables intervenidas.
- Quedaron fechas de último login sin recuperar (no se imputaron para no inventar datos), lo que limita
  cualquier análisis de actividad temporal.
- No existe una variable objetivo (ej. baja del servicio), por lo que no se evaluó capacidad predictiva.
""")

st.markdown("""
### Próximos pasos (mejoras futuras)

- Incorporar información adicional (variable objetivo, actividad temporal) para ampliar el alcance del
  análisis hacia un enfoque predictivo.
- Probar métodos de imputación más sofisticados (KNN, imputación múltiple) y comparar su impacto.
- Aplicar técnicas de agrupamiento (clustering) sobre las variables escaladas para detectar segmentos
  de usuarios no evidentes.
- Reforzar la validación en origen (reglas de carga) para reducir la limpieza posterior.
""")

st.markdown("---")
st.markdown("🔗 **Repositorio GitHub:** _(completar)_  |  📄 **Informe final:** `reports/informe_final.pdf`")
