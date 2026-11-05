# 07 — Índice de Magnitud ENSO

**Fase:** 7 de 10 (ver Fase 0, §9)
**Notebook asociado:** `notebooks/Step7_Ecuador_ENSO_Magnitude_Index.ipynb`
**Estado:** implementado y ejecutado — 2026-08-05; **magnitud combinada ICEN+ONI el 2026-08-17** (ver §12)
**Audiencia:** científicos, desarrolladores, especialistas en climatología/ENSO

## 1. Objetivo de la fase

Construir el cuarto y último insumo del EFCI compuesto (Fase 0 §9):
traducir las categorías ICEN (Débil/Moderado/Fuerte/Extraordinario) en
valores normalizados 0-1, específicos por cantón y provincia, usando ICEN
como índice ancla (confirmado en Fase 5 §4.2).

## 2. Decisión metodológica confirmada antes de programar (y revisada el mismo día)

### 2.1 El problema: ICEN es nacional/mensual, los demás índices son cantonales

ICEN produce un solo valor por mes para todo Ecuador — no varía por
cantón. Severidad, Recurrencia y Persistencia (Fases 4-6) sí varían por
cantón. Para que los cuatro sean combinables en el EFCI (Fase 8), había que
decidir una regla de agregación que convierta la magnitud ENSO nacional en
un valor específico por unidad administrativa.

**Ronda 1 — alternativas presentadas a Jerson (AskUserQuestion) y su
elección inicial:**
- **Máximo entre los meses afectados (elegida primero):** la magnitud ENSO
  más alta entre todos los meses en que el cantón tuvo al menos un evento
  — responde "¿al El Niño más fuerte que ha enfrentado este cantón?".
  Consistente con el enfoque de peor escenario ya usado en Severidad (Fase
  4, máximo histórico) y Persistencia (Fase 6, racha máxima).
- Media entre los meses afectados — descartada en la ronda 1: más estable,
  pero se pensó que no distinguiría un cantón golpeado una vez por un
  episodio Extraordinario de uno golpeado repetidamente solo por episodios
  Débiles.
- Magnitud del mes del evento más severo — descartada por mayor
  complejidad de implementación sin beneficio claro sobre el máximo.

**Ronda 2 — revisión el mismo día, tras ver el resultado real:** el máximo
resultó con muy bajo poder de discriminación (§6.1 más abajo — las 24
provincias empataban en 0.75). Jerson pidió pensar juntos el problema; se
probaron 3 alternativas con datos reales (no solo en teoría) antes de
decidir:

| Alternativa | Valores distintos (cantón, n=221) | Correlación con `severity_index` |
|---|---|---|
| Máximo, categoría ordinal (ronda 1) | 4 | — |
| **Promedio, categoría ordinal** | **200** | **0.135 (baja — señal propia)** |
| Máximo, ICEN continuo (no ordinal) | ~165 (56 seguían empatados en el techo) | 0.262 |
| Promedio ponderado por severidad del evento, ICEN continuo | ~221 (dispersión completa) | 0.148 |

**Decisión final:** calcular **ambas** — `enso_magnitude_max` y
`enso_magnitude_mean` — como columnas separadas, sin descartar ninguna
todavía. La elección de cuál usar (o si combinarlas) en el EFCI compuesto
queda para el análisis de sensibilidad de la Fase 8, junto con los demás
parámetros ya señalados en fases anteriores. Se prefirió el promedio sobre
las variantes con ICEN continuo porque Fase 0 pide explícitamente traducir
*categorías* (Débil/Moderado/Fuerte/Muy Fuerte), no el valor numérico
continuo — el promedio ordinal es la alternativa que mejor resuelve el
problema de discriminación sin apartarse de esa instrucción.

## 3. Fundamento científico

Las categorías ICEN usadas (Neutro, La Niña Débil/Moderada/Fuerte, El Niño
Débil/Moderado/Fuerte/Extraordinario) son las oficiales de ENFEN, ya
documentadas en el workbook maestro (`Notas Metodológicas`) y ya aplicadas
desde la Fase 1 para clasificar cada mes (`icen_category`). No se inventa
un esquema de clasificación nuevo.

