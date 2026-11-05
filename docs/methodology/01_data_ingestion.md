# 01 — Ingesta y armonización de la base histórica de eventos

**Fase:** 1 de 10 (ver Fase 0, §8 Pipeline completo)
**Notebook asociado:** `notebooks/Step1_Ecuador_Hazard_Event_Ingestion.ipynb`
**Estado:** implementado y ejecutado — 2026-08-05 (v1.1: corrección de dato puntual, 2026-08-06, §4.6)
**Audiencia:** científicos, desarrolladores, especialistas GIS

## 1. Objetivo de la fase

Construir la tabla `Hazard_Event`, limpia, armonizada y trazable, a partir de
la base histórica cruda de eventos de desastre del SNGRE/ECU911
(`BD_2015_2025`, hoja del workbook maestro `Indices ENSO (1).xlsx`), y
enriquecerla con el índice ENSO mensual completo (ICEN/ONI) para el periodo
2015–2025. Esta tabla es el insumo único para todas las fases posteriores
(2–10): sin una base de eventos confiable y bien documentada, ningún índice
derivado (Recurrencia, Severidad, Persistencia, HCI) es defendible.

Esta fase **no** calcula índices, umbrales ni criterios de cohorte ENSO —
esa responsabilidad se reserva a la Fase 3 (análisis histórico) y Fase 8
(HCI), para mantener una separación clara de responsabilidades entre fases
(principio de arquitectura modular, ver diseño Fase 0 §5).

## 2. Fundamento científico y de gestión de riesgo

La base `BD_2015_2025` es un registro operacional de eventos adversos
reportado por operadores de SNGRE/ECU911 a nivel de parroquia, con
coordenadas, fecha e impacto multisectorial (población, vivienda, educación,
salud, infraestructura, agricultura, ganadería). Es consistente con el tipo
de fuente usado en los marcos de Acción Anticipatoria de FAO ya revisados
(Etiopía, Somalia, Kenya, Sudán del Sur, Afganistán — ver Fase 0), que
también parten de bases de impacto reportado a nivel subnacional, no de
modelos físicos, en su primera fase.

## 3. Fundamento estadístico y geoespacial

- **Filtrado por tipo de evento**, no por texto libre de causa, para
  garantizar reproducibilidad — la columna `EVENTO` es un campo controlado
  (lista cerrada de valores), mientras que `CAUSA` es texto semi-libre.
- **Validación de coordenadas** contra un bounding box de Ecuador
  (continental + Galápagos) como control de calidad geoespacial mínimo,
  sin descartar registros — se marcan (`coord_valid`), permitiendo que
  fases posteriores decidan el tratamiento (ver §6).
- **Serie ENSO mensual completa por reconstrucción, no por tabla curada**:
  se comprobó que la hoja `2015 2025 (mes)` del workbook maestro no cubre
  los 132 meses del periodo 2015–2025 (solo 38–52 meses con impacto
  documentado, ver Notas Metodológicas del propio workbook). Para tener
  cobertura mensual completa y auditable, la serie se reconstruye desde
  `ICEN_Trimestral` y `ONI trimestral` (formato largo, 1950–presente).

## 4. Decisiones metodológicas y su justificación

### 4.1 Alcance de peligro ampliado (decisión 2026-08-05)

