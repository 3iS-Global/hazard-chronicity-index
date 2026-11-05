# 05 — Región Niño 1+2, cierre de Fase 0 §19.4, e Índice de Recurrencia

**Fase:** 5 de 10 (ver Fase 0, §9)
**Notebook asociado:** `notebooks/Step5_Ecuador_Recurrence_Index.ipynb`
**Estado:** implementado y ejecutado — 2026-08-05; **criterio ENSO ampliado el 2026-08-17** (ver §12)
**Audiencia:** científicos, desarrolladores, especialistas en climatología/ENSO

## 12. Actualización 2026-08-17 — Criterio ENSO ampliado (unión ICEN+ONI)

Jerson pidió explícitamente dejar de restringir el proyecto a la región
Niño 1+2 (ICEN): "ya no debo enfocarme solo en enso 1 y 2, debo usar también
3 y 4 donde también hubo eventos que se relacionan". Esta sección documenta
qué cambió, con qué evidencia, y por qué el resto de §1-§11 (correlaciones,
fundamento del índice ancla, bug de cobertura) sigue vigente como contexto
histórico aunque la definición operacional de "evento ENSO" haya cambiado.

**Decisión tomada (confirmada por Jerson vía pregunta estructurada):**
en vez de calcular Niño 3 y Niño 4 como índices independientes, se amplió
el criterio de "evento ENSO" a la **unión** de ICEN y ONI — ONI es el índice
estándar NOAA/CPC construido sobre la región Niño 3.4, que cubre el Pacífico
central que Niño 3 y Niño 4 flanquean. Motivos:

1. **Redundancia estadística verificada, no asumida.** Correlación de
   Pearson de las *anomalías* (no la SST cruda, que comparte ciclo
   estacional e infla la correlación) 2015-2025: Niño3-Niño3.4(ONI)=0.968,
   Niño4-Niño3.4(ONI)=0.918. Ambas regiones están, en la práctica, ya
   representadas por ONI — calcularlas aparte no habría agregado señal
   nueva, solo complejidad.
2. **El workbook maestro ya anticipaba esta distinción.** La hoja `2015
   2025 (mes)` de `Indices ENSO (1).xlsx` trae una columna `Niño + Niño
   Costero` con valores "Ambos" — el mismo concepto de unión con
   trazabilidad que se implementó aquí, ya usado informalmente por el
   equipo antes de este proyecto.
3. **El desacuerdo ICEN-ONI es señal real, no ruido.** De 132 meses
   2015-2025, ICEN y ONI coinciden en 81.1% (107/132). En los 25 meses de
   desacuerdo se probó si esos meses "solo ONI" o "solo ICEN" también
   tienen tasas de eventos elevadas — si fuera ruido, esos meses deberían
   parecerse al baseline no-ENSO. No fue así: meses "solo ICEN" promedian
   441.7 eventos/mes, meses "solo ONI" 251.8 eventos/mes, ambos muy por
   encima del baseline no-ENSO (129.1 eventos/mes) — es decir, usar solo
   ICEN (como en la versión anterior de esta fase) excluía meses que
   *sí* tenían señal de impacto elevada.

**Implementación — "unión con trazabilidad":**

```python
es_evento_enso_icen_solo = icen_category.str.startswith("El Niño")
es_evento_enso_oni_solo  = oni_category.str.startswith("El Niño")
es_evento_enso = es_evento_enso_icen_solo | es_evento_enso_oni_solo

tipo_enso = "Ambos" si ambos | "Niño Costero" si solo ICEN | "Niño" si solo ONI | "No ENSO"

magnitud_enso_combinada = max(valor_ordinal(icen_category), valor_ordinal(oni_category))
```

La columna `tipo_enso` preserva cuál índice disparó la clasificación —
ninguna fusión ciega. `magnitud_enso_combinada` alimenta directamente la
Fase 7 (ver `docs/methodology/07_enso_magnitude_index.md` §7).

