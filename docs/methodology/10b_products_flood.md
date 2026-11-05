# 10b — Productos Independientes por Peligro: Inundación (Mapas)

**Fase:** 10, primera de 4 versiones independientes por tipo de amenaza
**Notebook asociado:** `notebooks/Step10a_Ecuador_Static_Maps_Flood.ipynb`
**Estado:** implementado y ejecutado — 2026-08-17 (mapas estáticos + atlas; el resto de productos de Fase 10 — interactivos, dashboard, perfiles, reporte Word — quedan pendientes, ver §5)
**Audiencia:** científicos, desarrolladores, especialistas DRM/FAO AA

## 1. Objetivo de esta versión

Réplica de `Step10a_Ecuador_Static_Maps.ipynb` (mapas estáticos + atlas PDF) filtrada a `hazard_type == "flood"`, usando los insumos ya construidos en `09b_spatial_analysis_flood.md`. Primera de 4 versiones de Fase 10 por tipo de amenaza — el resto de sub-fases de productos (10b-10f interactivos, dashboard, Excel, perfiles, reporte Word) no se han replicado aún para ningún peligro; se hará después de que Jerson revise este primer entregable (mapas), por acuerdo explícito.

## 2. Bug real detectado y corregido antes de entregar

**El primer intento de generar el mapa de cronicidad EFCI-inundación salió casi completamente en la clase "Muy Baja"** — visualmente inútil, casi todo el país del mismo color clarísimo. Diagnóstico: el notebook reutilizó ingenuamente la columna `clase_efci` de `efci_composite_canton.csv`, asumiendo que ya venía calculada como en el notebook original. Pero **Fase 8 (`Step8`, Sección 3) solo calcula la clasificación Jenks para `hazard_type == "TODOS"`** — para las demás vistas (`flood`, `landslide`, `scour`, `debris_flow`), la columna queda `NaN` sin calcular, un hecho no documentado explícitamente en su momento porque nunca se había necesitado hasta ahora. El primer intento de relleno (fillna a "Muy Baja" para los 7 cantones sin historial) terminó rellenando también los 214 cantones con historial real pero sin clase calculada — no solo los 7 esperados.

**Corrección:** se recalculó la clasificación Jenks directamente en este notebook, sobre la distribución real del EFCI-flood (221 cantones, incluidos los 7 rellenados con 0 en `09b`), con el mismo método exacto de Fase 8 (`jenkspy.jenks_breaks`, 5 clases, mismo ajuste `breaks[0] -= 1e-9`). Quiebres resultantes: `[0.0, 0.095, 0.170, 0.245, 0.353, 0.562]`. Verificado visualmente tras la corrección — el mapa ahora muestra variación real y geográficamente coherente (ver `09b_spatial_analysis_flood.md` §4 para el patrón costa-caliente/oriente-frío).

Un segundo detalle corregido en el mismo proceso: el dataset maestro (`mapa_master_canton_flood.csv/gpkg`) se exportaba en la Sección 1, antes de que la clasificación Jenks (Sección 4) estuviera calculada — el archivo exportado no incluía `clase_efci`. Se agregó un segundo `to_file`/`to_csv` al final de la Sección 4, después de calcular la clase, para que el producto final sí la incluya.

**Nota metodológica para las 3 replicaciones pendientes (deslizamiento/socavamiento/aluvión):** este mismo patrón de bug (reutilizar `clase_efci` sin calcularla) se repetiría si se copia el notebook original sin este ajuste — documentado aquí explícitamente para no repetir el error.

## 3. Productos generados

8 mapas PNG (mismo esquema que el atlas original, sufijo `_flood`) + `Atlas_EFCI_Ecuador_Flood.pdf` (9 páginas: portada + 8 mapas):

1. `01_frecuencia_inundaciones_flood.png` — nº de eventos de inundación 2015-2025.
2. `02_severidad_flood.png` — Índice de Severidad (Fase 4), vista flood.
3. `03_frecuencia_enso_flood.png` — eventos de inundación en meses El Niño (criterio ICEN, Fase 5).
4. `04_poblacion_afectada_flood.png` — máximo histórico de población afectada por inundación.
5. `05_perdidas_agricolas_flood.png` — máximo histórico de hectáreas agrícolas afectadas por inundación.
6. `06_perdidas_vivienda_flood.png` — máximo histórico de viviendas afectadas por inundación.
7. `07_efci_cronicidad_flood.png` — EFCI compuesto, clasificación Jenks propia (§2).
8. `08_hotspots_gi_star_flood.png` — hotspots Gi* (Fase 9b).

También: `mapa_master_canton_flood.{gpkg,csv}` (221 cantones × 20 columnas, dataset maestro reutilizable).

## 4. Resultados reales (ranking)

Top 5 cantones por EFCI-inundación: **Chone** (Manabí, 0.562), Distrito Metropolitano de Quito (0.436), Guayaquil (0.422), Babahoyo (0.418), Santo Domingo (0.401) — ver interpretación completa en `09b_spatial_analysis_flood.md` §4. Distribución de clases: Baja=88, Moderada=59, Alta=37, Muy Baja=30, Muy Alta=7 (de 221).

## 5. Explícitamente pendiente (no construido en esta ronda)

- Mapas interactivos HTML (equivalente a `Step10b`).
- Hoja de cálculo de estadísticas (`Step10c`).
- Dashboard HTML/ipywidgets (`Step10d`/`Step10e`).
- Perfiles cantonales/provinciales en PDF (`Step10f`).
- Reporte ejecutivo Word.

Se priorizaron los mapas estáticos + atlas por ser el producto más directamente visual para la revisión que Jerson pidió antes de continuar con los otros 3 peligros. El resto de sub-fases se construirán, para los 4 peligros, después de esa revisión.

## 6. Referencias

- `docs/methodology/10_products.md` — Fase 10 original (vista `TODOS`), mismo método base para `Step10a`.
- `docs/methodology/09b_spatial_analysis_flood.md` — insumos Gi*/EFCI-flood usados aquí.
