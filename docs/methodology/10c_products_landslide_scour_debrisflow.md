# 10c — Productos Independientes por Peligro: Deslizamiento, Socavamiento y Aluvión (Mapas)

**Fase:** 10, versiones 2-4 de 4 (ver `10b_products_flood.md` para inundación)
**Notebooks asociados:** `Step10a_Ecuador_Static_Maps_Landslide.ipynb`, `Step10a_Ecuador_Static_Maps_Scour.ipynb`, `Step10a_Ecuador_Static_Maps_DebrisFlow.ipynb`
**Estado:** implementados y ejecutados — 2026-08-17 (mapas estáticos + atlas; resto de sub-fases de Fase 10 pendientes para los 4 peligros, ver `10b` §5)
**Audiencia:** científicos, desarrolladores, especialistas DRM/FAO AA

## 1. Objetivo

Réplica de `Step10a_Ecuador_Static_Maps_Flood.ipynb` (incluida ya la corrección del bug de clasificación Jenks documentado en `10b_products_flood.md` §2) a los 3 peligros restantes, generada por sustitución sistemática de `hazard_type` y etiquetas en español, verificada exhaustivamente para no dejar texto de "inundación" residual.

## 2. La corrección de Fase 10b ya viene incluida desde el inicio

A diferencia de la primera versión (inundación), donde el bug de la clasificación Jenks se descubrió y corrigió sobre la marcha, estos 3 notebooks se generaron **a partir de la versión ya corregida** de `Step10a_Ecuador_Static_Maps_Flood.ipynb` — cada uno recalcula su propia clasificación Jenks localmente (`jenkspy`, 5 clases) sobre su distribución específica de EFCI, sin reutilizar la columna `clase_efci` de `efci_composite_canton.csv` (que solo existe para `hazard_type=="TODOS"`, ver `10b` §2). Verificado en los logs de ejecución — los 3 notebooks imprimen sus propios quiebres Jenks reales, distintos entre sí y del de inundación.

## 3. Resultados reales — quiebres Jenks y ranking por peligro

| Peligro | Quiebres Jenks (5 clases) | Top cantón EFCI |
|---|---|---|
| Deslizamiento | `[0, 0.068, 0.169, 0.276, 0.404, 0.637]` | Distrito Metropolitano de Quito (0.637) |
| Socavamiento | `[0, 0.0, 0.125, 0.174, 0.238, 0.392]` | Distrito Metropolitano de Quito (0.392) |
| Aluvión | `[0, 0.0, 0.118, 0.162, 0.226, 0.313]` | Baños de Agua Santa (0.313) |

(Comparar con inundación: `[0, 0.095, 0.170, 0.245, 0.353, 0.562]`, top Chone 0.562 — ver `10b_products_flood.md`.)

Nótese que socavamiento y aluvión tienen un segundo quiebre en exactamente `0.0` — consecuencia directa de la alta proporción de cantones rellenados con EFCI=0 (30.3% y 59.7% respectivamente, ver `09c_spatial_analysis_landslide_scour_debrisflow.md` §2): la clase "Muy Baja" queda definida por el propio valor 0, no por un rango continuo pequeño.

## 4. Productos generados (por peligro, mismo esquema de 8 mapas que inundación)

`outputs/maps/{01..08}_*_{landslide|scour|debris_flow}.png` + `outputs/reports/Atlas_EFCI_Ecuador_{Landslide|Scour|DebrisFlow}.pdf` (9 páginas cada uno) + `data/processed/mapa_master_canton_{landslide|scour|debris_flow}.{gpkg,csv}` (221 cantones × 20 columnas cada uno, incluyendo `clase_efci` ya calculada).

## 5. Explícitamente pendiente

Igual que inundación (`10b` §5): mapas interactivos HTML, hoja de estadísticas, dashboard, perfiles por cantón/provincia, reporte ejecutivo Word — para los 4 peligros, a construir juntos en la siguiente etapa.

## 6. Referencias

- `docs/methodology/10b_products_flood.md` — versión 1 (inundación), incluye el detalle completo del bug de Jenks corregido.
- `docs/methodology/09c_spatial_analysis_landslide_scour_debrisflow.md` — insumos Gi*/EFCI por peligro usados aquí.