**Resultado:** 54 de 132 meses califican como "evento ENSO" bajo el
criterio ampliado (antes: 38, solo ICEN). Desglose por `tipo_enso`: No
ENSO=78, Ambos=29, Niño (solo ONI)=16, Niño Costero (solo ICEN)=9. Los 38
meses ICEN-solo originales quedan preservados íntegros en la nueva columna
`es_evento_enso_icen_solo` — no se pierde la serie original, se amplía.

**Niño 3 y Niño 4 NO se calculan como índices independientes** — decisión
explícita, justificada por la redundancia del punto 1. Si en el futuro se
necesita distinguir un evento con fuerte señal en el Pacífico central-oeste
puro (Niño 4) de uno más cercano a Niño 3.4, esa sería la señal a revisar
primero, pero no hay evidencia en 2015-2025 de que ese caso se haya dado.

**Recurrencia recalculada con el nuevo denominador (54, no 38):**

- Top cantones (vista `TODOS`): Ambato (0.926, 50/54 meses ENSO con
  evento — antes 0.89/38), Distrito Metropolitano de Quito (0.852, antes no
  aparecía en el top 5), Morona (0.833), Baños de Agua Santa (0.759), Loja
  (0.759).
- Top provincias: Morona Santiago y Tungurahua empatadas en el máximo
  (1.0, evento en 54/54 meses ENSO), Napo y Chimborazo (0.981).
- Distribución cantonal: media 0.323, mediana 0.296, máximo 0.926 — el
  ranking relativo entre cantones es, en términos generales, consistente
  con la versión anterior (los mismos cantones de la sierra centro-sur
  siguen dominando), pero Quito sube notablemente al top al incorporar
  meses "solo ONI" en los que sí tuvo eventos que antes quedaban fuera del
  denominador ENSO.

**Impacto en cascada:** Fase 7 (Magnitud) se reejecutó consumiendo
`magnitud_enso_combinada` en vez de derivar solo de `icen_category` — el
techo de la escala ahora sí se alcanza (1.0, "Muy Fuerte" según ONI, 8
meses del episodio 2015-2016) donde antes el máximo observado era 0.75.
Fase 8 (HCI compuesto) se reejecutó sin cambios de código, heredando los
nuevos insumos de Recurrencia y Magnitud — 221 cantones, 24 provincias,
rango [0,1] verificado.

Referencia: `config/config.yaml` → bloque `enso_criterio_ampliado`.

## 1. Objetivo de la fase

