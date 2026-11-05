# 08 — HCI Compuesto y Análisis de Sensibilidad

**Fase:** 8 de 10 (ver Fase 0, §9, §7)
**Notebook asociado:** `notebooks/Step8_Ecuador_HCI_Composite.ipynb`
**Estado:** implementado y ejecutado — 2026-08-05 (v1.1: re-ejecutado tras corrección de dato en Fase 1 §4.6, 2026-08-06; v1.2: re-ejecutado tras ampliación del criterio ENSO en Fase 5/7, 2026-08-17 — ver nota al final de este documento)
**Audiencia:** científicos, desarrolladores, especialistas DRM/FAO AA

## 1. Objetivo de la fase

Combinar los cuatro índices ya construidos (Severidad — Fase 4,
Recurrencia — Fase 5, Persistencia — Fase 6, Magnitud ENSO — Fase 7) en el
Índice de Cronicidad de Inundaciones por El Niño (HCI):

```
HCI = 0.35·Recurrencia + 0.30·Severidad + 0.20·Persistencia + 0.15·Magnitud ENSO
```

y ejecutar el análisis de sensibilidad que la Fase 0 (§9) exige
explícitamente antes de fijar los pesos, resolviendo en el proceso los
cuatro parámetros pendientes señalados en fases anteriores (Fase 4 §6,
Fase 5 §10, Fase 6 §4.2, Fase 7 §6).

## 2. Fundamento científico

Combinar cuatro dimensiones normalizadas 0-1 en una suma ponderada es el
mismo enfoque usado en los marcos de referencia de Etiopía/Somalia citados
en la Fase 0 (§19.3). El valor añadido de esta fase no es la fórmula en sí
(ya definida en el diseño original) sino **demostrar, con datos, qué tan
sensible es el resultado a las decisiones metodológicas tomadas en el
camino** — exactamente lo que separa un índice publicable de un ejercicio
exploratorio.

## 3. Fundamento estadístico

- **Correlación de rangos de Spearman** (no Pearson) para comparar el
  ranking base contra cada variante de sensibilidad: lo que importa para
  priorización territorial es el *orden* relativo de los cantones, no la
  magnitud exacta del HCI.
- **Conteo de cambios de clase Jenks** como segunda métrica, complementaria
  a Spearman: una correlación alta puede convivir con muchos cambios de
  clase si los valores están muy cerca de un quiebre — se reporta ambas
  para no ocultar ese matiz (ver hallazgo en §6.2).
- **Quiebres naturales (Jenks)**, no cuantiles, para la clasificación final
  — confirmado por Jerson vía AskUserQuestion, dado que la distribución del
  HCI es sesgada (ver §7): Jenks minimiza la varianza dentro de cada clase
  y maximiza la varianza entre clases, en vez de forzar grupos de igual
  tamaño sin relación con la forma real de los datos.

## 4. Decisiones metodológicas y su justificación

### 4.1 Unión de los cuatro índices por atributo, con verificación de consistencia cruzada

Las cuatro tablas (`severity_index_canton`, `recurrence_index_canton`,
`persistence_index_canton`, `enso_magnitude_index_canton`) se unen por
`province_code`/`province_name_official`/`canton_code`/`canton_name_official`/
`hazard_type` — la misma llave que comparten por construcción. Antes de
unir, se verifica que `n_eventos` coincida exactamente entre Severidad y
Persistencia (ambas lo calculan directamente sobre `hazard_event_geo`): de
no coincidir, señalaría un error de unión en alguna fase anterior. Coincidió
exactamente — confirma que las cuatro fases previas construyeron sus
tablas sobre el mismo universo de eventos, sin fugas ni duplicaciones entre
ellas.

### 4.2 Magnitud ENSO: se adopta `enso_magnitude_mean` como insumo oficial

Resuelve el pendiente de Fase 7 §6: se usa `enso_magnitude_mean` (200/221
valores distintos, correlación baja con Severidad) como el insumo oficial
del HCI base, y `enso_magnitude_max` se conserva como variante de
sensibilidad (§6.1) — no se descarta, queda disponible en la tabla final.