## 4. Decisiones metodológicas y su justificación

### 4.1 Traducción ordinal fija, no min-max sobre el valor continuo de ICEN

Neutro y La Niña (cualquier magnitud) → **0**; El Niño Débil → 0.25;
Moderado → 0.50; Fuerte → 0.75; Extraordinario → 1.00.

**Por qué ordinal y no min-max:** Fase 0 pide explícitamente traducir las
*categorías* (Débil/Moderado/Fuerte/Muy Fuerte), no el valor numérico
continuo de ICEN — y esas categorías ya tienen un orden oficial publicado
por ENFEN, con significado operacional propio (activación de protocolos
COE por nivel). Usar min-max sobre el ICEN numérico habría introducido una
escala arbitraria sin ese respaldo institucional.

**Por qué Neutro y La Niña valen 0, no un valor negativo o distinto de
cero:** el proyecto mide inundaciones asociadas específicamente a El Niño
— misma decisión de alcance que la definición de "evento ENSO" de la Fase
5 (§4.3). Un mes La Niña no es "menos El Niño", es *no* El Niño; 0 es la
codificación coherente con esa decisión de alcance ya tomada.

### 4.2 Dos agregaciones calculadas, ninguna descartada — ver §6

Implementado como se describe en §2.1: `enso_magnitude_max` y
`enso_magnitude_mean` para cada unidad administrativa y vista. Un cantón
sin ningún evento en un mes El Niño obtiene 0 en ambas — coherente con la
codificación de §4.1, no es una ausencia de dato sino el valor correcto.

### 4.3 Cobertura completa garantizada

Mismo principio que Fases 5 (§4.6) y 6 (§3): toda unidad administrativa con
eventos históricos aparece en la vista `"TODOS"`, incluso si su índice es 0
— se verificó explícitamente (221/221 cantones, 24/24 provincias) antes de
exportar.

## 5. Esquema de salida

Dos tablas en `data/processed/` (Parquet + CSV):

- `enso_magnitude_index_canton` (1,105 filas: 221 cantones × 5 vistas).
- `enso_magnitude_index_provincia` (120 filas: 24 provincias × 5 vistas).

Columnas: `province_code`, `province_name_official`,
`canton_code`/`canton_name_official` (solo cantón), `hazard_type`,
`n_eventos`, `enso_magnitude_max` (0-1), `enso_magnitude_mean` (0-1).

## 6. Resultado principal y hallazgo metodológico importante — poder de discriminación

**Ningún mes de la ventana 2015-2025 alcanzó la categoría "El Niño -
Extraordinario"** (ICEN > 3.5) — el máximo observado es "El Niño - Fuerte"
(12 de 132 meses). No es un error: ENFEN asocia la categoría Extraordinaria
a episodios históricamente raros (1982-83, 1997-98), anteriores a la
ventana del proyecto. Consecuencia directa: **ningún cantón puede alcanzar
1.0 en ninguna de las dos agregaciones** con los datos actuales — el techo
real observado es 0.75.

### 6.1 `enso_magnitude_max`: poder de discriminación muy bajo (hallazgo original)

Con la agregación por máximo, el índice tiene **poder de discriminación
muy bajo** entre unidades administrativas:

- A nivel **provincia**: las **24 de 24 provincias** alcanzan exactamente
  0.75 — el índice no distingue absolutamente nada entre provincias. Esto
  ocurre porque los 12 meses "El Niño Fuerte" tuvieron impacto
  suficientemente extendido a nivel nacional como para que toda provincia
  registrara al menos un evento en alguno de esos 12 meses.
- A nivel **cantón**: 196 de 221 cantones (89%) también alcanzan el techo
  de 0.75; solo 24 quedan por debajo (18 en 0.50, 6 en 0.25), y 1 solo
  cantón (San Fernando, Azuay — el mismo caso de un único evento aislado ya
  visto en Fase 5 §4.6) queda en 0. En total, solo **4 valores distintos**
  existen en toda la tabla de 221 cantones.

### 6.2 `enso_magnitude_mean`: discriminación restaurada