Dos objetivos, solicitados juntos por Jerson ("tener en cuenta ENSO 1 y
ENSO 2, regiones que afectan a Ecuador y se relacionan"):

1. Incorporar la SST cruda de la región **Niño 1+2** (0-10°S, 90-80°W —
   la región del Pacífico ecuatorial oriental, la más próxima a la costa de
   Ecuador y Perú) y cuantificar su relación con ICEN y ONI, cerrando
   formalmente la decisión abierta de la Fase 0 §19.4 ("ICEN vs. ONI como
   índice ancla").
2. Calcular el Índice de Recurrencia (Fase 0 §9):
   `Recurrencia = Eventos de Inundación / Total de Eventos ENSO`.

## 2. Fundamento científico

Las cuatro regiones Niño estándar (NOAA) cubren distintas franjas del
Pacífico ecuatorial: Niño 1+2 (90-80°W, la más oriental, frente a la costa
sudamericana), Niño 3 (150-90°W), Niño 3.4 (170-120°W, la que usa ONI) y
Niño 4 (160°E-150°W, la más occidental). El fenómeno de "El Niño costero"
que afecta directamente a Ecuador y Perú está físicamente ligado al
calentamiento del Pacífico oriental (Niño 1+2), no necesariamente al
calentamiento del Pacífico central (Niño 3.4/ONI) — ambos pueden ocurrir
juntos o de forma independiente (de hecho, El Niño costero 2017 fue un
evento con fuerte señal en Niño 1+2 pero débil en Niño 3.4/ONI, un caso ya
documentado en la literatura ENFEN).

ICEN (Índice Costero El Niño), publicado oficialmente por ENFEN
(Perú), se calcula precisamente a partir de la SST de la región Niño 1+2
(ERSSTv5), con una corrección de tendencia (detrending) para aislar la
variabilidad interanual del calentamiento de largo plazo del océano. Es,
por diseño, el índice más adecuado para un análisis de impactos costeros en
Ecuador — la pregunta era si los datos del proyecto lo confirmaban.

## 3. Fuente de datos: SST cruda de Niño 1+2 (NOAA/CPC)

El workbook maestro no trae la SST cruda de Niño 1+2 como hoja — solo trae
ICEN (ya calculado por ENFEN) y ONI. Jerson descargó manualmente
`ersst5.nino.mth.91-20.ascii` de NOAA/CPC (mismo patrón de adquisición que
los límites administrativos en Fase 2 §4.1 — este entorno no tiene salida
de red hacia NOAA/CPC, verificado) y lo colocó en `data/raw/`. Formato:
ancho fijo/espacios, columnas `YR MON NINO1+2 ANOM NINO3 ANOM NINO4 ANOM
NINO3.4 ANOM`, mensual, 1950 a 2026. Se usan solo las columnas de Niño 1+2;
las demás regiones se descartan (Niño 3.4 ya está cubierto por ONI, misma
metodología NOAA).

## 4. Decisiones metodológicas y su justificación

### 4.1 Media móvil trimestral, sin detrending

ICEN y ONI en el workbook están en trimestres móviles (DEF, EFM...); la SST
de Niño 1+2 llega mensual puntual. Se calculó una media móvil centrada de 3
meses para comparabilidad temporal — **sin aplicar ningún ajuste de
tendencia**, a diferencia de ICEN (que sí lo hace por definición oficial
ENFEN). La diferencia entre ambas series, cuando exista, es precisamente la
señal de la tendencia removida por ENFEN, no un error de esta fase.

### 4.2 Cierre de la Fase 0 §19.4: ICEN confirmado como índice ancla, con evidencia propia del proyecto

Correlación de Pearson, calculada sobre la ventana real del proyecto
(2015-2025, no la muestra histórica más amplia usada en la discusión previa
con Jerson):

| Par | r (2015-2025) |
|---|---|
| ICEN vs. Niño 1+2 (crudo) | **0.997** |
| ICEN vs. ONI | 0.794 |
| ONI vs. Niño 1+2 (crudo) | 0.791 |

**Interpretación:** ICEN y la SST cruda de Niño 1+2 son, en la práctica,
la misma señal (r=0.997) — consistente con que ICEN se calcula
oficialmente a partir de esa región. ONI correlaciona de forma moderada-alta
con ambas (~0.79) pero es un fenómeno de escala distinta (Pacífico
central), no una redundancia. Esto confirma con datos propios del proyecto
—no solo con literatura general— la recomendación de usar **ICEN como
índice ancla** para definir "evento ENSO" relevante a inundaciones costeras
en Ecuador. Cierra la decisión abierta de la Fase 0 §19.4.

**Nota sobre una discrepancia aparente:** una verificación rápida inicial
sobre la hoja `ICEN_ONI)` completa del workbook (1965 en adelante, 158
pares) había dado r=0.374 para ICEN-ONI — mucho más bajo que el 0.794 de
esta sección. La diferencia no es un error: son ventanas temporales
distintas (58+ años vs. 11 años) y la relación ICEN-ONI no es estacionaria
en el tiempo (varía según el periodo climático analizado) — se documenta
la discrepancia en vez de ocultarla u omitir una de las dos cifras.

### 4.3 Definición operacional de "evento ENSO" (confirmada por Jerson antes de programar)

**Evento ENSO = mes con categoría ICEN "El Niño" de cualquier magnitud**
(Débil, Moderado, Fuerte o Extraordinario) — se excluyen Neutro y La Niña.
Alternativas presentadas y descartadas: incluir La Niña (lectura más
literal de "Total de Eventos ENSO", pero diluiría el denominador con meses
en que la costa de Ecuador típicamente tiene condiciones más secas, no de
inundación); restringir a El Niño Moderado+ (más estricto, pero reduce
aún más el denominador y excluye episodios Débiles que igual pueden
producir impacto).

**Validación independiente, no buscada a propósito:** contar los meses
2015-2025 con esta definición da **38 meses** — exactamente el mismo número
que `Notas Metodológicas` del workbook usó para construir `Base2` ("38
meses con impacto ENSO documentado", Fase 2 §4.8). La definición
ICEN-céntrica reproduce, de forma independiente, la delimitación temporal
que el propio equipo de FAO/COE ya había usado.

### 4.4 Validación de la hipótesis central del proyecto (antes de calcular el índice)

Se contrastó la hipótesis que justifica todo el diseño del HCI (Fase 0,
H1: los eventos ocurren con mayor frecuencia durante episodios El Niño):
tasa media de eventos por mes, dentro de meses El Niño vs. fuera de ellos.

- Meses El Niño (n=38): **252.8 eventos/mes** en promedio.
- Meses No-El-Niño (n=94): **129.1 eventos/mes** en promedio.
- **Razón: 1.96x** — casi el doble de eventos por mes durante El Niño.

Se reporta el resultado tal cual salió de los datos, no se ajustó nada para
que "se viera bien" — de haber salido cercano a 1x (sin diferencia), habría
cuestionado el diseño completo del proyecto. El resultado obtenido respalda
empíricamente, con datos propios de Ecuador 2015-2025, la premisa
fundacional del HCI.

### 4.5 Fórmula del Índice de Recurrencia: tasa de meses con evento, no conteo crudo

**Elegida:** `Recurrencia = (meses El Niño con ≥1 evento en la unidad) /
(total de meses El Niño, 38)` — acotada en [0,1].

**Alternativa descartada:** `eventos / 38` (conteo crudo de eventos sobre
meses ENSO) — se descartó porque podría superar 1 si una unidad
administrativa tiene varios eventos en un mismo mes, rompiendo la escala
0-1 que comparten los demás índices (Severidad, Fase 4) y que se necesita
para combinarlos sin que uno domine el HCI compuesto solo por su rango
numérico (Fase 8).

### 4.6 Cobertura completa en la vista `"TODOS"` — bug detectado y corregido antes de exportar

La primera versión de la función de agregación generaba filas únicamente
para combinaciones (unidad administrativa × mes ENSO) con al menos un
evento — una unidad con eventos históricos pero **ninguno** en un mes El
Niño (caso real: San Fernando, Azuay, canton_code 0107, un solo evento de
deslizamiento el 2025-02-12, en un mes que no calificó como El Niño) no
generaba ninguna fila, quedando ausente de la tabla en vez de aparecer con
`recurrence_index = 0` — que es la información correcta, no una ausencia de
datos. Corregido con un `merge` explícito contra el universo completo de
221 cantones/24 provincias antes de exportar, con relleno de ceros donde
corresponde. Detectado por la misma disciplina de aserciones de cobertura
usada en Fases 3 y 4 (contar cantones/provincias esperados vs. presentes en
la tabla final), no después de la entrega.

## 5. Esquema de salida

Tres tablas en `data/processed/` (Parquet + CSV):

- `recurrence_index_canton` (835 filas: 221 cantones × hasta 5 vistas,
  incluida `TODOS` con cobertura garantizada al 100%).
- `recurrence_index_provincia` (113 filas, mismo patrón, 24 provincias).
- `enso_index_monthly_extended` (132 filas: la serie mensual ICEN+ONI de
  Fase 1 extendida con `nino12_sst`, `nino12_anom`, `nino12_anom_trim` y
  `es_evento_enso`).

Columnas de `recurrence_index_*`: `province_code`,
`province_name_official`, `canton_code`/`canton_name_official` (solo
cantón), `hazard_type`, `meses_enso_con_evento`, `n_eventos_en_meses_enso`
(crudo, trazabilidad), `recurrence_index` (0-1).

## 6. Resultados — primeras cifras

- **Top cantones por Recurrencia (vista `TODOS`):** Ambato (0.89, 34/38
  meses El Niño con evento), Morona (0.84), Santo Domingo (0.79), Distrito
  Metropolitano de Quito (0.79), Loja (0.76).
- **Top provincias:** Tungurahua y Morona Santiago empatadas en el máximo
  posible (1.0 — evento en los 38/38 meses El Niño de la ventana),
  Chimborazo y Napo (0.97).
- **Distribución cantonal:** media 0.34, mediana 0.32, mínimo 0.03, máximo
  0.89 — ningún cantón llega a 1.0 a nivel individual (sí a nivel
  provincia, donde se agregan más eventos).

## 7. Limitaciones

> **Actualización 2026-10-06 (Fase 15):** la razón cruda de 1.96x de §4.4 no descuenta estacionalidad. Con un modelo Binomial Negativo con efectos fijos de mes y tendencia, el efecto nacional es IRR = 1.41 (IC 95 % 1.17–1.70); por región: Costa 3.45, Sierra 1.15 (no significativo), Oriente 1.09 (no significativo); aluvión 0.46 (inverso). El denominador "meses El Niño" de esta fase mide intensidad de reporte en esos meses, no atribuibilidad a ENSO. Ver `15_enso_hazard_association.md`.

- La correlación ICEN-Niño1+2 (0.997) es prácticamente una identidad
  matemática esperada (ICEN se calcula a partir de esa región) — se reporta
  como confirmación empírica, no como un hallazgo independiente inesperado.
- El umbral "cualquier magnitud El Niño" (§4.3) es una decisión de diseño,
  no una convención universal — otros marcos (p. ej. NOAA para ONI) a veces
  exigen 5 meses consecutivos para declarar un "episodio", umbral que aquí
  no se aplicó (se cuenta mes a mes, no por episodio consecutivo — la
  consecutividad se aborda en la Fase 6, Persistencia).
- El denominador (38 meses) es fijo a nivel nacional para todas las
  unidades administrativas — no se ajustó por ninguna variación regional en
  la manifestación de El Niño dentro de Ecuador (asume que un "mes El Niño"
  climatológico es igualmente relevante para la costa, sierra y oriente,
  lo cual es una simplificación conocida).

## 8. Supuestos

- Se asume que la ausencia de detrending en la serie de Niño 1+2 (§4.1) no
  afecta materialmente la comparación cualitativa con ICEN dentro de la
  ventana 2015-2025 (11 años, tendencia de largo plazo probablemente
  pequeña frente a la variabilidad interanual) — no se verificó
  cuantitativamente el tamaño de esa tendencia.

## 9. Ventajas del enfoque

- Decisión del índice ancla (ICEN vs. ONI) resuelta con evidencia empírica
  del propio proyecto, no por preferencia arbitraria ni solo por precedente
  bibliográfico.
- La hipótesis central del proyecto se validó explícitamente antes de
  construir el índice (§4.4) — si no se hubiera cumplido, el diseño se
  habría reconsiderado en vez de continuar.
- El bug de cobertura (§4.6) se detectó y corrigió antes de exportar,
  gracias a mantener la misma disciplina de aserciones de las fases
  anteriores.

## 10. Posibles mejoras futuras

- Evaluar una definición de "episodio ENSO" basada en consecutividad (p.
  ej. ≥3 meses consecutivos en categoría El Niño) en vez de mes a mes,
  cuando se aborde la Fase 6 (Persistencia) — podría cambiar el
  denominador de 38 a un número menor de "episodios".
- Cuantificar el tamaño de la tendencia de largo plazo en la serie cruda de
  Niño 1+2 dentro de 2015-2025, para confirmar cuantitativamente el
  supuesto de §8.

## 11. Referencias

- Fase 0 — Diseño Conceptual HCI Ecuador, §9 (fórmula de Recurrencia),
  §19.4 (decisión ICEN vs. ONI).
- NOAA/CPC — ERSSTv5 monthly Niño region indices
  (`ersst5.nino.mth.91-20.ascii`).
- ENFEN (Perú) — metodología oficial del Índice Costero El Niño (ICEN).
- `docs/methodology/02_spatial_integration.md` §4.8 (los mismos 38 meses
  ENSO, verificados de forma independiente en esta fase).
