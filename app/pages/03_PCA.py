import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from pathlib import Path

st.set_page_config(page_title="PCA", page_icon="🧭", layout="wide")

BASE = Path(__file__).resolve().parent.parent.parent
CLEAN = BASE / "data" / "processed" / "streaming_users_clean.csv"

st.title("🧭 Escalamiento y PCA")

st.markdown("""
**Variables utilizadas:** `age`, `monthly_watch_time_mins`, `customer_support_tickets` (las numéricas).

**Escalamiento:** se aplicó `StandardScaler` (media 0, desvío 1) antes del PCA. Es necesario porque
PCA busca direcciones de máxima varianza; sin escalar, la variable de mayor magnitud (tiempo de
visualización) dominaría artificialmente por sus unidades, no por su importancia real.
""")

@st.cache_data
def calcular():
    df = pd.read_csv(CLEAN)
    num = ["age", "monthly_watch_time_mins", "customer_support_tickets"]
    X = df[num]
    Xs = StandardScaler().fit_transform(X)
    pca = PCA(n_components=3)
    comp = pca.fit_transform(Xs)
    return df, num, pca, comp

df, num, pca, comp = calcular()
var_exp = pca.explained_variance_ratio_ * 100
var_acum = np.cumsum(var_exp)

st.markdown("### Varianza explicada")
tabla = pd.DataFrame({
    "Componente": ["PC1", "PC2", "PC3"],
    "Varianza explicada (%)": var_exp.round(2),
    "Varianza acumulada (%)": var_acum.round(2),
})
st.dataframe(tabla, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(tabla, x="Componente", y="Varianza explicada (%)",
                 title="Varianza explicada por componente", color_discrete_sequence=["steelblue"])
    st.plotly_chart(fig, use_container_width=True)
with c2:
    corr = df[num].corr()
    fig = px.imshow(corr, text_auto=".3f", aspect="auto",
                    color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                    title="Heatmap de correlación")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### Interpretación")
st.info("""
Cada componente explica aproximadamente **un tercio** de la varianza (~33%). Esto indica que las tres
variables son **prácticamente independientes**: no hay redundancia que PCA pueda comprimir. A diferencia
de un dataset con variables correlacionadas (donde las primeras componentes capturan casi toda la
información), acá **no conviene reducir dimensiones** — descartar componentes perdería información real.

PCA cumple entonces un rol **diagnóstico**: confirma que `edad`, `tiempo de uso` y `tickets` aportan
información distinta y deben conservarse las tres. Un resultado de "no se puede comprimir" es un hallazgo
válido, no un fracaso del método.
""")
