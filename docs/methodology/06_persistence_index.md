# 06 — Índice de Persistencia

**Fase:** 6 de 10 (ver Fase 0, §9)
**Notebook asociado:** `notebooks/Step6_Ecuador_Persistence_Index.ipynb`
**Estado:** implementado y ejecutado — 2026-08-05
**Audiencia:** científicos, desarrolladores, especialistas GIS/DRM

## 1. Objetivo de la fase

Construir el Índice de Persistencia (Fase 0 §9), definido ahí solo de forma
conceptual — "meses consecutivos afectados, duración, longitud de
temporada" — sin una fórmula explícita como la de Severidad. Esta fase
traduce esa definición conceptual en tres componentes medibles y los
combina en un índice 0-1 por cantón y por provincia.

## 2. Decisión metodológica confirmada antes de programar

### 2.1 Alcance temporal: toda la ventana 2015-2025, no solo meses El Niño

**Alternativas consideradas** (presentadas a Jerson vía AskUserQuestion):
- Restringir el cálculo a los 38 meses "evento ENSO" de la Fase 5 — más
  puro conceptualmente (100% atribuible a El Niño), pero esos 38 meses no
  son consecutivos entre sí (están repartidos en 5 episodios distintos
  entre 2015 y 2024), lo que fragmentaría artificialmente cualquier racha
  que cruce la frontera entre dos episodios.
- Calcular ambas versiones por separado — más trabajo, sin necesidad
  inmediata.
- **Elegida: toda la línea de tiempo 2015-2025** (132 meses). La
  Persistencia, a diferencia de la Recurrencia (Fase 5, explícitamente
  normalizada por meses ENSO), mide cronicidad general del cantón —
  temporadas invernales completas, lluvias prolongadas — no solo lo
  estrictamente enmarcado en un episodio ENSO documentado. Es coherente con
  que Fase 0 no ató la definición de Persistencia a ENSO específicamente
  (a diferencia de Recurrencia, que sí lo hace en su fórmula).

## 3. Fundamento estadístico

Los tres componentes se calculan sobre la serie booleana mensual
"afectado/no afectado" de cada unidad administrativa, reindexada a los 132
meses completos de la ventana (mismo principio que el reindexado usado en
Fase 3 para Mann-Kendall y en Fase 5 para la validación de hipótesis: un
mes sin eventos cuenta como `False`, no desaparece de la serie).

- **Racha máxima** (`racha_maxima`): longitud, en meses, de la racha de
  meses consecutivos `True` más larga. Identificada con la técnica estándar
  de marcar un cambio de valor entre un mes y el anterior, y agrupar por el
  conteo acumulado de cambios.
- **Duración media** (`duracion_media`): promedio de la longitud de
  *todas* las rachas de la unidad, no solo la más larga — distingue una
  unidad con una sola racha larga excepcional de una con muchas rachas
  cortas repetidas.
- **Longitud de temporada** (`longitud_temporada`): número de meses
  calendario distintos (enero a diciembre, sin importar el año) en que la
  unidad tuvo al menos un evento alguna vez en toda la ventana — mide
  dispersión estacional, no consecutividad.

## 4. Decisiones metodológicas y su justificación

### 4.1 Normalización mixta: min-max para racha/duración, techo natural para temporada

`racha_maxima` y `duracion_media` se normalizan con min-max (igual que
Severidad, Fase 4) porque no tienen un techo natural interpretable — 132
meses consecutivos afectados (el 100% de la ventana) no es una referencia
realista para comparar cantones, así que se comparan contra el máximo
observado en los datos.

`longitud_temporada` se normaliza dividiendo entre 12 directamente — **sí**
tiene un techo natural, alcanzable y significativo: una unidad con al
menos un evento en cada uno de los 12 meses del año calendario en algún
momento de 11 años obtiene el máximo (1.0) sin necesidad de compararse
contra otras unidades. Se documenta esta asimetría explícitamente para que
no se lea como inconsistencia entre componentes.

### 4.2 Pesos de componentes: partes iguales (1/3), por defecto documentado, no una fórmula del diseño original

A diferencia de Severidad (que trae fórmula explícita en Fase 0 §9),
Persistencia no especifica pesos entre sus tres componentes. Se adoptó
partes iguales (0.3333/0.3333/0.3334, en `config.yaml`,
`persistence_index.component_weights`) como el valor neutral por defecto,
explícitamente señalado como pendiente del mismo análisis de sensibilidad
que ya se pidió para los pesos de Severidad (Fase 4 §6) y el umbral de
"evento ENSO" (Fase 5 §10) — no se presenta como una elección definitiva.

## 5. Esquema de salida

Dos tablas en `data/processed/` (Parquet + CSV):

- `persistence_index_canton` (1,105 filas: 221 cantones × 5 vistas —
  4 `hazard_type` + `"TODOS"` — con cobertura completa garantizada, mismo
  principio que Fase 5 §4.6).