Con la agregación por promedio: **200 de 221 valores distintos**, media
0.19, mediana 0.18, máximo observado 0.47 (Pedro Vicente Maldonado,
Pichincha — un cantón con pocos eventos, 9, pero todos concentrados en
meses de magnitud ENSO relativamente alta). Correlación con
`severity_index` de solo 0.135 — confirma que es una señal genuinamente
distinta de la Severidad, no una redundancia. El top 10 de este ranking
(Pedro Vicente Maldonado, Zapotillo, Santa Cruz/Galápagos, 24 de Mayo,
Colimes...) no coincide con el top 10 de Severidad (Fase 4) ni de
Recurrencia (Fase 5) — son cantones con relativamente pocos eventos
totales, pero cuyos eventos, en promedio, coincidieron con meses de El
Niño más intenso que el promedio nacional.

### 6.3 Consecuencia para el EFCI compuesto (Fase 8)

Con `enso_magnitude_max`, el término de Magnitud ENSO (peso 0.15 en la
fórmula de Fase 0 §9) contribuiría casi el mismo valor constante (0.15 ×
0.75 ≈ 0.1125) a prácticamente todas las provincias y a la gran mayoría de
cantones — en la práctica, no diferenciaría entre unidades administrativas,
que es justamente lo que un índice de "cronicidad" comparativa necesita
hacer. `enso_magnitude_mean` no tiene ese problema. Ninguna de las dos
columnas se descartó unilateralmente — quedan ambas disponibles, y la
elección final (o una combinación de ambas) se decide en el análisis de
sensibilidad de la Fase 8.

## 7. Limitaciones

> **Actualización 2026-10-06 (Fase 15):** se contrastó la magnitud ENSO contra la tasa de eventos (dosis-respuesta, ajustada por estacionalidad). No hay gradiente monótono a escala nacional (pendiente por categoría IRR 0.95, p = 0.53); solo la Costa lo muestra (IRR 1.67 por categoría, p < 0.001). Esto limita la justificación empírica del peso de 15 % de este componente fuera de la Costa. Ver `15_enso_hazard_association.md` §5.2 y §6.

