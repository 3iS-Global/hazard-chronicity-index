# 03 — Análisis histórico descriptivo

**Fase:** 3 de 10 (ver Fase 0, §8 Pipeline completo)
**Notebook asociado:** `notebooks/Step3_Ecuador_Historical_Analysis.ipynb`
**Estado:** implementado y ejecutado — 2026-08-05
**Audiencia:** científicos, desarrolladores, especialistas GIS/DRM

## 1. Objetivo de la fase

Calcular, por provincia y por cantón, los indicadores históricos
descriptivos definidos en el diseño (Fase 0, §8 "Fase 3"): número de
eventos, años/meses afectados, frecuencia por categoría ENSO, estadísticos
de impacto (media/mediana/máximo/desviación estándar) y tendencia temporal.

Esta fase **no** calcula los índices compuestos (Severidad, Recurrencia,
Persistencia, HCI — Fase 4 a 8). Produce los insumos descriptivos que esos
índices normalizarán y ponderarán, y es también el primer punto donde el
proyecto entrega cifras interpretables (rankings, tendencias) a alguien no
técnico.

## 2. Fundamento científico

Los cuatro bloques de indicadores replican, con una adaptación, el
"chronicity framework" ya usado en los proyectos de Acción Anticipatoria de
Etiopía/Somalia citados en la Fase 0 (§19.3): recurrencia (¿con qué
frecuencia?), persistencia (¿durante cuánto tiempo dentro de cada
episodio?), severidad descriptiva (¿qué tan grave, en promedio y en el
peor caso?) y asociación con ENSO (¿coincide con episodios documentados?).
La adaptación es que aquí se calculan por separado **por tipo de peligro**
(`hazard_type`), no agregados desde el inicio — decisión heredada de la
ampliación de alcance del 2026-08-05 (inundación + aluvión + deslizamiento +
socavamiento no deben promediarse a ciegas, ver `01_data_ingestion.md`).

## 3. Fundamento estadístico

- **Mann-Kendall + pendiente de Sen** (librería `pymannkendall`) para la
  tendencia temporal, no regresión lineal: es una prueba no paramétrica,
  no asume normalidad ni una relación lineal, y es robusta a valores
  atípicos — apropiada para series de conteo de eventos por año, que son
  pequeñas (11 puntos, 2015-2025) y no necesariamente normales.
- **Reindexado explícito al rango completo 2015-2025** antes de aplicar la
  prueba: los años sin eventos se cuentan como 0, no se omiten. Omitirlos
  comprimiría artificialmente la serie y sesgaría tanto el p-valor como la
  pendiente estimada.
- **Umbral mínimo de 4 años con al menos un evento** para calcular
  Mann-Kendall (`MIN_ANIOS = 4`, convención estándar para que la prueba
  tenga sentido mínimo). Por debajo de eso se marca explícitamente
  `datos_insuficientes` — no se oculta el hecho de que no hay evidencia
  suficiente reportando un p-valor que sería engañoso.
- **Formato largo, no ancho**, para impactos y ENSO: con 10 variables de
  impacto × 4 estadísticos serían 40 columnas en formato ancho; en formato
  largo (una fila por combinación grupo + variable) es más fácil de filtrar,
  graficar y extender en fases futuras sin reescribir el esquema.
- **`n` (conteo) reportado junto a cada estadístico de impacto**: un máximo
  o una media calculados sobre 2 eventos no debe leerse con la misma
  confianza que uno calculado sobre 200 — se deja explícito en la propia
  tabla, no como nota aparte que se pueda perder.

## 4. Decisiones metodológicas y su justificación

### 4.1 Nombre oficial de cantón/provincia incorporado por atributo (`canton_code`), no heredado del cruce espacial de la Fase 2

`hazard_event_geo.gpkg` (Fase 2) ya trae `province_name_official`, pero esa
columna se derivó del cruce **espacial** punto-en-polígono de la Fase 2 y
por eso hereda sus 35 valores nulos (los eventos sin polígono contenedor,
Fase 2 §4.4) — y no trae en absoluto `canton_name_official`.

