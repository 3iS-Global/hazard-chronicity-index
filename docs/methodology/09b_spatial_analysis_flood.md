# 09b — Análisis Espacial Independiente por Peligro: Inundación

**Fase:** 9, primera de 4 versiones independientes por tipo de amenaza (ver Fase 0 §8; decisión de separación total confirmada por Jerson el 2026-08-17)
**Notebook asociado:** `notebooks/Step9_Ecuador_Spatial_Analysis_Flood.ipynb`
**Estado:** implementado y ejecutado — 2026-08-17
**Audiencia:** científicos, desarrolladores, especialistas DRM/FAO AA

## 1. Objetivo de esta versión

Jerson pidió explícitamente dejar de combinar los 4 tipos de amenaza (inundación, deslizamiento, socavamiento, aluvión) en un solo análisis espacial filtrable por columna, y en su lugar construir **análisis y mapas completamente independientes por tipo de amenaza**. Este documento cubre la primera versión — **inundación** — construida y validada antes de replicar el mismo patrón a los otros 3 peligros (secuencia confirmada por Jerson: "detente tras inundación para revisión").

`notebooks/Step9_Ecuador_Spatial_Analysis.ipynb` (el original, vista `"TODOS"` combinada) **no se modifica ni se reemplaza** — sigue siendo válido como lectura agregada de cronicidad. Este notebook responde una pregunta distinta y más específica: ¿dónde se agrupa geográficamente la cronicidad de **inundación en particular**, sin mezclarla con los otros 3 peligros?

## 2. Método — idéntico al original, solo cambia la fuente de datos

Mismo método exacto validado en la Fase 9 original (2026-08-06): contigüidad Queen orden 1 + respaldo KNN=1 para islas, Getis-Ord Gi* y Local Moran's I sobre las 5 capas (HCI + 4 sub-índices), KDE ponderado por severidad de evento, agregación hexagonal H3 resolución 5. La única diferencia: `hci_composite_canton.csv` y `hazard_event_geo.gpkg` se filtran a `hazard_type == "flood"` antes de correr el análisis, en vez de usar la vista `"TODOS"`.

**La matriz de pesos espaciales (Queen+KNN) es idéntica a la del notebook original** — depende únicamente de la geometría administrativa (221 polígonos de cantón), no del valor de las variables, así que no había necesidad de recalcularla. Las mismas 3 islas (San Cristóbal, Isabela, Santa Cruz — Galápagos) se conectan entre sí vía el respaldo KNN, igual que en el análisis combinado.

## 3. Decisión confirmada por Jerson antes de programar: relleno de cantones sin historial

De los 221 cantones, **214 tienen al menos un evento de inundación histórico y 7 no tienen ninguno**. Se presentaron dos opciones (AskUserQuestion, 2026-08-17):

1. **Rellenar esos 7 cantones con HCI=0 y mantener el universo completo de 221** (elegida) — un cantón sin historial de inundación tiene cronicidad de inundación genuinamente nula, no un dato faltante; consistente con la disciplina de cobertura completa ya usada en Fases 3-8 (ver `05_recurrence_index.md` §4.6, el caso de San Fernando).
2. Excluir esos cantones del análisis (grafo espacial más pequeño) — descartada porque haría que cada mapa de peligro tuviera un universo distinto, dificultando la comparación entre los 4 peligros.

Implementación: `merge` explícito contra el universo completo de 221 cantones antes de construir la tabla espacial de trabajo, con `fillna(0.0)` en las 5 variables (HCI + 4 sub-índices). Verificado: 7 cantones rellenados, coincide exactamente con `221 - 214`.

## 4. Resultados reales

**Gi* (hotspots), capa HCI-flood:** 70 puntos calientes / 36 puntos fríos de 221 cantones — sustancialmente más dispersión que el análisis combinado. El patrón geográfico es **claramente distinto** al de la vista `"TODOS"` (que se concentraba en un arco alrededor de Quito/sierra centro-norte): aquí los puntos calientes se concentran en la **costa** (Esmeraldas, Manabí, Guayas, Los Ríos — franja litoral y cuencas bajas) y los puntos fríos en el **oriente amazónico** (Sucumbíos, Napo, Orellana, Pastaza). Geográficamente coherente: la inundación fluvial/costera de baja altitud es un fenómeno distinto al de los deslizamientos de la sierra, que dominaban el patrón combinado.

**Local Moran's I (HCI-flood):** 50 clusters HH (Alto-Alto), 19 LL (Bajo-Bajo) de 221 — mismo patrón costa-caliente/oriente-frío confirmado con el segundo método.

**Verificación de sentido común (Quito):** en el análisis combinado, Quito era el cantón #1 de HCI nacional. En el análisis de inundación específicamente, Quito **no es un hotspot Gi* significativo** para HCI-flood (aunque sí tiene un HCI-flood relativamente alto individualmente, 0.436, 2º lugar nacional en inundación) — es un caso donde el valor propio es alto pero el patrón de sus vecinos no lo confirma como cluster espacial, información real, no un error.

**Hexágonos H3 (res 5):** 618 celdas con ≥1 evento; suma de eventos por hexágono = 7,281 exactamente (verificado, coincide con el total de eventos `hazard_type=="flood"`).

## 5. Exportación

Mismos 4 productos que la Fase 9 original, con sufijo `_flood`: `hotspots_gi_star_canton_flood.{parquet,csv}`, `local_moran_canton_flood.{parquet,csv}`, `kde_severidad_grid_flood.{geojson,csv}`, `hexagonos_h3_res5_flood.{geojson,csv}` — todos en `data/processed/`, ninguno sobrescribe los archivos de la Fase 9 original (sin sufijo, vista `"TODOS"`).

## 6. Limitaciones y supuestos

- El relleno con 0 (§3) asume que la ausencia histórica de inundación en un cantón es representativa de su riesgo futuro — una simplificación conocida (11 años de historial, no garantiza ausencia de riesgo real, solo ausencia de eventos observados en esta ventana).
- Los 7 cantones rellenados no distorsionan significativamente el patrón Gi*/Moran observado — son minoría (3.2% del total) y su valor 0 los coloca naturalmente entre los "no significativo" o "punto frío", coherente con su historial real.
- Mismas limitaciones estructurales de la Fase 9 original (permutaciones=999 para p-valores, contigüidad Queen puede no capturar conectividad hidrológica real — cuencas compartidas entre cantones no necesariamente contiguos).

## 7. Próximos pasos

- Replicar el mismo patrón para deslizamiento, socavamiento y aluvión — pendiente de confirmación de Jerson tras revisar estos resultados de inundación.
- Fase 10 (productos/mapas) para inundación: completada en paralelo, ver `10b_products_flood.md`.

## 8. Referencias

- `docs/methodology/09_spatial_analysis.md` — versión combinada original, mismo método base.
- `docs/methodology/05_recurrence_index.md` §12 — criterio ENSO ampliado, insumo previo de `hci_composite_canton.csv`.
