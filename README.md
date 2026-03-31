# 📊 People Analytics — Proyección de Horas Extra en Call Center

> Análisis exploratorio y modelado predictivo de horas extra para una operación de Call Center de Atención al Cliente, usando Python y técnicas de series temporales.

---

## Contexto

El área de **Gestión Humana** identificó que la aprobación de horas extra se hacía de manera reactiva, generando costos no planificados y alertas tardías de sobre-esfuerzo en el equipo operativo. Este proyecto nació como una iniciativa de **People Analytics** para anticipar la demanda de HHEE y facilitar decisiones proactivas de dotación y presupuesto.

Los datos corresponden a **49 meses** (Ene 2022 – Ene 2026) de una posición de agentes en un Call Center de servicio al cliente.

---

## Estructura del repositorio

```
overtime-analytics/
│
├── data/
│   ├── raw/
│   │   └── overtime_callcenter_2022_2026.csv   ← datos originales
│   └── processed/
│       ├── overtime_procesado.csv              ← dataset limpio + variables derivadas
│       └── proyecciones_2026.csv               ← output de proyecciones
│
├── notebooks/
│   └── 01_EDA_y_Proyecciones_HHEE.ipynb        ← notebook principal
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py                        ← funciones de limpieza
│   ├── features.py                             ← ingeniería de variables
│   └── models.py                               ← wrappers de modelos
│
├── outputs/
│   ├── figures/                                ← gráficos exportados (PNG)
│   └── models/                                 ← modelos serializados (pickle)
│
├── docs/
│   └── diccionario_datos.md                    ← descripción de columnas
│
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── bug_report.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Variables del dataset

| Columna | Tipo | Descripción |
|---|---|---|
| `periodo` | str | Mes en formato YYYY-MM |
| `year` / `month` | int | Año y mes numérico |
| `num_personas` | int | Dotación activa en el período |
| `horas_extra_totales` | float | HHEE acumuladas del equipo (h) |
| `horas_extra_promedio` | float | HHEE por persona (h/persona) |
| `ausentismo_pct` | float | Tasa de ausentismo mensual (%) |
| `rotacion_mensual_pct` | float | Rotación del mes (%) |
| `volumen_llamadas_miles` | float | Llamadas atendidas (miles) |
| `nivel_servicio_pct` | float | % llamadas dentro del SLA |
| `costo_hhee_soles` | float | Costo total de HHEE (S/) |
| `campania_activa` | int | 1 si hay campaña comercial activa, 0 si no |

---

## Metodología

```
Datos brutos
    │
    ▼
Limpieza y EDA ──► distribuciones, outliers, correlaciones
    │
    ▼
Análisis de series temporales ──► descomposición, ACF/PACF, test ADF
    │
    ▼
Modelado ──► Lineal · Holt-Winters (ETS) · SARIMA · Prophet
    │
    ▼
Evaluación out-of-sample ──► MAE · RMSE · MAPE
    │
    ▼
Proyecciones Feb–Jul 2026
```

---

## Resultados principales

- **Estacionalidad confirmada**: Sep–Ene concentra los picos de HHEE, alineados con campañas de fin de año.
- **Mejor modelo**: ETS (Holt) con menor MAE en el período de validación.
- **Alerta operativa propuesta**: activar cuando HHEE promedio supere **55 h/persona/mes**.
- **Impacto potencial**: anticipar el refuerzo de headcount en Ago con ~6 semanas de anticipación puede reducir el costo de HHEE en campaña hasta en un 20%.

---

## Cómo usar este proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/overtime-analytics.git
cd overtime-analytics
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el notebook

```bash
jupyter notebook notebooks/01_EDA_y_Proyecciones_HHEE.ipynb
```

> También puedes abrirlo directamente en [Google Colab](https://colab.research.google.com/) subiendo el notebook y el CSV.

---

## Dependencias principales

| Librería | Versión mínima | Uso |
|---|---|---|
| pandas | 2.0 | Manipulación de datos |
| numpy | 1.24 | Cálculo numérico |
| matplotlib | 3.7 | Visualización |
| seaborn | 0.12 | Visualización estadística |
| statsmodels | 0.14 | Series temporales (ETS, SARIMA) |
| scikit-learn | 1.3 | Regresión lineal, métricas |
| prophet | 1.1 | Forecasting con estacionalidad |

---

## Limitaciones conocidas

- El dataset tiene **49 observaciones mensuales**, lo que limita la potencia estadística de modelos complejos. Con más historia (3+ años completos), SARIMA y Prophet mejorarían notoriamente.
- El número de personas en planilla varió mucho (6–29), lo que introduce ruido en las HHEE totales. Se recomienda priorizar el análisis sobre el **promedio por persona**.
- No se dispone de datos de HHEE a nivel individual (agente), lo que impediría segmentar por perfil o antigüedad.

---

## Próximos pasos

- [ ] Incorporar datos de ausentismo como variable exógena en SARIMAX
- [ ] Explorar modelos de ML supervisado (XGBoost, LightGBM) con features de calendario
- [ ] Construir un dashboard en Power BI / Streamlit para monitoreo mensual
- [ ] Ampliar el análisis a nivel de agente individual

---

## Autor

Equipo de People Analytics — Gestión Humana  
*Proyecto interno — uso exclusivo de la organización*

---

*Última actualización: Febrero 2026*