Esta fase reemplaza `province_name_official` e incorpora
`canton_name_official` mediante un join por **atributo** sobre `canton_code`
contra la capa `adm2_canton` de `admin_boundaries.gpkg` (no un join
espacial). `canton_code` es la clave 100%-completa y autoritativa reportada
por SNGRE (Fase 2 §4.4-4.8, nunca sobrescrita), así que el nombre oficial
correcto es el que corresponde a ese código en el mapa oficial — no el del
polígono geométrico que contiene el punto, que puede diferir o simplemente
no existir para 35 eventos.

**Por qué esto importa, no es cosmético:** la primera versión de este
notebook agrupaba por `["province_code", "province_name_official",
"canton_code", "canton_name_official"]` usando la columna heredada de la
Fase 2 directamente. Como `province_name_official` tenía 35 nulos, pandas
`groupby` (que por defecto descarta filas con clave nula) eliminaba esos 35
eventos silenciosamente de todas las tablas agregadas — la aserción de
totales de la sección 7 lo detectó (21,708 vs. 21,743 esperados) antes de
exportar nada. Corregido con el join por atributo descrito arriba, que
tiene cobertura 100% porque `canton_code` la tiene. Ver también §6
(historial de la corrección) y la mejora futura ya anotada en
`02_spatial_integration.md` §9, que este cambio resuelve para efectos de
esta fase (no modifica el archivo `hazard_event_geo.gpkg` de la Fase 2 en
sí, que conserva sus 35 nulos documentados).

### 4.2 Agrupación por `province_code`/`canton_code` + nombre oficial, nunca por el texto libre `province`/`canton` de SNGRE

Se descartó agrupar directamente por las columnas de texto libre `province`
y `canton` que trae SNGRE, aunque tienen cobertura 100%. Motivo: 9 de las 24
provincias tienen más de una variante de escritura en ese texto libre
(tildes, mayúsculas — documentado en Fase 2 §4.3), lo que duplicaría grupos
indebidamente. La primera versión de este notebook cometió exactamente este
error (`CANTON_COLS` con `province`/`canton` en vez de los nombres
oficiales), detectado por la misma aserción de la sección 7 (223 cantones
con eventos vs. 221 en la tabla de tendencia — 2 grupos espurios por
variantes de nombre).

### 4.3 Todo se calcula dos veces: desglosado por `hazard_type` y combinado (`"TODOS"`)

Cada una de las cuatro funciones de resumen se ejecuta sobre el subconjunto
por tipo de peligro (`admin_cols + ["hazard_type"]`) y también sobre el
total combinado, añadiendo una fila sintética `hazard_type = "TODOS"` al
resultado. Esto preserva la segmentación por tipo de peligro exigida por la
ampliación de alcance del 2026-08-05, sin perder la vista agregada que
también pide el diseño original (Fase 0 §8).

**Consecuencia visible en los resultados:** la tendencia Mann-Kendall
calculada por tipo de peligro tiene muchos más casos `datos_insuficientes`
que la vista combinada (p. ej. `scour`: 104 de 178 cantones con datos
insuficientes, frente a solo 5 de 221 en la vista `TODOS`) — es esperable:
un cantón puede tener suficientes eventos de inundación en general para
superar el umbral de 4 años, pero muy pocos eventos específicamente de
socavamiento. No se oculta esta limitación promediando de más; queda
visible en la propia tabla.

### 4.4 ICEN y ONI reportados por separado, no colapsados a un solo índice ancla