- `persistence_index_provincia` (120 filas, mismo patrón, 24 provincias).

Columnas: `province_code`, `province_name_official`,
`canton_code`/`canton_name_official` (solo cantón), `hazard_type`,
`n_eventos`, `racha_maxima`, `duracion_media`, `longitud_temporada`
(crudos), `norm_racha_maxima`, `norm_duracion_media`,
`norm_longitud_temporada` (normalizados 0-1), `persistence_index` (0-1).

## 6. Resultados — primeras cifras

- **Distrito Metropolitano de Quito** encabeza el ranking cantonal
  (`persistence_index = 1.0`): racha máxima de **104 de 132 meses**
  consecutivos con al menos un evento, y presencia en los 12 meses
  calendario — consistente con ser, por lejos, el cantón con más eventos
  totales (Fase 3 §6).
- A nivel provincia, **Tungurahua alcanza el máximo absoluto posible**:
  `racha_maxima = 132` — es decir, no hubo un solo mes en los 11 años de la
  ventana sin al menos un evento en algún cantón de la provincia. Es un
  resultado real, no un error de cálculo (verificado: `duracion_media =
  132.0` porque hay una única racha que cubre toda la ventana).
- **41 de 221 cantones (18.6%)** alcanzaron el máximo de longitud de
  temporada (eventos en los 12 meses calendario en algún momento de la
  ventana) — la afectación en esos cantones no está limitada a una
  "temporada de lluvias" estrecha.
- Distribución del índice a nivel cantón: media 0.27, mediana 0.25, máximo
  1.0 (Quito) — distribución con cola larga hacia la derecha, la mayoría de
  cantones agrupados en valores bajos-medios.

## 7. Limitaciones

- El resultado de Tungurahua (racha máxima = 132, el techo absoluto) deja
  a esa provincia sin ningún margen de variación en `norm_racha_maxima`
  frente a futuros datos (siempre normalizará a 1.0 mientras siga siendo el
  máximo observado) — no es un error, pero conviene tenerlo presente al
  interpretar comparaciones futuras si se agregan años adicionales.
- Los pesos iguales entre los tres componentes (§4.2) no están validados
  por sensibilidad — un cantón con racha larga pero baja dispersión
  estacional (o viceversa) puede tener un índice similar a uno con el
  patrón opuesto, y el índice compuesto no distingue cuál de los dos
  patrones es más relevante operativamente para Acción Anticipatoria.
- No se filtró por `canton_confidence` (Fase 2 §4.7) — igual que en Fase 3,
  se usan los 21,743 eventos completos, incluidos los 43 casos "revisar".

## 8. Supuestos

- Se asume que un mes con un solo evento aislado cuenta igual que un mes
  con impactos severos y prolongados dentro del mismo mes — la Persistencia
  mide *presencia temporal* de afectación, no su magnitud (eso ya lo cubre
  Severidad, Fase 4); combinarlas es tarea del EFCI compuesto (Fase 8).
- Se asume que la racha de un mes de "veda" entre dos eventos cercanos
  rompe la persistencia (un mes sin ningún evento reportado corta la racha,
  aunque el siguiente evento esté relacionado con el mismo episodio
  climático) — es una simplificación del reindexado mensual, no distingue
  causalidad entre eventos consecutivos.

## 9. Ventajas del enfoque

- Los tres componentes capturan aspectos genuinamente distintos de la
  persistencia (racha extrema vs. patrón típico vs. dispersión estacional)
  en vez de colapsar a una sola métrica que podría ocultar cuál de los tres
  patrones domina en un cantón dado.
- Cobertura completa verificada explícitamente (221 cantones × 5 vistas,
  24 provincias × 5 vistas) antes de exportar — mismo principio de "nada se
  pierde silenciosamente" de las fases anteriores.
- Todos los pesos y el denominador de temporada viven en `config.yaml`, no
  hardcodeados — listos para el análisis de sensibilidad de Fase 8.

## 10. Posibles mejoras futuras

- Evaluar una definición de "racha" que tolere un mes de hueco (p. ej. dos
  meses activos separados por un mes sin eventos podrían seguir siendo
  parte del mismo episodio climático) — actualmente cualquier mes sin
  evento corta la racha estrictamente.
- Análisis de sensibilidad de los pesos entre los tres componentes (§4.2).
- Investigar si el resultado de Tungurahua (racha máxima = 132) refleja
  cronicidad real y sostenida o una alta densidad de reportes de baja
  magnitud que individualmente no serían significativos — requiere revisar
  la distribución de severidad de esos eventos, cruzando con la Fase 4.

## 11. Referencias

- Fase 0 — Diseño Conceptual EFCI Ecuador, §9 (Persistencia).
- `docs/methodology/03_historical_analysis.md` (insumo de conteo de eventos
  por mes).
- `docs/methodology/05_recurrence_index.md` §4.3 (definición de "evento
  ENSO", no usada directamente aquí pero relevante para la Fase 8).