### 4.3 Clasificación final: Jenks, no cuantiles

Confirmado por Jerson antes de programar (§3). Se aplica solo sobre la
vista `"TODOS"` de cada nivel — la clasificación por peligro individual no
forma parte del producto principal de esta fase.

## 5. Análisis de sensibilidad — cuatro pruebas, con hallazgos concretos

### 5.1 Magnitud ENSO: `mean` vs. `max` (resuelve Fase 7 §6)

**[Corregido 2026-09-04 — ver nota al final del documento.]** Spearman
ρ=0.9704 (alto), pero **72 de 221 cantones (32.6%) cambian de clase
Jenks**. Confirma la decisión de §4.2 con más fuerza de lo que se había
reportado originalmente: la elección tiene consecuencia práctica para
casi 1 de cada 3 cantones, no 1 de cada 8 — justifica aún más haber
tratado esto como una decisión explícita en vez de una elección
arbitraria.

### 5.2 Pesos alternativos (Fase 0 §9)

**[Corregido 2026-09-04 — ver nota al final del documento.]**

| Escenario | Pesos (Rec/Sev/Per/Mag) | Spearman ρ | Cantones que cambian de clase |
|---|---|---|---|
| Base (oficial) | 0.35/0.30/0.20/0.15 | — | — |
| Equitativo | 0.25/0.25/0.25/0.25 | 0.9854 | **65 (29.4%)** |
| Énfasis Severidad | 0.25/0.45/0.15/0.15 | 0.9907 | 31 (14.0%) |
| Énfasis Recurrencia | 0.55/0.20/0.15/0.10 | 0.9938 | 39 (17.6%) |

**Hallazgo actualizado, invierte lo reportado originalmente:** con los
pesos base recalculados en v1.2 (criterio ENSO ampliado, Fase 5/7 §12),
el escenario "Énfasis Severidad" ahora tiene tanto la correlación de
Spearman más alta **como** el menor número de cambios de clase (14.0%) de
los tres — es el escenario **más robusto**, no el más frágil. El
escenario "Equitativo" es ahora el más frágil en clasificación (29.4%),
pese a tener el Spearman más bajo de los tres. **Implicación práctica
revisada:** ya no hay evidencia de que el peso de Severidad sea el
parámetro que más cuidado requiera frente a los otros tres — si acaso, es
el que menos altera la clasificación final entre los tres escenarios
probados. Esta reversión respecto a la versión anterior del documento no
proviene de un cambio de método (los 3 escenarios y la fórmula de
comparación son idénticos), sino de que los insumos de Recurrencia y
Magnitud ENSO cambiaron de forma ascendente en la actualización v1.2
(denominador de Recurrencia 38→54 meses, techo de escala de Magnitud
ahora alcanza 1.0) — un recordatorio de que las pruebas de sensibilidad
deben re-ejecutarse, no solo el HCI base, cada vez que cambia un insumo
aguas arriba.

### 5.3 Robustez de Severidad a los outliers de Fase 4 §6

**[Corregido 2026-09-04 — ver nota al final del documento.]**

**Nota metodológica importante, descubierta en el proceso:** la primera
prueba de winsorización usó percentil 95, pero varias columnas de impacto
(`affected_indirect`, `houses_destroyed`, `livestock_deaths`) tienen más
del 95% de sus eventos en 0 — su percentil 95 es literalmente 0.
Winsorizar ahí no recorta un valor extremo, aplasta casi toda la señal de
esa columna a 0: produjo un artefacto de empate masivo, 117 de 221
cantones (53%) exactamente en 0.75, que medía un umbral mal elegido, no
sensibilidad real a outliers. Se corrigió usando percentil 99 (verificado
antes: preserva señal real en las 5 columnas, sin percentiles en cero).

