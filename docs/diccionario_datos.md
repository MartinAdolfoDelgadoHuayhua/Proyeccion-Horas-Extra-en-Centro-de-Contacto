# Diccionario de Datos — overtime_callcenter_2022_2026.csv

**Fuente:** Sistema de Gestión de RRHH / Plataforma de Asistencia  
**Frecuencia:** Mensual  
**Cobertura:** Enero 2022 – Enero 2026  
**Área:** Call Center – Atención al Cliente  

---

## Columnas

### `periodo`
- **Tipo:** string
- **Formato:** YYYY-MM
- **Ejemplo:** `2024-09`
- **Descripción:** Mes del registro en formato año-mes. Cada fila representa un mes calendario.

---

### `year`
- **Tipo:** integer
- **Rango:** 2022 – 2026
- **Descripción:** Año numérico extraído del campo `periodo`. Útil para agrupaciones anuales.

---

### `month`
- **Tipo:** integer
- **Rango:** 1 – 12
- **Descripción:** Mes numérico. Enero = 1, Diciembre = 12.

---

### `num_personas`
- **Tipo:** integer
- **Unidad:** personas
- **Descripción:** Cantidad de agentes activos en planilla durante el mes. Incluye solo personal contratado con jornada completa; excluye practicantes y personal de agencia sin asignación al área.
- **Nota:** Variaciones grandes entre meses pueden deberse a altas/bajas masivas o restructuraciones del área.

---

### `horas_extra_totales`
- **Tipo:** float
- **Unidad:** horas
- **Descripción:** Suma total de horas extra autorizadas y efectivamente trabajadas por todos los agentes del equipo durante el mes. Incluye HHEE diurnas y nocturnas según los registros del sistema de marcación.
- **Fuente:** Sistema de control de asistencia (marcación biométrica).

---

### `horas_extra_promedio`
- **Tipo:** float
- **Unidad:** horas por persona
- **Fórmula:** `horas_extra_totales / num_personas`
- **Descripción:** Indicador de intensidad de HHEE por colaborador. Es el indicador preferido para comparar períodos con diferente dotación.
- **Alerta operativa:** Valores superiores a 55 h/persona se consideran zona de riesgo de sobre-esfuerzo.

---

### `ausentismo_pct`
- **Tipo:** float
- **Unidad:** porcentaje (%)
- **Fórmula:** `(días no trabajados / días programados) × 100`
- **Descripción:** Tasa de ausentismo mensual del equipo. Incluye faltas injustificadas, licencias médicas y permisos sin goce de haber. No incluye vacaciones programadas.

---

### `rotacion_mensual_pct`
- **Tipo:** float
- **Unidad:** porcentaje (%)
- **Fórmula:** `(bajas del mes / promedio personas) × 100`
- **Descripción:** Tasa de rotación voluntaria e involuntaria del mes. Un valor alto puede explicar picos de HHEE por el período de transición hasta cubrir la vacante.

---

### `volumen_llamadas_miles`
- **Tipo:** float
- **Unidad:** miles de llamadas
- **Descripción:** Total de llamadas entrantes atendidas por el equipo durante el mes. Es el principal driver de carga operativa y tiene correlación directa con las HHEE.
- **Fuente:** ACD / plataforma telefónica.

---

### `nivel_servicio_pct`
- **Tipo:** float
- **Unidad:** porcentaje (%)
- **Descripción:** Porcentaje de llamadas atendidas dentro del tiempo objetivo definido en el SLA (Service Level Agreement). Valores bajos indican presión sobre el equipo y se correlacionan con mayor uso de HHEE.
- **Target interno:** ≥ 85%

---

### `costo_hhee_soles`
- **Tipo:** float
- **Unidad:** soles peruanos (S/)
- **Descripción:** Costo total de las horas extra pagadas en el mes. Calculado con base en la tarifa de HHEE por hora según el convenio colectivo vigente. No incluye cargas sociales adicionales.

---

### `campania_activa`
- **Tipo:** integer (binario)
- **Valores:** 0 = sin campaña, 1 = campaña activa
- **Descripción:** Indica si durante ese mes estuvo activa alguna campaña comercial de alto volumen (ej. campaña navideña, Black Friday, lanzamientos de producto). Los meses con `campania_activa = 1` suelen mostrar mayor volumen de llamadas y, por tanto, mayor demanda de HHEE.
- **Meses típicos con campaña:** Sep, Oct, Nov, Dic, Ene.

---

## Notas de calidad

- No se detectaron valores nulos en ninguna columna.
- Los datos de 2024–2025 son datos reales del sistema. Los de 2022–2023 fueron complementados con estimaciones históricas basadas en patrones similares.
- El campo `costo_hhee_soles` es una aproximación; para reportes contables usar el sistema de nómina oficial.

---

*Documento mantenido por el equipo de People Analytics — Gestión Humana.*  
*Última revisión: Febrero 2026*
