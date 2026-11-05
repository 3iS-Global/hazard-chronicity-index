# 09c — Análisis Espacial Independiente por Peligro: Deslizamiento, Socavamiento y Aluvión

**Fase:** 9, versiones 2-4 de 4 (ver `09b_spatial_analysis_flood.md` para la versión 1, inundación, y su justificación metodológica completa)
**Notebooks asociados:** `Step9_Ecuador_Spatial_Analysis_Landslide.ipynb`, `Step9_Ecuador_Spatial_Analysis_Scour.ipynb`, `Step9_Ecuador_Spatial_Analysis_DebrisFlow.ipynb`
**Estado:** implementados y ejecutados — 2026-08-17, tras confirmación de Jerson de replicar el patrón validado en inundación a los 3 peligros restantes
**Audiencia:** científicos, desarrolladores, especialistas DRM/FAO AA

## 1. Objetivo y método

Mismo método exacto que `09b_spatial_analysis_flood.md` (Queen+KNN, Gi*/Local Moran's I sobre las 5 capas, KDE ponderado por severidad, hexágonos H3 res5), replicado mecánicamente a los 3 peligros restantes mediante sustitución sistemática de `hazard_type` y las etiquetas en español — verificado cuidadosamente para no dejar texto de "inundación"/"flood" residual en ninguno de los 3 notebooks. Misma decisión confirmada por Jerson (relleno con EFCI=0 para cantones sin historial, universo completo de 221 cantones, mismo grafo Queen+KNN).

## 2. Cobertura real por peligro — una diferencia importante entre los 3

A diferencia de inundación (214/221 cantones con historial, solo 7 rellenados), la cobertura histórica varía mucho entre estos 3 peligros:

| Peligro | Cantones con historial | Cantones rellenados con 0 | % rellenado |
|---|---|---|---|
| Deslizamiento | 186/221 | 35 | 15.8% |
| Socavamiento | 154/221 | 67 | 30.3% |
| Aluvión | 89/221 | **132** | **59.7%** |

**Aluvión es un caso límite del relleno con ceros:** más de la mitad del país (132/221 cantones) nunca registró un evento de aluvión en 2015-2025. La decisión de Jerson (rellenar con 0 en vez de excluir) sigue siendo correcta metodológicamente — esos cantones genuinamente no tienen historial — pero implica que el mapa de aluvión tiene una masa mucho mayor de "Muy Baja" cronicidad por diseño (132/221 = 59.7% de los cantones parten de EFCI=0), no solo por ausencia real de riesgo en algunos casos marginales. Se documenta como limitación explícita, no se oculta.

## 3. Resultados reales — patrones geográficos claramente distintos entre los 3 peligros y de inundación

**Deslizamiento (Gi*, capa EFCI):** 61 puntos calientes / 39 fríos de 221. Hotspots 99% concentrados en la **sierra centro-sur** (Guaranda, Riobamba, Colta, Guano, Pallatanga — corredor Bolívar-Chimborazo) y una segunda bolsa en el **oriente norte** (Archidona, El Chaco, Quijos — Napo). Coldspots casi exclusivamente en la **costa baja de Guayas** (Guayaquil, Daule, Milagro, Samborondón, Balzar) — el patrón geográfico opuesto al de inundación, consistente con que los deslizamientos requieren pendiente (sierra), mientras que la costa baja es justamente donde se concentra la inundación. Top EFCI: **Distrito Metropolitano de Quito** (0.637, primer lugar — a diferencia de inundación donde Quito era 2º), Ambato (0.491), San Pedro de Pelileo (0.448), Baños de Agua Santa (0.439), Loja (0.404). Cobertura hexagonal verificada: 523 celdas, suma de eventos = 12,625 (coincide exactamente con el total `hazard_type=="landslide"`).

**Socavamiento (Gi*, capa EFCI):** 48 puntos calientes / 22 fríos de 221 — la Gi* más "caliente-dominante" de los 4 peligros (pocos fríos). Hotspots 99% mezclan zonas de costa baja con ríos grandes (Baba, Puebloviejo, Urdaneta — Los Ríos) y zonas andinas (Quijos, Cayambe, Mejía) — coherente con que el socavamiento (erosión de cauces/riberas) ocurre donde hay ríos con caudal fuerte, tanto en tierras bajas como en quebradas andinas. Top EFCI: Distrito Metropolitano de Quito (0.392), El Chaco (0.366, Napo), Cuenca (0.306), Babahoyo (0.297), Pallatanga (0.281). Hexágonos: 370 celdas, suma = 1,152 eventos (coincide exactamente).

**Aluvión (Gi*, capa EFCI):** 48 puntos calientes / 50 puntos fríos de 221 — la distribución más equilibrada caliente/frío de los 4 (consistente con la baja cobertura histórica, §2). Hotspots 99% en la **sierra** (Mira-Carchi, Pujilí-Cotopaxi, Riobamba-Colta-Guano-Chimborazo, Portovelo-El Oro) y un punto costero (San Vicente-Manabí). Coldspots concentrados en la **costa baja de Guayas** (Guayaquil, Daule, Durán, Milagro, Naranjito) — mismo patrón que deslizamiento, coherente con que aluvión (flujo de detritos) es un fenómeno de pendiente igual que deslizamiento, aunque con dinámica distinta. Top EFCI: **Baños de Agua Santa** (0.313, primer lugar — el cantón del volcán Tungurahua, coherente con lahares/flujos volcánicos históricos), Quito (0.306), Riobamba (0.248), Mejía (0.226), El Chaco (0.224). Hexágonos: 188 celdas, suma = 685 eventos (coincide exactamente).

**Verificación de sentido común (Quito) — resultado real, no forzado:** Quito es hotspot Gi* significativo al 95% en deslizamiento y aluvión (coherente con eventos reales documentados, incl. el evento de 2022 ya discutido en Fase 4), pero **no** es significativo en socavamiento ni (como ya se documentó en `09b`) en inundación específicamente — un patrón consistente: la cronicidad alta de Quito en el EFCI combinado está impulsada principalmente por deslizamiento/aluvión (fenómenos de pendiente), no por inundación ni socavamiento.

## 4. Clases Jenks resultantes (5 clases, `jenkspy`, recalculadas por peligro — mismo método que 09b/10b)

| Peligro | Muy Baja | Baja | Moderada | Alta | Muy Alta |
|---|---|---|---|---|---|
| Deslizamiento | 51 | 76 | 62 | 28 | 4 |
| Socavamiento | 67 | 57 | 49 | 35 | 13 |
| Aluvión | 132 | 30 | 34 | 22 | 3 |

La masa de "Muy Baja" en aluvión (132/221, 59.7%) es consecuencia directa del relleno con ceros (§2), no un artefacto del método Jenks en sí.

## 5. Exportación

Mismos 4 productos por peligro que en `09b`, con sufijo `_landslide`/`_scour`/`_debris_flow`: `hotspots_gi_star_canton_*`, `local_moran_canton_*`, `kde_severidad_grid_*`, `hexagonos_h3_res5_*` — todos en `data/processed/`.

## 6. Referencias

- `docs/methodology/09b_spatial_analysis_flood.md` — método base completo y justificación de las decisiones de diseño compartidas.
- `docs/methodology/09_spatial_analysis.md` — versión combinada original (`"TODOS"`).