La frecuencia de eventos por categoría ENSO (`resumen_enso`) se calcula
independientemente para ICEN (índice costero, fuente ENFEN Perú/Ecuador) y
ONI (índice oceánico, fuente NOAA) — sigue siendo una decisión de diseño
abierta de la Fase 0 (§19.4). Con datos reales ya calculados, las
distribuciones nacionales difieren de forma no trivial (ver §6): ICEN
concentra más eventos en categorías "Débil"/"Moderado" de El Niño (5,308 +
2,517), mientras que ONI marca más eventos como "Neutro" (9,679 vs. 7,622
de ICEN) y captura una categoría "Muy Fuerte" (880 eventos) que ICEN no
distingue en su categorización estándar. Esta discrepancia es justamente la
evidencia empírica que la Fase 0 preveía necesaria antes de fijar un índice
ancla — se deja para la Fase 7 (Índice de Magnitud ENSO), con este
contraste ya cuantificado como insumo.

## 5. Esquema de salida

Ocho tablas, exportadas en Parquet + CSV a `data/processed/`:

| Tabla | Nivel | Filas | Columnas clave |
|---|---|---|---|
| `hist_recurrencia_canton` | cantón | 927 | `n_eventos`, `anios_afectados`, `meses_afectados`, `primer_evento`, `ultimo_evento` |
| `hist_recurrencia_provincia` | provincia | 116 | ídem |
| `hist_impactos_canton` | cantón | 9,270 | `variable_impacto`, `n`, `media`, `mediana`, `maximo`, `desv_std` (formato largo) |
| `hist_impactos_provincia` | provincia | 1,160 | ídem |
| `hist_enso_canton` | cantón | 7,952 | `indice_enso` (ICEN/ONI), `categoria`, `n_eventos` (formato largo) |
| `hist_enso_provincia` | provincia | 1,413 | ídem |
| `hist_tendencia_canton` | cantón | 927 | `tendencia`, `p_valor`, `pendiente_sen`, `anios_con_dato` |
| `hist_tendencia_provincia` | provincia | 116 | ídem |

Todas incluyen `hazard_type` (`flood`/`debris_flow`/`landslide`/`scour`/
`"TODOS"`) como columna de segmentación. El número de filas por nivel no es
un múltiplo exacto de 221 cantones o 24 provincias × 5 categorías de
`hazard_type` porque no todos los cantones/provincias tienen eventos de los
4 tipos de peligro — cada combinación cantón×hazard_type sin eventos
simplemente no genera fila (no se rellena con ceros, a diferencia de la
serie anual usada internamente para Mann-Kendall, que sí se reindexa).

## 6. Resultados — primeras cifras nacionales

Como referencia y control de calidad, no como resultado final del proyecto
(los índices compuestos vienen en Fase 4-8):

- **Top 5 provincias por número de eventos (2015-2025, los 4 peligros
  combinados):** Pichincha (2,718), Guayas (1,738), Loja (1,575), Manabí
  (1,506), El Oro (1,492).
- **Tendencia Mann-Kendall a nivel provincia (`TODOS`):** de 24 provincias,
  9 muestran tendencia `increasing` significativa, 1 `decreasing`, 14 sin
  tendencia (`no trend`) — ninguna con datos insuficientes a nivel
  provincial (agregando los 4 peligros siempre hay ≥4 años con eventos).
- **Tendencia a nivel cantón (`TODOS`):** de 221 cantones, 47 `increasing`,
  6 `decreasing`, 163 `no trend`, 5 `datos_insuficientes`. Los cantones con
  la pendiente de Sen más alta son el Distrito Metropolitano de Quito
  (+28.75 eventos/año, p=0.0063), Cuenca (+9.6, p=0.0127) y Guayaquil
  (+5.44, p=0.043) — consistente con ser los cantones más poblados y con
  mayor exposición reportada, no necesariamente con mayor cronicidad
  relativa (eso lo normaliza la Fase 5, Índice de Recurrencia).
- **Distribución ICEN vs. ONI (los 4 peligros, nacional):** ver §4.4.

## 7. Limitaciones

- Las cifras de esta fase son descriptivas y **no están normalizadas por
  población ni por superficie cantonal** — un cantón grande y poblado
  (Quito, Guayaquil) domina los rankings de conteo bruto casi por
  construcción. La comparación de cronicidad *relativa* entre cantones de
  distinto tamaño es tarea de los índices compuestos (Fase 4-8), no de esta
  fase.
