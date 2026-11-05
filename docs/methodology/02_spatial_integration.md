# 02 — Integración espacial

**Fase:** 2 de 10 (ver Fase 0, §8 Pipeline completo)
**Notebook asociado:** `notebooks/Step2_Ecuador_Spatial_Integration.ipynb`
**Estado:** implementado y ejecutado — 2026-08-05 (v2: incluye confirmación cruzada por parroquia, §4.7)
**Audiencia:** científicos, desarrolladores, especialistas GIS

## 1. Objetivo de la fase

Convertir la tabla `Hazard_Event` (Fase 1, tabular) en una capa geoespacial
de puntos, incorporar los límites administrativos oficiales de Ecuador
(provincia/cantón/parroquia), validar espacialmente la geolocalización
reportada por SNGRE, armonizar nombres oficiales, y exportar ambas capas en
formatos SIG estándar (GeoPackage, GeoJSON).

Esta fase **no** calcula indicadores ni hotspots (Fase 3 y Fase 9). Su único
propósito es dejar la base lista para análisis espacial, con la calidad de
la geolocalización explícitamente cuantificada, no asumida.

## 2. Fundamento científico y geoespacial

Se resuelve la decisión abierta en el diseño Fase 0 (§19.4, "INEC vs.
OCHA"): el dataset "Ecuador - Subnational Administrative Boundaries" de HDX
(cod-ab-ecu, actualizado 2024-12-18) está declarado por HDX como derivado
directamente de INEC — no es una fuente alternativa/competidora, es la
misma fuente oficial empaquetada en formato SIG con códigos Pcode
estandarizados para uso humanitario. Esto es consistente con el patrón ya
identificado en los proyectos de Acción Anticipatoria de Somalia (Fase 0,
uso de Pcode OCHA/IOM DTM).

## 3. Fundamento estadístico y geoespacial

- **CRS único de trabajo:** EPSG:4326 (WGS84), forzado explícitamente en
  todas las capas aunque ya vinieran así, para no depender de que la fuente
  no cambie de CRS en una actualización futura.
- **Doble verificación de la geolocalización:** en vez de asumir que la
  coordenada reportada por SNGRE es correcta, se contrasta contra el cantón
  también reportado por SNGRE mediante una unión espacial punto-en-polígono
  independiente. El desacuerdo entre ambos es información de calidad, no un
  error a esconder.
- **Simplificación geométrica solo para los productos de visualización**
  (GeoJSON), nunca para el GeoPackage de trabajo — ver §4.4.

## 4. Decisiones metodológicas y su justificación

### 4.1 Excepción de adquisición de datos

El entorno de ejecución tiene salida de red restringida a una lista blanca
de dominios; no fue posible descargar el shapefile directamente desde
HDX/INEC/IGM (`curl`/fetch de página verificado y bloqueado). Jerson
descargó manualmente `ecu_adm_2024.zip` (cod-ab-ecu, HDX) y lo colocó en la
carpeta del proyecto. **Ventaja:** no depende de que el entorno de ejecución
tenga acceso a internet — el pipeline es reproducible offline una vez que el
archivo está presente. **Limitación:** cualquier actualización futura del
dataset (HDX indica actualización anual) requiere descarga manual, no es
automática.

### 4.2 Niveles administrativos usados: ADM0–ADM3, se excluye ADM4

Se cargan ADM0 (país, 1 feature, solo contexto cartográfico), ADM1
(provincia, 24), ADM2 (cantón, 221) y ADM3 (parroquia, 1,042, nivel
opcional del diseño). **ADM4 (52,958 features, 656 MB) se descarga pero no
se usa**: no forma parte del esquema `Admin_Boundary` (Fase 0 §7.2,
provincia/cantón/parroquia) y su resolución (sub-parroquial/censal) excede
lo necesario para un índice a nivel cantonal. Queda documentado como capa
disponible para una fase futura de mayor resolución espacial.

### 4.3 Código DPA (INEC) como llave de unión, no el nombre de texto libre

Se verificó empíricamente que `ADMx_PCODE` de HDX = `"EC"` + código DPA de
INEC (p. ej. `EC0101` = cantón 0101 = Cuenca), y que ese código DPA coincide
**100%** con `province_code`/`canton_code` ya presentes en `Hazard_Event`
desde la Fase 1 (24/24 provincias, 221/221 cantones — ninguna provincia ni
cantón de `hazard_event` queda sin límite administrativo, verificado con
aserciones que detienen el pipeline si fallan). Esto confirma la decisión de
diseño de la Fase 0 (§7.2, heredada de Somalia): usar Pcode/código DPA como
llave de unión, nunca el nombre de texto libre.

**Por qué es la decisión correcta:** el nombre de texto libre de SNGRE tiene
inconsistencias reales — 9 de 24 provincias presentan más de una variante de
escritura en `hazard_event` (tildes, mayúsculas, abreviaturas). Unir por
nombre habría requerido normalización de texto adicional y quedaría expuesto
a colisiones; unir por código DPA es determinístico y ya estaba validado al
100%.

### 4.4 `canton_code` (reportado) como campo autoritativo; unión espacial como control de calidad, no como reemplazo

El pipeline mantiene **intacto** el `canton_code`/`canton` que SNGRE reportó
en cada evento (heredado de la Fase 1, campo autoritativo para todo el
proyecto) y añade por separado, vía unión espacial punto-en-polígono
(`gpkg.sjoin`, `predicate="within"`), un cantón "geométrico"
(`canton_code_geo`, `canton_name_geo`) y una bandera
`canton_geo_matches_reported`.

**Resultado:** 97.97% de coincidencia entre el cantón reportado y el
geométrico; 0.16% (35 eventos) sin ningún polígono contenedor (coordenada
cae fuera de todo cantón, típicamente en el mar — concentrado en cantones
costeros: Esmeraldas, Galápagos, Manabí, Santa Elena, El Oro); 1.87% (406
eventos) con polígono encontrado pero distinto del cantón reportado,
concentrado en Guayas (66), Morona Santiago (64), Loja (40), Esmeraldas
(36) y Pichincha (36).

**Justificación de por qué NO se sobrescribe `canton_code` con el
resultado geométrico:** un desacuerdo punto-en-polígono puede deberse a (a)
error de geocodificación (coordenada mal capturada por el operador SNGRE),
(b) redondeo de coordenadas cerca de un límite cantonal, o (c) el cantón
reportado ser correcto pero la coordenada capturada corresponder a una
ubicación de referencia distinta (p. ej. la cabecera cantonal más cercana en
vez del sitio exacto del evento) — en ninguno de estos casos el polígono
geométrico es automáticamente "más correcto" que el dato administrativo
reportado. La bandera queda disponible para que fases posteriores decidan
tratamiento diferenciado (p. ej. excluir del análisis espacial fino los
eventos con baja confianza), sin perder ningún evento del conteo total.

**Alternativa descartada:** usar el cantón geométrico como autoritativo y
descartar el reportado. Se descartó porque introduciría exactamente el tipo
de "corrección silenciosa" que el proyecto busca evitar (ver regla de
documentación honesta, Fase 0).

### 4.7 Confirmación cruzada por parroquia (ADM3) — resuelve la mayoría de la ambigüedad de §4.4

**Origen:** Jerson observó que, incluso en los eventos con problemas de
coordenada, SNGRE reportó de todos modos un nombre/código de parroquia
(`parish_code`, campo ADM3), no usado en la primera versión de esta fase, y
preguntó si un cruce a nivel de parroquia lograría 100% de coincidencia
espacial y de nombres.

**Verificado con datos, no asumido:** la cobertura de `parish_code` contra
el ADM3 2024 de HDX es del **80.7%** en todo el dataset (17,549 de 21,743
eventos), estable entre 76% y 88% año a año — no es un problema concentrado
en registros antiguos. Adoptar parroquia como unidad base de análisis
**empeoraría** la cobertura actual (cantón = 100%) en vez de mejorarla, por
lo que se descarta como capa base. Sí resulta extremadamente útil como
**confirmación dirigida** de los casos ambiguos de §4.4:

- De los eventos con `parish_code` válido, el **100%** confirma el
  `canton_code` que SNGRE ya había reportado directamente (0% confirma el
  cantón geométrico calculado en §4.4) — evidencia fuerte adicional de que
  el desacuerdo punto-en-polígono se debe a imprecisión de coordenada, no a
  codificación cantonal incorrecta.
- De los 35 eventos sin polígono cantonal (§4.4): **30 quedan confirmados**
  por parroquia (cantón reportado correcto). Los 5 restantes —todos de la
  parroquia "5 De Agosto"/"Esmeraldas" en el cantón Esmeraldas— no tienen
  `parish_code` válido en el ADM3 2024 (posible reclasificación/fusión de
  parroquia urbana no reflejada aún en el snapshot).
- De los 406 eventos con cantón geométrico distinto del reportado (§4.4):
  **363 quedan confirmados** por parroquia a favor del cantón reportado.

Se añade una columna de confianza consolidada, `canton_confidence`, con tres
valores: `alta` (geometría o parroquia confirman el cantón reportado —
99.78% de los eventos, 21,695 de 21,743), `revisar` (ninguna de las dos
verificaciones confirma y al menos una las contradice — 43 eventos, 0.20%),
`baja_sin_parroquia` (sin polígono ni parroquia disponible para confirmar,
no es evidencia de error, es ausencia de evidencia — 5 eventos, 0.02%).

**Por qué no se usa la parroquia como sistema de reemplazo:** su cobertura
parcial (80.7%) la descalifica como base; su valor es como segunda fuente
de evidencia independiente para los casos ya señalados por §4.4, no como
sustituto del cruce por `canton_code`.

### 4.5 Simplificación geométrica solo en los GeoJSON de visualización

La geometría original (línea de costa de alta resolución) genera GeoJSON de
92–293 MB, inviable para un dashboard web. Se aplicó
`simplify(tolerancia=0.0005°, preserve_topology=True)` (~50 m en el
ecuador) **únicamente** a las copias GeoJSON de ADM1/ADM2 para
visualización; el GeoPackage (`admin_boundaries.gpkg`) conserva la
geometría original sin simplificar para cualquier análisis espacial fino de
fases futuras (Getis-Ord Gi*, Moran's I, etc., que si son sensibles a la
simplificación).

### 4.6 Escritura vía directorio temporal local (limitación de infraestructura, no de diseño)

La carpeta del proyecto está montada como sistema de archivos remoto que no
soporta el bloqueo de archivos (file locking) que SQLite requiere para
escribir un GeoPackage — la escritura directa falla con
`"no such table: gpkg_contents"`. Se resuelve escribiendo primero en un
directorio temporal local y copiando los archivos ya cerrados/completos al
destino final (operación de copia simple, sí soportada). Documentado aquí
para que no se interprete como parte del diseño científico del pipeline —
es una adaptación de infraestructura.

## 5. Esquema de salida

- `admin_boundaries.gpkg`: 4 capas (`adm0_country`, `adm1_province`,
  `adm2_canton`, `adm3_parish`), geometría original sin simplificar, EPSG:4326.
- `hazard_event_geo.gpkg`: capa de puntos, 21,743 features, todas las
  columnas de `Hazard_Event` (Fase 1) + `canton_code_geo`, `canton_name_geo`,
  `province_name_official`, `canton_name_official`, `canton_geo_matches_reported`,
  `canton_code_from_parish`, `canton_confirmed_by_parish`, `canton_confidence`
  (`alta` / `revisar` / `baja_sin_parroquia` — ver §4.7).
- `adm1_province.geojson` / `adm2_canton.geojson`: copias simplificadas para
  visualización web (Fase 0 §9, dashboard).

## 6. Limitaciones

- ADM3 (parroquia) tiene una discrepancia conocida y documentada por la
  propia HDX: 1,042 features vs. 1,025 en las tablas de población COD-PS —
  no se investigó más a fondo por ser un nivel opcional del diseño.
- 35 eventos (0.16%) sin polígono cantonal geométrico contenedor —
  concentrados en cantones costeros/insulares, consistente con imprecisión
  de coordenadas cerca de la línea de costa, no con un error sistemático.
- Para esos mismos 35 eventos, `province_name_official`/`canton_name_official`
  también quedan nulos (se derivan del mismo join espacial) aunque el
  `province_code`/`canton_code` original sigue siendo válido y utilizable —
  ver mejora futura en §9.
- 406 eventos (1.9%) con cantón geométrico distinto del reportado — resuelto
  en un 89.4% por la confirmación de parroquia (§4.7, 363 de 406 a favor del
  cantón reportado); quedan 43 eventos (0.20% del total) sin ninguna
  confirmación, clasificados `canton_confidence == "revisar"`.
- 5 eventos (0.02%) sin ninguna evidencia disponible (ni geometría ni
  parroquia) para confirmar el cantón reportado — no es evidencia de error,
  es ausencia de evidencia (`canton_confidence == "baja_sin_parroquia"`).
- La cobertura de `parish_code` contra ADM3 2024 es de solo 80.7% en todo el
  dataset — no se investigó la causa exacta (posibles fusiones/creaciones de
  parroquias entre el momento de cada reporte SNGRE y el snapshot 2024).
- El dataset HDX se actualiza anualmente; esta fase usa el snapshot
  2024-12-18, no una versión en vivo.

### 4.8 Resolución de pendientes: qué es `Base2`, y contraste contra el modelo COE existente

**Qué es `Base2` (workbook maestro, no generado por este pipeline).**
Determinado con coincidencia **exacta** de los 16,465 ID (no una
aproximación): `Base2 = BD_2015_2025` restringida a los 38 meses con
impacto ENSO documentado en `Notas Metodológicas` (2015 completo; 2016
ene–jun; 2017 ene–may; 2023 mar–dic; 2024 ene–may) **y** excluyendo 8
provincias — Tungurahua, Morona Santiago, Zamora Chinchipe, Napo, Pastaza,
Orellana, Sucumbíos y Galápagos (Amazonía/Oriente + Tungurahua + insular).
`Base2` es el insumo exacto del modelo `Escenarios y Nivel de Respuesta`
preexistente en el workbook, no una base alternativa de `Hazard_Event`.

**Metodología exacta del `Máximo Impacto Histórico` del modelo COE,
reproducida y verificada:** `MAX(PERSONAS AFECTADAS DIRECTAMENTE)` por
cantón, calculado sobre `Base2` — **sin** filtrar por tipo de evento (usa
los 16 tipos de peligro presentes en `Base2`, no solo los 4 de nuestro
alcance). Verificado contra 134/141 cantones de la hoja `Escenarios y
nivel de respuesta`; los 7 restantes son solo variantes de nombre
(`Puerto Ayora`/`Santa Cruz`, `Distrito Metropolitano de Quito`/`Quito`,
etc.) o cantones de Galápagos, excluidos de `Base2` por diseño — no son
discrepancias de método.

**Contraste con nuestro alcance de peligro (hallazgo nuevo, no estaba en la
v1 de este documento):** en 93 de 134 cantones (69%), el evento que produjo
el `Máximo Impacto Histórico` del modelo COE SÍ pertenece a nuestro alcance
(inundación/aluvión/deslizamiento/socavamiento) — el modelo COE y el HCI
miden esencialmente lo mismo en esos casos. En los 41 restantes (31%), el
máximo proviene de un tipo de evento **fuera** de nuestro alcance que cayó
dentro de la misma ventana de 38 meses "ENSO": Sismo (19 cantones —
coincide con el terremoto de abril de 2016, que cayó dentro de la ventana
2016 ene-jun sin tener relación causal con ENSO), erupción volcánica (3,
incluyendo Chillanes con 35,800 personas afectadas — muy probablemente
Cotopaxi/Tungurahua, no El Niño), vendaval (5), déficit hídrico (4), y
otros. **Implicación:** el modelo COE existente, al restringir por mes
pero no por tipo de peligro, puede sobreestimar el riesgo específico de El
Niño en cantones donde el evento históricamente más severo fue en realidad
un sismo o una erupción que coincidió por calendario, no por causa. El HCI,
al filtrar por tipo de peligro desde la Fase 1, no hereda ese problema. Ver
`outputs/tables/cierre_pendientes_fase2.xlsx` (hoja `Comparacion_COE`) para
el detalle cantón por cantón.

**Los 43 eventos `canton_confidence == "revisar"` (§4.7):** revisados
manualmente contra la descripción de texto libre del reporte original de
SNGRE cuando estaba disponible. No se encontró un patrón de error
sistemático — la mayoría son pares de cantones vecinos dentro de la misma
provincia (Rumiñahui/Quito, Loja/Catamayo, Gualaquiza/Limón Indanza),
consistente con una coordenada cercana a la cabecera cantonal que cae del
otro lado del límite administrativo. En al menos un caso verificado
(evento 57996), la descripción del evento nombra explícitamente el cantón
reportado ("cantón Chone"), no el geométrico (Pichincha) — refuerzo
adicional para mantener `canton_code` como autoritativo también en estos 43
casos. Ver `outputs/tables/cierre_pendientes_fase2.xlsx` (hoja `Revisar_43`).

## 7. Supuestos

- El código DPA de INEC embebido en `Hazard_Event` desde SNGRE usa la misma
  versión/vigencia de codificación cantonal que el snapshot 2024 de HDX (no
  se verificó explícitamente que no haya habido creación/fusión de cantones
  entre el momento de cada reporte SNGRE y 2024).
- La coordenada (`latitude`/`longitude`) de cada evento representa un punto
  puntual válido, no un área — no se investigó si algunos registros usan en
  realidad la cabecera cantonal como proxy de ubicación.

## 8. Ventajas del enfoque

- Doble verificación (atributo + geometría) sin pérdida de eventos: los 35
  y 406 casos quedan señalados, no descartados.
- Reproducible offline una vez presente el shapefile (no depende de acceso
  a red en tiempo de ejecución).
- Geometría de trabajo (GeoPackage) sin simplificar, apta para análisis
  espacial fino futuro; geometría de visualización (GeoJSON) optimizada por
  separado, sin contaminar la capa de trabajo.

## 9. Posibles mejoras futuras

- Backfill de `province_name_official`/`canton_name_official` para los 35
  eventos sin polígono geométrico, usando una búsqueda por atributo
  (`canton_code` → tabla `adm2`) en vez de depender del resultado espacial —
  mejora sencilla, de bajo impacto (0.16% de las filas), pendiente por
  prioridad.
- Revisar manualmente los 43 eventos `canton_confidence == "revisar"` contra
  el reporte SNGRE original (más práctico ahora que el grupo se redujo de
  406 a 43 gracias a §4.7).
- Investigar por qué la cobertura de `parish_code` contra ADM3 es solo
  80.7% — posible indicio de que el snapshot 2024 de parroquias difiere más
  de lo esperado de la codificación usada por SNGRE en años anteriores.
- Automatizar la verificación de vigencia de códigos cantonales entre la
  fecha de cada evento y la versión de límites administrativos usada.

## 10. Referencias

- Fase 0 — Diseño Conceptual HCI Ecuador, §7.2, §19.4.
- HDX — "Ecuador - Subnational Administrative Boundaries" (cod-ab-ecu),
  INEC, actualizado 2024-12-18.
- `docs/methodology/01_data_ingestion.md` (Fase 1, insumo de esta fase).