El alcance de HCI v1 no se limita a `EVENTO == "Inundación"`. Por
instrucción explícita de Jerson ("debe incluir floods (riverine, flash),
landslide, scour, y lo detectable temporalmente con las imágenes o procesos
que vamos a hacer"), se incluyen cuatro tipos de evento:

| EVENTO (SNGRE) | `hazard_type` | Filas 2015–2025 |
|---|---|---|
| Inundación | `flood` | 7,281 |
| Aluvión (Flujos) | `debris_flow` | 685 |
| Deslizamiento | `landslide` | 12,625 |
| Socavamiento | `scour` | 1,152 |
| **Total** | | **21,743** |

**Ventaja:** trata el complejo hidrometeorológico como una unidad, coherente
con el hecho de que estos cuatro peligros comparten el mismo forzante
(lluvias intensas asociadas a ENSO — confirmado empíricamente: 90.8% de
estos eventos tiene `Eventos_Lluvias = 1` en la fuente) y con la visión de
diseño hazard-agnóstico del proyecto (Fase 0 §17). También deja el esquema
listo para incorporar detección remota futura (Sentinel-1 para inundación,
InSAR para deslizamiento) sin rediseñar la tabla.

**Limitación:** mezclar hazards con dinámicas físicas distintas (inundación
vs. deslizamiento) en un mismo índice de cronicidad requiere que la Fase 3+
mantenga `hazard_type` como variable de segmentación explícita — el HCI no
debe promediar across hazards sin decisión explícita al respecto (pendiente
de discutir en Fase 3).

**Alternativa considerada y descartada:** limitar a `Inundación` estricto
(alcance del brief original). Se descartó por instrucción directa del
usuario, documentada aquí para trazabilidad de la decisión.

### 4.2 Sub-clasificación fluvial/pluvial/costera (heurística, no campo oficial)

La fuente no distingue el mecanismo de inundación. Se deriva `flood_subtype`
a partir de palabras clave en `CAUSA` (`desbordamiento` → `riverine`;
`aguaje`/`marejada` → `coastal`; `lluvias(intensas)` → `pluvial_flash`).

Resultado empírico sobre `flood` + `debris_flow` (n = 7,966):

| flood_subtype | n | % |
|---|---|---|
| pluvial_flash | 7,113 | 89.3% |
| riverine | 550 | 6.9% |
| other | 263 | 3.3% |
| coastal | 40 | 0.5% |

**Ventaja:** permite un análisis diferenciado (crecidas fluviales vs. lluvia
directa) sin esperar a capas hidrológicas (DEM, red de drenaje) que son
trabajo de fases futuras.

**Limitación explícita:** es un heurístico de texto libre. `CAUSA = "Lluvias"`
sin más detalle no distingue realmente pluvial de fluvial cuando la crecida
del río es la causa real pero el operador solo registró "lluvias". Debe
tratarse como variable exploratoria, no como verdad de terreno, hasta que se
valide contra capas hidrológicas (Fase futura, CHIRPS/GloFAS/DEM).

### 4.3 Reconstrucción de la serie ENSO mensual (validación empírica de la convención trimestre→mes)

Las hojas `ICEN`/`ONI` (formato ancho) usan 12 códigos de trimestre móvil
(`DEF, EFM, FMA, MAM, AMJ, MJJ, JJA, JAS, ASO, SON, OND, NDE`). Se validó
empíricamente que cada código corresponde al **mes central** del trimestre
(p. ej. `DEF` = Dic-Ene-Feb → mes central = Enero), comparando los valores
derivados contra la hoja curada `2015 2025 (mes)` para 2015: coinciden
exactamente (ICEN Enero 2015 = -0.08 en ambas fuentes; Febrero = -0.14;
Marzo = 0.26 — ver notebook, sección 8). Esta convención se codificó en
`config.yaml → trimester_to_month` y no debe asumirse para otros productos
ENSO sin validación propia.

**Resultado:** serie mensual completa, 132/132 meses (2015–2025), sin nulos
en ICEN ni ONI, con categoría oficial ya calculada por el equipo COE
(`icen_category`, `oni_category`).

**Por qué no usar directamente `2015 2025 (mes)`:** esa hoja está
deliberadamente restringida a meses con impacto ENSO documentado (criterio
de negocio válido para el modelo de Escenarios existente, ver Notas
Metodológicas), pero no es una serie climatológica completa — usarla como
tal introduciría 60%+ de valores faltantes en el join con eventos, como se
comprobó en el prototipo (tasa de emparejamiento 40.1% vs. 100% con la
reconstrucción trimestral).

### 4.4 Tratamiento de PII en la columna `Fuente`

Se detectó que el 80.9% de las filas dentro del alcance filtrado contienen
un patrón de teléfono en `Fuente` (nombres y números de operadores
SNGRE/ECU911). Por gobernanza de datos de un producto institucional FAO, la
tabla procesada reemplaza esta columna por `source_type = "SNGRE_ECU911_report"`
y una bandera `source_has_pii`; el texto crudo permanece únicamente en el
workbook original (`data/raw`, sin modificar).

**Justificación:** un producto FAO destinado a compartirse con contrapartes
y potencialmente publicarse no debe exponer datos personales de operadores
de emergencia. **Limitación:** se pierde la trazabilidad fina hacia el
reporte individual; si se necesitara auditar un evento específico, debe
hacerse contra el workbook crudo, no contra `Hazard_Event`.

### 4.5 No se usó `Base2`

`Base2` (16,465 filas) es un subconjunto de `BD_2015_2025` cuyo criterio de
filtro exacto no pudo inferirse automáticamente (no corresponde a un filtro
simple por fecha, tipo de evento o categoría). Por instrucción del usuario,
se usa `BD_2015_2025` completa como fuente única de verdad, y se aplican
criterios de filtrado propios, documentados y reproducibles (este
documento), en lugar de heredar un filtro manual no documentado.
**Pendiente:** confirmar con el equipo qué representa `Base2` — podría
aportar una señal de calidad adicional útil en fases futuras.

### 4.6 Corrección de dato puntual: evento ID 51387 (2026-08-06)

**Origen del hallazgo:** no surgió en esta fase, sino en la Fase 8 (HCI
compuesto), cuya prueba de sensibilidad de outliers de Severidad (§5.3 de
`08_hci_composite.md`) identificó que un solo evento dominaba
desproporcionadamente el pilar Ganadería del Índice de Severidad (Fase 4
§6): evento ID 51387, Baños de Agua Santa (Tungurahua), aluvión en Río
Negro, 2021-09-05, columna `ANIMALES MUERTOS` = 500,000.

**Verificación antes de corregir (no se corrige por sospecha, se corrige
con evidencia):**
1. La misma fila trae `ANIMALES AFECTADOS` = 0 — inconsistente (no puede
   haber 0 animales afectados y 500,000 muertos).
2. La `DESCRIPCIÓN GENERAL DEL EVENTO` en SNGRE es extensa y detallada
   día a día (más de 20 entradas entre el 5 de septiembre y el 24 de
   noviembre de 2021) y no menciona ninguna cifra de animales muertos —
   solo una línea genérica de MAG sobre "afectación pecuaria".
3. Búsqueda en prensa independiente (El Comercio, El Universo, La Hora,
   septiembre 2021) confirma el evento — 3 fallecidos, 2 desaparecidos,
   ~50 personas incomunicadas, pérdidas estimadas por el alcalde de Baños
   en 600,000 USD — sin mencionar pérdida de ganado en ningún artículo.
   500,000 animales muertos superaría varias veces esa pérdida total
   estimada, para una comunidad rural de unas pocas decenas de familias.

**Decisión (Jerson, 2026-08-06):** corregir el valor a 0 (consistente con
`ANIMALES AFECTADOS`=0 en la misma fila), aplicado en el origen (esta
fase, antes de cualquier filtro), documentado en `config.yaml` →
`known_data_corrections` con verificación explícita (`original_value`
comprobado antes de sobrescribir) y log de auditoría
(`logger.warning`). El workbook original **no se modifica** — la
corrección vive únicamente en el pipeline.

**Por qué corregir en el origen (Fase 1) y no en la Fase 4:** las 7 fases
posteriores (2–8) derivan todas de `Hazard_Event`; parchear el valor solo
en Severidad habría dejado las tablas de Fase 3 (estadísticos de impacto)
mostrando el valor erróneo sin que nadie lo supiera. Corregir en el origen
garantiza que todas las fases hereden el dato correcto automáticamente —
se re-ejecutó la cadena completa Step1→Step8 tras aplicar la corrección.

## 5. Esquema de salida (`Hazard_Event`)

40 columnas — identificación y ubicación (`event_id`, `province`,
`province_code`, `canton`, `canton_code`, `parish`, `parish_code`,
`latitude`, `longitude`, `coord_valid`), tipificación del evento
(`hazard_type`, `flood_subtype`, `cause_raw`, `event_date`, `year`, `month`),
~20 variables de impacto (población, vivienda, educación, salud, agricultura,
ganadería), gobernanza de fuente (`source_type`, `source_has_pii`), y
enriquecimiento ENSO (`ICEN`, `icen_category`, `ONI`, `oni_category`).

Se exporta también `ENSO_Index_Monthly` (132 filas, 2015–2025) como tabla
independiente reutilizable por cualquier fase futura sin releer el Excel.

Formatos de salida: Parquet (consumo por el pipeline, tipado preservado) y
CSV (inspección manual). Ubicación: `data/processed/`.

## 6. Limitaciones

- `flood_subtype` es heurístico (texto libre), no un campo estructurado —
  ver §4.2.
- El criterio de filtro de `Base2` queda sin resolver — ver §4.5.
- 0% de coordenadas inválidas o nulas en el alcance filtrado (validado), pero
  no se verificó la **precisión** de la geolocalización (p. ej. si el punto
  reportado es el lugar exacto del evento o un centroide administrativo) —
  pendiente de discusión con la fuente.
- La categorización ICEN/ONI proviene de un producto de terceros (ENFEN
  Perú vía el workbook maestro) — no se recalculó desde SST cruda; es
  consistente con el uso planeado de Niño 1+2 SST (GEE) como capa
  complementaria en fases futuras, no como reemplazo.
- Mezclar 4 tipos de hazard en una sola tabla requiere disciplina en fases
  posteriores para no promediar impactos de naturaleza física distinta sin
  justificación explícita.

## 7. Supuestos

- La columna `EVENTO` es un campo controlado y confiable para filtrar por
  tipo de peligro (no se validó contra una fuente externa).
- El mes calendario "central" del trimestre móvil ENSO es la asignación
  correcta para el join evento-ENSO (validado empíricamente para 2015, no
  para todo el rango 2015–2025 punto por punto).
- Todas las filas de `BD_2015_2025` provienen de reportes SNGRE/ECU911 (según
  Notas Metodológicas del workbook), lo que justifica generalizar `Fuente` a
  un único `source_type`.

## 8. Ventajas del enfoque

- 100% reproducible: cada decisión de filtrado vive en `config.yaml`, no
  hardcodeada.
- 100% trazable: cada fila conserva `event_id` original de SNGRE.
- Serie ENSO mensual completa y validada, sin depender de una tabla parcial.
- Cumple gobernanza de datos (PII) desde la primera fase, no como parche
  posterior.

## 9. Posibles mejoras futuras

- Reemplazar el heurístico de `flood_subtype` por clasificación basada en
  capas hidrológicas (DEM, red de drenaje, GloFAS) cuando estén disponibles.
- Resolver y documentar el criterio de `Base2`; evaluar si aporta una
  bandera de calidad/verificación adicional.
- Añadir un proceso de deduplicación cruzada con EM-DAT/DesInventar (Fase de
  validación, Fase 0 §14).
- Evaluar precisión de geolocalización por fuente/año.

## 10. Referencias

- Fase 0 — Diseño Conceptual HCI Ecuador (`HCI_Ecuador_Fase0_Diseno_Conceptual.docx`), §7–8, §17, §19.4.
- Notas Metodológicas — hoja `Notas Metodológicas`, workbook `Indices ENSO (1).xlsx`.
- Pipelines de Acción Anticipatoria de FAO Etiopía/Somalia/Kenya (patrón de
  ingestión tabular impacto+clima, ver memoria de proyecto).