- La tendencia Mann-Kendall a nivel `hazard_type` individual tiene una
  proporción alta de `datos_insuficientes` para `scour` (58%) y
  `debris_flow` (73%) — son los dos peligros con menos eventos totales
  (1,152 y 685 respectivamente), y la Fase 5-8 deberá decidir cómo tratar
  cantones sin tendencia calculable (¿excluir del componente de tendencia
  del HCI, o asumir neutralidad?).
- No se aplicó ningún ajuste por autocorrelación espacial entre cantones
  vecinos en este análisis — cada unidad administrativa se trata como
  independiente. El análisis espacial explícito (Getis-Ord Gi*, Moran's I)
  está planificado para la Fase 9 (Fase 0 §8).
- El p-valor de Mann-Kendall con solo 11 puntos anuales tiene poder
  estadístico limitado — tendencias "no trend" en cantones con pocos
  eventos pueden reflejar falta de poder, no ausencia real de tendencia.
  Documentado, no oculto: por eso se reporta también `anios_con_dato` junto
  al resultado.

## 8. Supuestos

- Los 21,743 eventos completos de la Fase 2 se usan sin excluir ninguno por
  `canton_confidence` (`alta`/`revisar`/`baja_sin_parroquia`) — se asume que
  el `canton_code` reportado por SNGRE es correcto incluso en los 43 casos
  `revisar`, consistente con la resolución de ese pendiente en Fase 2 §4.8
  (ningún patrón de error sistemático encontrado).
- Se asume que un año calendario es la unidad temporal correcta para
  Mann-Kendall (no un año hidrológico ni una ventana ENSO) — es la
  convención más simple e interpretable; se documenta como supuesto, no
  como verdad dada, porque un evento El Niño puede cruzar el límite de dos
  años calendario.

## 9. Ventajas del enfoque

- Ninguna cifra se pierde silenciosamente: la sección 7 del notebook valida
  explícitamente que la suma de eventos por vista `"TODOS"` coincide con el
  total de `hazard_event_geo` (21,743) tanto a nivel cantón como provincia,
  y que todo cantón con eventos tiene una fila de tendencia (aunque sea
  `datos_insuficientes`) — nada se cae del `groupby` sin que una aserción lo
  detenga.
- El bug de agrupación (§4.1-4.2) fue detectado por esas mismas aserciones
  antes de exportar ninguna tabla, no después — validación honesta,
  consistente con la regla del proyecto de no ocultar errores.
- El formato largo de impactos y ENSO permite añadir nuevas variables de
  impacto o categorías ENSO en fases futuras sin cambiar el esquema de la
  tabla exportada.

## 10. Posibles mejoras futuras

- Backfill de `province_name_official`/`canton_name_official` directamente
  en `hazard_event_geo.gpkg` (Fase 2), usando el mismo join por atributo
  aplicado aquí, para que el archivo fuente ya no dependa de que cada fase
  posterior repita la corrección — pendiente de decisión sobre si se
  regenera el artefacto de Fase 2 o se documenta como responsabilidad de
  cada consumidor.
- Evaluar normalización por población/superficie en un análisis descriptivo
  intermedio (antes de los índices compuestos formales de Fase 4-8), para
  que los rankings de esta fase no se lean como "cronicidad" sin advertencia.
- Decidir el tratamiento de cantones con tendencia `datos_insuficientes` por
  tipo de peligro antes de construir el componente de Persistencia (Fase 6).

## 11. Referencias

- Fase 0 — Diseño Conceptual HCI Ecuador, §8 (Fase 3), §19.3, §19.4.
- `docs/methodology/02_spatial_integration.md` (Fase 2, insumo de esta fase;
  §4.4, §4.7, §4.8, §9).
- Hussain, M. & Mahmud, I. (2019). *pyMannKendall: a python package for
  non parametric Mann Kendall family of trend tests.* Journal of Open
  Source Software.