**Con percentil 99 (post-corrección):** Spearman ρ=0.8716 (la correlación
**más baja** de las cinco pruebas — la de mayor sensibilidad real) y
**131 de 221 cantones (59.3%) cambian de clase** — más de la mitad del
país. Casos concretos (estos sí se mantienen idénticos a la versión
anterior del documento: los valores de `severity_index`/`severity_index_robusto`
no dependen del criterio ENSO que cambió en v1.2, solo el `hci`/`hci_sev_robusta`
que los combina con Recurrencia/Persistencia/Magnitud):

| Cantón | Severidad original | Severidad robusta (p99) |
|---|---|---|
| Chone | 0.530 | 1.000 |
| Distrito Metropolitano de Quito | 0.365 | 0.600 |
| Baños de Agua Santa | 0.026 | 0.802 |

**Interpretación, no intuitiva a primera vista:** los tres valores
*suben* con la winsorización, no bajan. Esto es un efecto matemático
esperado del min-max: al recortar los valores más extremos (que antes
definían el techo nacional), el techo baja — y como todos los demás
cantones se miden contra ese techo, sus valores normalizados suben en
general. La winsorización no solo afecta a los cantones "dueños" de los
valores extremos: cambia el punto de comparación para **todos** los
cantones del país. Esto confirma que el riesgo señalado en Fase 4 §6 era
real y de magnitud considerable — **más de la mitad** de los cantones del
país (59.3%, actualizado desde el 48.9% reportado originalmente) cambiarían
de categoría de cronicidad según cómo se traten los valores extremos de
Severidad, incluso después de haber corregido el dato erróneo de Baños
(§4.6 de Fase 1). Es decir: la fragilidad de esta prueba **no provenía
únicamente** del error de captura de Baños — la winsorización sigue
siendo, por sí sola, la decisión metodológica más consecuente de todo el
HCI, con o sin ese error, y sigue siendo la prueba más sensible de las
cinco tras la actualización v1.2. La corrección de Baños resolvió si su
valor concreto era confiable (no lo era), pero no elimina la sensibilidad
estructural del índice a valores extremos legítimos como el de Quito.

### 5.4 Resumen consolidado

Exportado en `data/processed/hci_sensitivity_summary.csv` — las cinco
pruebas, con Spearman ρ y % de cambio de clase, en una sola tabla para
referencia rápida. Es la fuente autoritativa (salida directa del
notebook); si alguna vez este documento vuelve a divergir de ese CSV,
el CSV manda — ver nota de corrección al final de este documento.

## 6. Esquema de salida

- `hci_composite_canton.{parquet,csv}` (835 filas): las columnas de los 4
  índices insumo, `hci` (base), `clase_hci` (Jenks, solo vista `"TODOS"`),
  más las 5 variantes de sensibilidad (`hci_mag_max`,
  `hci_pesos_equitativo`, `hci_pesos_enfasis_severidad`,
  `hci_pesos_enfasis_recurrencia`, `hci_sev_robusta`) y sus clases Jenks
  correspondientes.
- `hci_composite_provincia.{parquet,csv}` (113 filas): mismo esquema,
  nivel provincia (solo HCI base + clase, sin las variantes de
  sensibilidad — esas se probaron únicamente a nivel cantón).
- `hci_sensitivity_summary.csv`: tabla resumen de las 4 pruebas.

## 7. Resultados — ranking nacional (HCI base, vista `"TODOS"`, post-corrección Baños 2026-08-06)

**Distribución de clases (cantón, Jenks):** Muy Baja 25, Baja 59, Moderada
85, Alta 37, Muy Alta 15 — de 221. Distribución no uniforme (a diferencia
de un cuantil, que forzaría ~44 en cada una), concentrada en "Moderada".
Un cantón se movió de "Baja" a "Moderada" respecto a la versión
pre-corrección — efecto indirecto de la corrección de Baños sobre el techo
nacional de la pillar de Ganadería, que recalcula la normalización
min-max de esa categoría para todos los cantones, no solo para Baños.