- `enso_magnitude_max` tiene poder de discriminación muy bajo — ver §6.1.
  Se mantiene exportado (no se eliminó) porque sigue siendo la respuesta
  correcta a una pregunta operacionalmente válida ("¿ha enfrentado este
  cantón el El Niño más fuerte disponible?"), aunque no sirva bien como
  insumo discriminante del EFCI compuesto.
- `enso_magnitude_mean` no se ha contrastado todavía contra una validación
  externa (p. ej. si los cantones con promedio alto realmente coinciden con
  percepción de expertos DRM/COE de mayor vulnerabilidad a El Niño) — es
  una mejora estadística demostrada contra el problema de discriminación,
  no una validación de que sea la interpretación "correcta".
- El techo real (0.75, no 1.0) no se ajustó ni se re-normalizó al rango
  observado — se mantiene la escala ordinal absoluta de ENFEN (0-1 con
  significado institucional) en vez de estirarla artificialmente para que
  el máximo observado sea 1.0, lo cual habría exagerado la magnitud
  relativa de los episodios "Fuerte" ya vividos en esta ventana.
- No se filtró por `canton_confidence` (Fase 2 §4.7), igual que en las
  fases anteriores.

## 8. Supuestos

- Se asume que las categorías oficiales ENFEN (con sus umbrales numéricos
  de ICEN) siguen siendo la clasificación correcta para todo el período
  2015-2025 — no se verificó si ENFEN ha revisado esos umbrales a lo largo
  del tiempo.

## 9. Ventajas del enfoque

- Traducción directamente trazable a una fuente oficial (ENFEN), sin
  inventar una escala propia.
- El hallazgo de bajo poder de discriminación de `enso_magnitude_max` (§6)
  se identificó, se investigó con 3 alternativas probadas empíricamente
  (no solo en teoría) y se resolvió con una segunda columna, todo dentro de
  esta misma fase — evita que un defecto de diseño se descubra recién al
  ensamblar el EFCI compuesto, cuando sería más costoso de diagnosticar.
- Calcular ambas agregaciones sin forzar una decisión prematura mantiene la
  Fase 8 libre de reabrir esta fase si el análisis de sensibilidad prefiere
  una, la otra, o una combinación de las dos.

## 10. Posibles mejoras futuras

- Decidir en la Fase 8, con el análisis de sensibilidad completo de los 4
  índices, si el EFCI usa `enso_magnitude_max`, `enso_magnitude_mean`, o
  una combinación (p. ej. promedio de ambas, o `mean` con `max` como
  desempate).
- Evaluar si el peso de 0.15 asignado a Magnitud ENSO en la fórmula
  original (Fase 0 §9) debería revisarse si ninguna de las dos
  agregaciones resulta suficientemente informativa tras la validación de
  Fase 8.
- Si se incorporan años adicionales en el futuro (ventana extendida más
  allá de 2025) que sí incluyan un episodio Extraordinario, revisar si el
  poder de discriminación de `enso_magnitude_max` mejora naturalmente.
- Validar `enso_magnitude_mean` contra criterio experto DRM/COE (ver §7).

## 11. Referencias

- Fase 0 — Diseño Conceptual EFCI Ecuador, §9 (Magnitud ENSO).
- `docs/methodology/05_recurrence_index.md` §4.2-4.3 (ICEN como índice
  ancla, definición de alcance El Niño) y §12 (criterio ampliado).
- Notas Metodológicas (workbook maestro) — categorías y umbrales oficiales
  ICEN/ENFEN.

## 12. Actualización 2026-08-17 — Magnitud combinada ICEN+ONI, techo 1.0 alcanzado

Consecuencia directa de la ampliación del criterio ENSO en Fase 5 (§12 de
`docs/methodology/05_recurrence_index.md`): la Fase 5 ahora exporta
`magnitud_enso_combinada = max(valor_ordinal_ICEN, valor_ordinal_ONI)` por
mes, en vez de dejar que cada fase derive su propia magnitud solo de
`icen_category`. Fase 7 se editó para **consumir directamente esa
columna** (`enso_monthly["magnitud_enso"] = enso_monthly["magnitud_enso_combinada"]`)
en lugar de recalcularla con `CATEGORY_VALUES.map(icen_category)`.

**Motivo:** ONI sí registró meses "El Niño - Muy Fuerte" (8 meses, todos
dentro del episodio 2015-2016) que la escala ICEN, calibrada a la costa
peruano-ecuatoriana, no etiquetó como "Extraordinaria". El §6 original de
este documento documentaba que "ningún cantón puede alcanzar 1.0 con los
datos actuales" — **esa afirmación ya no es correcta** con el criterio
ampliado, y se corrigió en el código y en esta documentación en vez de
dejarla como una nota histórica engañosa.

**Config añadido:** `enso_magnitude_index.category_values` ahora incluye
`"El Niño - Muy Fuerte": 1.00` (categoría exclusiva de ONI, ICEN no la
usa) — necesario porque el `max()` combinado debe poder resolver ambas
escalas de categorías a un valor ordinal común.

**Resultado tras recalcular (vista `TODOS`, 221 cantones):**

- `enso_magnitude_max`: 160/221 cantones (72%) ahora alcanzan el techo 1.0
  (antes: 0 cantones, techo real era 0.75) — el episodio 2015-2016 (el más
  fuerte de la ventana del proyecto, uno de los tres más intensos
  registrados globalmente desde 1950) ahora se refleja correctamente en la
  escala.
- `enso_magnitude_mean`: distribución poco cambiada en términos relativos
  (media 0.284, máximo 0.646 en Santa Cruz, Galápagos) — sigue siendo la
  agregación con mejor poder de discriminación entre cantones (§6 de este
  documento sigue vigente en ese punto).
- El assert de validación `enso_magnitude_max <= 0.75` (Sección 4 del
  notebook) se actualizó a `<= 1.0` — dejar el assert viejo habría hecho
  fallar la ejecución con el nuevo criterio, que es el comportamiento
  correcto esperado, no un error a silenciar.

Fase 8 (EFCI compuesto) se reejecutó sin cambios de código, heredando este
nuevo insumo — validación de cobertura y rango [0,1] confirmada para 221
cantones y 24 provincias.
