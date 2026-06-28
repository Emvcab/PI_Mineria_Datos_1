import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="EDA", page_icon="📈", layout="wide")

BASE = Path(__file__).resolve().parent.parent.parent
CLEAN = BASE / "data" / "processed" / "streaming_users_clean.csv"

st.title("📈 Análisis Exploratorio (EDA)")
st.markdown("Cinco visualizaciones sobre el dataset limpio: 2 univariadas, 2 bivariadas y 1 multivariada. "
            "Cada una con su interpretación de negocio.")

@st.cache_data
def cargar():
    return pd.read_csv(CLEAN)

df = cargar()
orden = ["Básico", "Estándar", "Premium"]

# ---------- 1. Univariada: edad ----------
st.markdown("## 1. Distribución de edades (univariada)")
fig1 = px.histogram(df, x="age", nbins=30, title="Distribución de edades")
fig1.update_layout(xaxis_title="Edad", yaxis_title="Usuarios", bargap=0.05)
st.plotly_chart(fig1, use_container_width=True)
st.info("**Interpretación:** la base se concentra en adultos jóvenes (mediana ~33 años). "
        "No es un servicio dominado por adolescentes ni adultos mayores: el marketing debería "
        "apuntar a ese público adulto-joven, que es el grueso real de clientes.")

# ---------- 2. Univariada: watch_time ----------
st.markdown("## 2. Tiempo de visualización mensual (univariada)")
fig2 = px.histogram(df, x="monthly_watch_time_mins", nbins=40,
                    title="Distribución del tiempo de visualización", color_discrete_sequence=["seagreen"])
fig2.update_layout(xaxis_title="Minutos / mes", yaxis_title="Usuarios", bargap=0.05)
st.plotly_chart(fig2, use_container_width=True)
st.info("**Interpretación:** el consumo típico ronda los ~770 min/mes (≈13 h), con una cola de "
        "usuarios muy intensos. Ese grupo de alto consumo es el más fiel y el que conviene retener.")

# Medidas de dispersión y forma (no es una visualización: es una tabla resumen)
st.markdown("### Medidas de dispersión y forma")
num_cols = ["age", "monthly_watch_time_mins", "customer_support_tickets"]
resumen_forma = pd.DataFrame({
    "media": [df[c].mean() for c in num_cols],
    "desvío": [df[c].std() for c in num_cols],
    "CV (%)": [df[c].std() / df[c].mean() * 100 for c in num_cols],
    "asimetría": [df[c].skew() for c in num_cols],
    "curtosis": [df[c].kurt() for c in num_cols],
}, index=num_cols).round(2)
st.dataframe(resumen_forma, use_container_width=True)
st.info("**Interpretación:** `tickets` es la variable más heterogénea (CV ~111%). El consumo y los "
        "tickets tienen asimetría positiva alta (cola a la derecha), lo que justifica describirlos e "
        "imputarlos con la mediana en lugar de la media. El consumo es además leptocúrtico (colas "
        "pesadas por los super-usuarios).")

# ---------- 3. Bivariada: plan vs tiempo ----------
st.markdown("## 3. Plan vs tiempo de uso (bivariada)")
fig3 = px.box(df, x="subscription_plan", y="monthly_watch_time_mins",
              category_orders={"subscription_plan": orden},
              title="Tiempo de visualización según plan", color="subscription_plan",
              color_discrete_sequence=px.colors.sequential.Blues[3:])
fig3.update_layout(xaxis_title="Plan", yaxis_title="Minutos / mes", showlegend=False)
st.plotly_chart(fig3, use_container_width=True)
st.info("**Interpretación:** los usuarios Premium consumen casi el doble que los Básico "
        "(≈1123 vs ≈587 min/mes). Quien paga más, mira más. Ofrecer upgrades a usuarios Básico "
        "de alto consumo podría aumentar ingresos: ya tienen el hábito.")

# ---------- 4. Bivariada: plan vs país ----------
st.markdown("## 4. Distribución de planes por país (bivariada)")
ct = pd.crosstab(df["country"], df["subscription_plan"])[orden].reset_index()
ct_long = ct.melt(id_vars="country", var_name="Plan", value_name="Usuarios")
fig4 = px.bar(ct_long, x="country", y="Usuarios", color="Plan", barmode="group",
              category_orders={"Plan": orden}, title="Planes por país")
fig4.update_layout(xaxis_title="País", yaxis_title="Usuarios")
st.plotly_chart(fig4, use_container_width=True)
st.info("**Interpretación:** el reparto de planes es muy parejo entre países (predomina Básico, "
        "sigue Estándar, Premium minoría). El mercado es geográficamente homogéneo: la estrategia "
        "comercial puede ser regional unificada, sin políticas distintas por país.")

# ---------- 5. Multivariada ----------
st.markdown("## 5. Edad, tiempo y plan (multivariada)")
fig5 = px.scatter(df, x="age", y="monthly_watch_time_mins", color="subscription_plan",
                  category_orders={"subscription_plan": orden}, opacity=0.5,
                  title="Edad vs tiempo de uso, coloreado por plan",
                  color_discrete_sequence=px.colors.qualitative.Set2)
fig5.update_layout(xaxis_title="Edad", yaxis_title="Minutos / mes")
st.plotly_chart(fig5, use_container_width=True)
st.info("**Interpretación:** la edad **no** influye en el consumo (la nube no sube ni baja con la edad), "
        "pero el **plan sí** separa los niveles (Premium siempre más arriba). Para predecir o segmentar "
        "por consumo, el plan es la variable que importa, no la edad. Las campañas de retención deberían "
        "segmentarse por plan/comportamiento, no por grupo etario.")