**Top 5 cantones:** Distrito Metropolitano de Quito (0.604), Ambato
(0.514), Chone (0.463), Esmeraldas (0.416), Morona (0.404). Baños de Agua
Santa —que antes de la corrección ocupaba el 4º lugar (0.437)— pasó al
**8º lugar (0.396)**, cediendo su puesto a cantones cuyo HCI no dependía
del dato corregido.

**Top 3 provincias:** Tungurahua (0.625), Manabí (0.573), Pichincha
(0.559) — sin cambios respecto a la versión pre-corrección: a nivel
provincia el error de captura de Baños queda diluido dentro del agregado
de Tungurahua y no altera el ranking.

**Hallazgo de valor diagnóstico — el HCI muestra perfiles muy distintos
entre cantones con puntaje similar:**
- **Quito** llega al primer lugar impulsado por Persistencia (1.0, el
  máximo posible) y Recurrencia (0.79) — su Severidad (0.365) es apenas
  moderada.
- **Ambato** (2º lugar) tiene una Severidad **casi nula** (0.007) pero
  Recurrencia (0.89) y Persistencia (0.91) extremadamente altas — es
  crónico en frecuencia y persistencia, no en magnitud de impacto por
  evento.
- **Chone** (3er lugar) es el patrón inverso: Severidad muy alta (0.530,
  la más alta de las tres) pero Recurrencia (0.605) y Persistencia (0.261)
  más moderadas.
- **Baños de Agua Santa** (8º lugar tras la corrección) sigue en "Muy
  Alta" cronicidad — su HCI ya no depende de un valor de Severidad
  inflado (0.026, prácticamente nula) sino de Recurrencia (0.763) y
  Persistencia (0.435) altas, un perfil ahora consistente con el resto de
  cantones de Tungurahua (Ambato, San Pedro de Pelileo) y sin depender de
  ningún dato cuestionado.

Esto no es un defecto del HCI — es precisamente el valor de un índice
compuesto de 4 dimensiones: cantones que serían indistinguibles con un
solo criterio (p. ej. solo conteo de eventos) resultan tener perfiles de
riesgo operacionalmente distintos, información directamente útil para
decidir qué tipo de intervención de Acción Anticipatoria prioriza cada
territorio.

## 8. Limitaciones

- El HCI base usa `enso_magnitude_mean`, que no ha sido validado
  externamente (Fase 7 §7) — es una mejora estadística demostrada, no una
  validación de que sea la interpretación operacionalmente correcta.
- La sensibilidad a los outliers de Severidad (§5.3, ρ=0.8716, 59.3% de
  cambios de clase) sigue siendo la más alta de las cinco pruebas —
  incluso tras verificar y corregir el evento de Baños (Fase 1 §4.6), el
  HCI base sigue siendo sensible a valores extremos legítimos como el de
  Quito. Esta es una propiedad estructural del método (min-max sobre una
  distribución con cola larga), no un problema de calidad de dato
  pendiente de resolver.
- El escenario "Equitativo" (§5.2) muestra que la clasificación final
  puede ser más frágil de lo que sugiere la correlación de Spearman — un
  hallazgo que aplica en general a cualquier clasificación por quiebres
  cerca de zonas densas de la distribución, no solo a este escenario
  específico. (Corregido 2026-09-04: la versión anterior de este documento
  atribuía esta fragilidad al escenario "Énfasis Severidad" — ver nota al
  final del documento.)
- Solo se probaron 3 escenarios de pesos puntuales (§5.2) y 2 variantes de
  normalización (mean/max en Magnitud, min-max/winsorizado en Severidad) —
  no un barrido continuo del espacio de pesos. La reversión del hallazgo
  de §5.2 entre v1.1 y v1.2 es evidencia directa de que 3 puntos discretos
  no caracterizan de forma estable el espacio completo; un método de
  sensibilidad global (Monte Carlo/Sobol) daría una caracterización menos
  dependiente de qué 3 escenarios se eligieron a mano — ver Fase 13.
