# PI Minería de Datos 1 — Análisis de Usuarios de Streaming

## Información general

Proyecto Integrador de la materia Minería de Datos 1. Desarrolla un análisis de datos reproducible y comunicable sobre un dataset de usuarios de una plataforma de streaming, cubriendo inspección, calidad, análisis exploratorio, escalamiento y PCA.

- **Comisión:** Turno Tarde, Nodo
- **Integrantes:** Emilio Cabaña
- **Fecha:** Lunes 29 de Junio
- **Repositorio:** https://github.com/Emvcab/PI_Mineria_Datos_1
- **Aplicación Streamlit:** https://pimineriadatos1.streamlit.app/

## Objetivo del proyecto

Aplicar los contenidos de Minería de Datos 1 para construir un análisis con decisiones justificadas por evidencia, trazabilidad del proceso y comunicación clara. Se busca comprender la calidad inicial del dataset, prepararlo a partir de evidencia observada, analizarlo a nivel univariado, bivariado y multivariado, aplicar escalamiento y PCA, y comunicar los resultados mediante una aplicación pública y un informe breve. No es un proyecto de modelado predictivo.

## Dataset

Registros de usuarios de una plataforma de streaming. Cada fila representa un usuario.

Variables: `user_id`, `age`, `subscription_plan`, `monthly_watch_time_mins`, `country`, `favorite_genre`, `last_login_date`, `customer_support_tickets`.

El dataset original se conserva sin modificaciones en `data/raw/streaming_users_dirty.json`. El dataset final utilizado para el análisis está en `data/processed/streaming_users_clean.csv`. Detalle completo de variables y vista previa: ver `notebooks/01_inspeccion_inicial.ipynb` y la página *Dataset* de la aplicación.

## Estructura del repositorio

```
PI_Mineria_Datos_1/
├── README.md
├── requirements.txt
├── data/raw/            # dataset original sin modificar
├── data/processed/      # dataset final del análisis
├── notebooks/           # 01 a 05: desarrollo por etapas
├── app/                 # aplicación Streamlit (Home + 4 páginas)
├── reports/             # informe_final.pdf
└── logs/                # pipeline_log.csv (registro ETL)
```

## Preparación y calidad de datos

Las decisiones de limpieza surgen de la evidencia reunida en la inspección inicial; cada transformación queda registrada en `logs/pipeline_log.csv`. Acciones aplicadas:

- Eliminación de duplicados por `user_id` (clave única).
- Normalización de `subscription_plan`, `country` y `favorite_genre` a categorías canónicas.
- Valores imposibles (edades fuera de rango, tiempos negativos, tickets -1) → nulo.
- Valores imposibles (99999 en tiempo; 99/150 en tickets), identificados por su repetición exacta y su separación del resto de la distribución, tratados como error → nulo.
- Winsorización (IQR k=3) de la cola alta real del tiempo de visualización.
- Parseo y validación de fechas; las no recuperables o futuras quedan como nulo (no se imputan).
- Diagnóstico del mecanismo de faltantes: la tasa de nulos en watch_time crece con el plan (Básico ~1%, Premium ~11%), lo que confirma un mecanismo MAR y justifica imputar por grupo.
- Imputación de faltantes por mediana según plan (numéricas) y moda (categórica).

Detalle y justificación paso a paso: `notebooks/02_calidad_y_limpieza.ipynb`.

## Resumen del análisis exploratorio

El EDA (5 visualizaciones: 2 univariadas, 2 bivariadas, 1 multivariada) está desarrollado en `notebooks/03_eda.ipynb` y resumido en la página *EDA* de la aplicación. Hallazgos principales:

- La base de usuarios se concentra en adultos jóvenes (mediana ~33 años).
- El plan de suscripción es el principal determinante del consumo: los usuarios Premium consumen casi el doble que los Básico.
- La edad no presenta relación con el tiempo de visualización.
- La preferencia de género es transversal al plan y al país; la distribución de planes es homogénea entre países.

El EDA incluye además medidas de dispersión y forma (coeficiente de variación, asimetría y curtosis): el consumo y los tickets presentan asimetría positiva alta, lo que respalda el uso de la mediana sobre la media. Cada visualización incluye su interpretación vinculada a los objetivos del análisis.

## Reducción de dimensionalidad

Desarrollada en `notebooks/04_pca.ipynb` y en la página *PCA* de la aplicación. Se utilizaron las variables numéricas (`age`, `monthly_watch_time_mins`, `customer_support_tickets`), estandarizadas con `StandardScaler` antes de aplicar PCA.

Resultado: cada componente principal explica aproximadamente un tercio de la varianza (~33%), lo que indica que las variables son independientes y que no es posible reducir dimensiones sin perder información. El heatmap de correlación confirma este diagnóstico (correlaciones cercanas a cero). PCA cumple aquí un rol diagnóstico, evidenciando la ausencia de redundancia entre variables.

## Visualización interactiva

La aplicación pública en Streamlit Cloud comunica los resultados para público general, con páginas de Dataset, EDA, PCA y Conclusiones. No reemplaza la evidencia técnica del repositorio.

- **Enlace público a Streamlit Cloud:** https://pimineriadatos1.streamlit.app/

## Cómo ejecutar localmente

```bash
git clone <URL-del-repositorio>
cd PI_Mineria_Datos_1
pip install -r requirements.txt
streamlit run app/Home.py
```

Los notebooks pueden ejecutarse en orden (01 a 05) desde la carpeta `notebooks/`. El notebook 02 genera el dataset procesado y el log que consumen las etapas siguientes.

## Conclusiones

El proyecto recorrió el ciclo completo de preparación y análisis de datos, con cada decisión justificada por evidencia y registrada para su trazabilidad. El dataset quedó limpio (retención ≈ 98%) y comprendido. El principal factor asociado al consumo es el plan de suscripción, no la edad. El PCA mostró que las variables numéricas son independientes y no reducibles.

Limitaciones y próximos pasos se detallan en `notebooks/05_conclusiones.ipynb` y en `reports/informe_final.pdf`.