- No se validó el HCI contra fuentes externas (UNOSAT, EM-DAT,
  DesInventar, Copernicus EMS — Fase 0 §12) — pendiente para una fase
  futura.
- No se realizó una búsqueda exhaustiva de todas las combinaciones
  posibles de pesos (grid search) — se probaron 3 escenarios
  representativos, no un barrido sistemático del espacio de parámetros.

## 9. Supuestos

- Se asume que las cuatro dimensiones (Severidad, Recurrencia,
  Persistencia, Magnitud ENSO) son conceptualmente independientes y
  aditivas — no se probó una estructura de interacción (p. ej. Severidad ×
  Magnitud) que podría ser más realista pero que Fase 0 no especificó.
- Se asume que la escala 0-1 de las cuatro dimensiones es comparable entre
  sí pese a haberse construido con métodos de normalización distintos
  (min-max en Severidad/Persistencia, tasa de meses en Recurrencia, escala
  ordinal ENFEN en Magnitud) — es una limitación conocida de combinar
  índices normalizados por métodos distintos, no resuelta en esta fase.

## 10. Ventajas del enfoque

- Las cinco pruebas de sensibilidad no fueron una formalidad: cada una
  encontró algo específico y accionable (Magnitud: 32.6% de cambio real;
  Pesos: el escenario más frágil en clasificación depende de los insumos
  vigentes, y cambió entre v1.1 y v1.2 — ver nota de corrección al final;
  Outliers: la prueba más sensible de las cinco, con causa raíz
  identificada — no solo un número).
- El error de winsorización al percentil 95 (§5.3) se detectó y corrigió
  dentro de la misma fase, con la causa raíz documentada (columnas con
  percentil 95 = 0) — no llegó a la tabla final como un artefacto sin
  explicar.
- La tabla de salida conserva **todas** las variantes de sensibilidad, no
  solo el HCI base — cualquier decisión futura de ajustar pesos o método
  puede compararse directamente contra lo ya calculado, sin re-ejecutar
  todo el pipeline.

## 11. Posibles mejoras futuras

- Considerar métodos de normalización menos sensibles a la cola larga de
  la distribución (p. ej. normalización robusta basada en percentiles en
  vez de min-max puro) para las columnas de impacto que muestran la mayor
  sensibilidad estructural (§5.3, §8).
- Considerar una estructura de interacción entre dimensiones si el
  análisis con expertos DRM/COE sugiere que la relación no es puramente
  aditiva.
- Validación externa (Fase 0 §12) antes de considerar el HCI apto para
  uso operacional en decisiones de Acción Anticipatoria.
- Barrido sistemático (grid search) de pesos, no solo 3 escenarios
  representativos, si se requiere una caracterización más completa de la
  sensibilidad.

## 12. Referencias

- Fase 0 — Diseño Conceptual HCI Ecuador, §7 (clasificación), §9 (fórmula
  HCI y pedido explícito de análisis de sensibilidad), §12 (validación
  externa), §19.3.
- `docs/methodology/04_severity_index.md` §6 (outliers), `05_recurrence_index.md`
  §4.3 (evento ENSO), `06_persistence_index.md` §4.2 (pesos de
  componentes), `07_enso_magnitude_index.md` §6 (max vs. mean) — los cuatro
  pendientes resueltos en esta fase.

## 12. Actualización 2026-08-17 (v1.2) — Reejecutado tras criterio ENSO ampliado

Sin cambios de código en esta fase. Se reejecutó el notebook para heredar
los insumos actualizados de Fase 5 (`recurrence_index_*`, denominador 54 en
vez de 38 meses ENSO) y Fase 7 (`enso_magnitude_*`, techo de escala ahora
alcanza 1.0) — ver `05_recurrence_index.md` §12 y `07_enso_magnitude_index.md`
§12 para el detalle del cambio ascendente.

Validación de cobertura y rango tras reejecutar: 221 cantones, 24
provincias, HCI en [0,1] — OK, sin regresiones.

Ranking recalculado (`hci`, vista `TODOS`, pesos base): **Distrito
Metropolitano de Quito** (0.637, "Muy Alta"), **Ambato** (0.537),
**Chone** (0.469), Esmeraldas (0.441), Morona (0.415), Loja (0.411), Baños
de Agua Santa (0.404), Santo Domingo (0.401) — el mismo orden de los tres
primeros puestos que ya reportaba la v1.1 (2026-08-06), no se guardó el
valor numérico exacto de esa versión para una comparación estricta punto
por punto, así que no se afirma aquí si los valores subieron/bajaron, solo
que el orden del top 3 se mantiene estable frente al cambio de criterio
ENSO. Lo que sí cambió de forma verificable es el insumo de Recurrencia
(Fase 5 §12): Quito no aparecía en el top 5 de Recurrencia por sí sola bajo
el criterio ICEN-solo, y ahora sí — consistente con que Quito ya llegaba a
la cima del HCI compuesto principalmente por Persistencia y Severidad, no
por Recurrencia (ver hallazgo ya documentado en `docs/executive/08_hci_composite.md`).
No se reabrió el análisis de sensibilidad de pesos (§7-§9) — las variantes
de pesos ya evaluadas siguen siendo válidas como estructura, solo cambian
los valores de entrada.

## 13. Corrección 2026-09-04 — la prosa de §5 no se había actualizado tras el re-ejecute v1.2

**Hallazgo:** al preparar la Fase 13 (validación de sensibilidad extendida,
ver `docs/methodology/13_sensitivity_validation.md`), se detectó que el
notebook completo sí se re-ejecutó de punta a punta el 2026-08-17 (mismo
timestamp en `hci_sensitivity_summary.csv` y en este documento), pero la
nota de la sección anterior ("no se reabrió el análisis de sensibilidad de
pesos") se interpretó — incorrectamente — como que tampoco había que
actualizar la prosa de §5.1-§5.3, que seguía describiendo los números de la
corrida v1.1 (pre-ampliación del criterio ENSO en Fase 5/7). Los números
sí cambiaron, porque Recurrencia, Persistencia y Magnitud ENSO son insumos
directos del HCI que compara cada prueba de sensibilidad.

**Verificación:** los valores corregidos en §5.1-§5.3 se recalcularon de
forma independiente directamente desde `hci_composite_canton.csv` (columnas
`hci_mag_max`, `hci_pesos_*`, `hci_sev_robusta` y sus clases Jenks
correspondientes) — coinciden exactamente con `hci_sensitivity_summary.csv`
y con la salida guardada del propio notebook (celda de `casos[[...]]`,
2026-08-17). Los valores de `severity_index`/`severity_index_robusto` en la
tabla de §5.3 (Chone, Quito, Baños) no cambiaron, porque Severidad no
depende del criterio ENSO — se verificaron igual, y coinciden con la
versión anterior del documento.

**Consecuencia editorial más importante:** el "hallazgo no obvio" de §5.2
—que el escenario "Énfasis Severidad" era el más frágil en clasificación
pese a tener el Spearman más alto— **ya no es cierto** con los insumos
vigentes. Con los datos actuales, "Equitativo" es el escenario más frágil
y "Énfasis Severidad" es el más robusto de los tres. El patrón cualitativo
general (Spearman alto ≠ clasificación estable) sigue siendo válido como
lección metodológica, pero el ejemplo concreto que lo ilustraba cambió de
escenario.

**Lección para el proceso, no solo para este documento:** cuando un
notebook se re-ejecuta completo por un cambio de insumo aguas arriba, toda
prosa que cite un número debe tratarse como potencialmente obsoleta hasta
verificarse contra la salida más reciente — no solo el resultado principal
de la fase (HCI base, §12 anterior), también los resultados secundarios
(pruebas de sensibilidad, tablas de casos). Este es exactamente el tipo de
riesgo que la Fase 13 busca reducir de forma sistemática.
