# 09 — Análisis Espacial

**Fase:** 9 de 10 (ver Fase 0, §8)
**Notebook asociado:** `notebooks/Step9_Ecuador_Spatial_Analysis.ipynb`
**Estado:** implementado y ejecutado — 2026-08-06
**Audiencia:** científicos, desarrolladores, especialistas DRM/FAO AA

## 1. Objetivo de la fase

Determinar si la cronicidad de inundaciones en Ecuador se distribuye
aleatoriamente en el espacio o forma agrupamientos geográficos
(clusters) estadísticamente significativos — información que un
ranking cantón-por-cantón (Fase 8) no puede responder por sí solo.
Cuatro técnicas complementarias, todas sobre las salidas ya validadas
de las Fases 1-8:

1. Getis-Ord Gi* — hotspots/coldspots (¿esta zona y sus vecinos son
   sistemáticamente altos o bajos?).
2. Local Moran's I — clusters (HH/LL) y valores atípicos espaciales
   (HL/LH).
3. Densidad kernel (KDE) — superficie continua de impacto, sin las
   fronteras artificiales de los polígonos administrativos.
4. Agregación hexagonal (H3) — comparación entre unidades de área
   uniforme, corrigiendo el sesgo visual de comparar cantones de
   tamaño muy distinto.

## 2. Fundamento científico

Gi* y Local Moran's I son los dos estadísticos estándar de
autocorrelación espacial local en econometría espacial (Getis & Ord
1992; Anselin 1995) — son complementarios, no redundantes: Gi* mide
"¿es esta zona y su entorno alto/bajo?" (una pregunta sobre nivel);
Local Moran's I mide "¿el valor de esta unidad es consistente con el
de sus vecinos, o es un atípico local?" (una pregunta sobre similitud/
disimilitud). Usar ambos, como aquí, es la práctica recomendada — cada
uno puede señalar patrones que el otro no captura (p. ej. un HL de
Moran's I sin ser necesariamente un coldspot Gi*, ver §6.3).

## 3. Fundamento estadístico

- **Significancia por permutación condicional** (999 permutaciones,
  semilla fija=42 para reproducibilidad), no por supuesto de
  normalidad — estándar para datos espaciales, que rara vez son
  normales.
- **Transformación de pesos:** Gi* usa pesos **binarios** (convención
  estándar para este estadístico); Local Moran's I usa pesos
  **fila-estandarizados** — misma topología de vecindad (§4), distinta
  transformación, cada una la convención propia de su estadístico.
- **KDE (Kernel Density Estimation)** con bandwidth de Silverman —
  regla estándar que adapta el ancho de banda a la dispersión real de
  los datos, en vez de fijar un valor arbitrario.
- **H3 (Hexagonal Hierarchical Spatial Index)**, la librería estándar
  de Uber para indexado hexagonal jerárquico — resolución 5 (~9.85 km
  de borde promedio), la más cercana a los "~10 km" pedidos por
  Jerson.

## 4. Decisiones metodológicas y su justificación

Todas confirmadas por Jerson vía AskUserQuestion (2026-08-06) antes de
programar — ver también `config.yaml` bloque `spatial_analysis`.

### 4.1 Variables: HCI + los 4 sub-índices, no solo el compuesto

Gi* y Local Moran's I se calculan sobre 5 capas (`hci`,
`severity_index`, `recurrence_index`, `persistence_index`,
`enso_magnitude_mean`) en vez de solo el HCI final. Decisión
explícita de Jerson: permite diagnosticar si un hotspot de HCI está
impulsado por un componente específico (§6.4) — información que un
único análisis sobre el HCI compuesto ocultaría.

### 4.2 Pesos espaciales: Queen + respaldo KNN=1, delegado a criterio técnico

Jerson delegó explícitamente la elección técnica ("el mejor para este
tipo de ejercicios"). Se usó contigüidad **Queen** de orden 1 —
convención estándar en econometría espacial (Anselin) para polígonos
administrativos irregulares, más permisiva que Rook (cuenta como
vecinos polígonos que comparten un solo vértice, no solo frontera).

**Problema real encontrado y verificado, no hipotético:** 3 cantones
(San Cristóbal, Isabela, Santa Cruz — los 3 cantones de la provincia de
Galápagos) no tienen ningún vecino por contigüidad, lo cual habría roto
el cálculo de Gi*/Local Moran's I para esas 3 unidades. Se verificó
explícitamente, antes de decidir la solución, que un respaldo KNN=1
(conectar cada isla a su centroide más cercano) conecta lo que
corresponde geográficamente: las 3 conexiones resultantes son
Galápagos-con-Galápagos (85-94 km entre sí), no con el continente
(>900 km) — confirma que el respaldo no es un artefacto arbitrario,
sino el resultado geográficamente correcto.

### 4.3 KDE: ponderado por severidad de evento, no densidad simple

Un score de severidad a nivel evento individual se recalculó con la
misma fórmula de pilares de Fase 4 §4.1 (mismos multiplicadores de
`config.yaml`), normalizado 0-1 a nivel nacional — **no es el mismo
`severity_index`** de Fase 4 (que agrega por máximo histórico y
normaliza por cantón); es una versión evento-a-evento, calculada
específicamente para esta fase. Ponderar por severidad, no solo contar
eventos, evita que una zona con muchos eventos leves domine visualmente
sobre una zona con pocos eventos graves.

### 4.4 Hexágonos: "hexbin" sobre eventos, no relleno de polígono nacional

En vez de rellenar todo el territorio con hexágonos (miles de celdas
vacías sobre el océano/zonas sin eventos), cada uno de los 21,743
eventos se asigna a su celda H3 (resolución 5) y se agrega solo sobre
las celdas con ≥1 evento (719 de las posibles) — el enfoque estándar
de "hexbin" para datos puntuales, más eficiente y sin ruido de celdas
vacías.

## 5. Validaciones aplicadas

- Cobertura completa: 221 cantones en las tablas de Gi*/Local Moran's
  I, sin nulos ni infinitos.
- 0 islas tras el respaldo KNN (verificado con `assert`).
- Suma de eventos por hexágono = 21,743 (coincide exactamente con el
  total de eventos, sin pérdidas ni duplicados).
- Verificación de sentido común: Quito (el cantón #1 en HCI, Fase 8
  §7) aparece como hotspot 95% (Gi*) y cluster HH (Moran's I) en la
  capa `hci` — consistente con lo esperado, no contradictorio.

## 6. Resultados

### 6.1 Getis-Ord Gi* — HCI

De 221 cantones: **51 hotspots** (11 al 99%, 19 al 95%, 21 al 90%) y
**13 coldspots** (3 al 99%, 4 al 95%, 6 al 90%); 157 sin significancia.

Los 11 hotspots al 99% forman un arco geográfico coherente, no puntos
aislados: Quinindé (Esmeraldas) - La Concordia (Santo Domingo) -
Cayambe/Mejía/Pedro Moncayo/Rumiñahui/San Miguel de los Bancos
(Pichincha, todos alrededor de Quito) - Santiago de Píllaro
(Tungurahua) - Archidona/El Chaco/Quijos (Napo/Amazonía norte).
Nota: el propio Distrito Metropolitano de Quito es hotspot al 95%, no
al 99% — su vecindario inmediato es un núcleo aún más consistentemente
alto que el propio Quito, un patrón real, no un error.

Los 13 coldspots se concentran en dos clusters geográficos: la
provincia de Sucumbíos casi completa (Lago Agrio 99%, Shushufindi 99%,
Cuyabeno 99%, Putumayo 95%, Sucumbíos 90%, La Joya de los Sachas 95% —
Amazonía norte, ENSO/costa tiene poca influencia allí, resultado
esperado) y un segundo cluster en Azuay (Cuenca 95%, Sevilla de Oro
90%, Guachapala 90%) + Carchi (Montúfar 90%) + Morona Santiago (Morona
90%, Santiago 90%).

### 6.2 Local Moran's I — HCI

21 clusters Alto-Alto (HH), 6 Bajo-Bajo (LL), 9 Bajo-Alto (LH), 1
Alto-Bajo (HL) — 184 sin significancia al 95%.

Los clusters HH confirman y refinan el patrón de Gi*: incluyen Quito
directamente (a diferencia de Gi* al 99%), más un cluster costero
(Esmeraldas, Muisne, Atacames, Rioverde, Pedernales, Flavio Alfaro,
Quinindé) y un cluster central Andino/amazónico (Guaranda, Guano,
Pallatanga en Bolívar/Chimborazo; Archidona, El Chaco, Quijos, Loreto
en la Amazonía norte). Los clusters LL coinciden exactamente con el
coldspot de Sucumbíos identificado en Gi* (§6.1), más Santa Cruz
(Galápagos) — un resultado estructural genuino: dentro del subgrafo de
3 cantones de Galápagos conectado por el respaldo KNN (§4.2), Santa
Cruz tiene un HCI relativamente bajo rodeado de vecinos igualmente
bajos, no un artefacto de la conexión KNN en sí.

### 6.3 Un caso HL, valioso como hallazgo diagnóstico

Cuenca es el único cantón "Alto-Bajo (HL)": su propio HCI es
relativamente alto, pero está rodeado de vecinos de HCI bajo — y por
eso mismo aparece como coldspot en Gi* (que promedia con los vecinos),
no como hotspot. Esto no es una contradicción entre los dos métodos:
es exactamente la información adicional que Local Moran's I aporta
sobre Gi* — Cuenca no es "poco crónico" en términos absolutos, es un
cantón relativamente crónico en una región (Azuay) que, en conjunto, lo
es poco.

### 6.4 Comparación entre las 5 capas — ¿qué impulsa los hotspots de HCI?

De los 51 hotspots de HCI (cualquier nivel de confianza), el
solapamiento con los hotspots de cada sub-índice:

| Sub-índice | Hotspots propios | Solapan con hotspots de HCI | % de los 51 hotspots de HCI |
|---|---|---|---|
| Recurrencia | 54 | 42 | 82% |
| Persistencia | 63 | 34 | 67% |
| Severidad | 48 | 28 | 55% |
| Magnitud ENSO | 57 | 13 | 25% |

**Hallazgo no obvio:** los hotspots de HCI están dominados por
Recurrencia y Persistencia, no por Severidad ni Magnitud ENSO — pese a
que Severidad tiene casi tanto peso en la fórmula (0.30) como
Recurrencia (0.35). Interpretación: Recurrencia y Persistencia miden
procesos sostenidos en el tiempo (¿con qué frecuencia y por cuánto
tiempo?), que tienden a tener una firma geográfica coherente (franjas
climáticas, cuencas hidrográficas); Severidad depende en parte de
eventos individuales extremos e idiosincráticos (ver los outliers de
Fase 4 §6/Fase 8 §5.3), que son menos predecibles espacialmente. Esto
es consistente, no contradictorio, con que Severidad sea el parámetro
más sensible en términos de valor numérico (Fase 8 §5.3) — sensible en
magnitud no implica necesariamente agrupado en el espacio.

### 6.5 Densidad Kernel (KDE)

La superficie de densidad ponderada por severidad confirma el mismo
núcleo identificado por Gi*/Moran's I: el punto de densidad más alta
(normalizado=1.0) está en el Distrito Metropolitano de Quito, con una
meseta de valores altos (>0.85) extendida sobre Quito, Rumiñahui y
Mejía (los 3 cantones inmediatamente colindantes al sur/este de Quito)
— consistente con el hallazgo de §6.1 de que el "núcleo" del cluster es
más el entorno de Quito que Quito mismo en aislamiento. La distribución
de densidad normalizada es fuertemente sesgada (mediana=0.014,
media=0.089, máximo=1.0): la mayor parte del territorio tiene densidad
de impacto ponderado muy baja, consistente con un fenómeno
geográficamente concentrado, no difuso.

**Nota de alcance:** la grilla KDE (5,032 puntos, paso 10 km) cubre
Ecuador continental; Galápagos se excluye de esta superficie continua
por su distancia extrema (incluirla generaría una grilla dominada por
océano vacío), aunque sus eventos sí participan en el ajuste del KDE.

### 6.6 Agregación hexagonal (H3 resolución 5)

719 celdas con al menos 1 evento (de los 21,743 eventos, suma exacta
verificada). Las celdas con más eventos se ubican, de nuevo, en Quito
(3 de las 5 celdas con más eventos, hasta 556 eventos en una sola
celda) y en el "eje central" del país (Ambato/San Pedro de Pelileo en
Tungurahua, Guayaquil, Cuenca, Baños de Agua Santa) — coherente con los
hallazgos anteriores. Al ordenar por `severity_sum` en vez de
`n_eventos`, el orden cambia notablemente: Chone y Babahoyo (con menos
eventos que Quito, pero de mayor severidad promedio) superan a varias
celdas de Quito — confirma, a nivel de grano fino, el mismo patrón ya
visto en Fase 8 §7 (Quito lidera por persistencia/recurrencia, Chone
por severidad).

## 7. Esquema de salida

- `hotspots_gi_star_canton.{parquet,csv}` (221 filas): z-score,
  p-valor de permutación y clasificación (7 niveles) de Gi*, para cada
  una de las 5 variables.
- `local_moran_canton.{parquet,csv}` (221 filas): I local, p-valor y
  cuadrante (HH/LL/HL/LH/No significativo), para cada una de las 5
  variables.
- `kde_severidad_grid.{geojson,csv}` (5,032 puntos): densidad KDE
  cruda y normalizada 0-1, grilla de 10 km sobre Ecuador continental.
- `hexagonos_h3_res5.{geojson,csv}` (719 celdas): n_eventos,
  severidad media/máxima/suma, tipo de peligro dominante, por celda
  H3 con ≥1 evento.

## 8. Limitaciones

- El respaldo KNN=1 para Galápagos conecta esos 3 cantones solo entre
  sí, aislados del continente en la matriz de pesos — cualquier
  hallazgo de cluster que involucre Galápagos (§6.2, Santa Cruz en LL)
  debe interpretarse como interno al archipiélago, no comparable
  directamente con el continente.
- El KDE excluye Galápagos de la superficie evaluada (§6.5) — no hay
  superficie de densidad continua para esa provincia en esta fase.
- El `event_severity_score` usado para ponderar el KDE (§4.3) es una
  aproximación a nivel evento, no el `severity_index` oficial de Fase
  4 — ambos usan la misma fórmula de pilares pero agregan/normalizan
  de forma distinta; no deben compararse numéricamente entre sí.
- No se probó sensibilidad a la resolución H3 (solo resolución 5) ni al
  método de bandwidth del KDE (solo Silverman) — quedan como mejoras
  futuras si se requiere robustez adicional en esta fase específica.
- Como en fases anteriores, no se ha hecho validación externa contra
  UNOSAT/EM-DAT/DesInventar/Copernicus EMS (Fase 0 §12).

## 9. Supuestos

- Se asume que la vista `"TODOS"` (todos los tipos de peligro
  combinados) es la relevante para el análisis espacial nacional — no
  se corrió Gi*/Local Moran's I por separado para cada `hazard_type`
  en esta fase (posible extensión futura).
- El respaldo KNN=1 asume que "el vecino geográfico más cercano" es una
  aproximación razonable de vecindad quality para unidades sin
  contigüidad — válido aquí porque se verificó explícitamente (§4.2),
  no se asumió sin comprobar.

## 10. Ventajas del enfoque

- Las 4 técnicas son complementarias, no redundantes, y sus resultados
  son mutuamente consistentes (§6.1-6.6 convergen en el mismo núcleo
  geográfico: entorno de Quito/Pichincha) — un resultado consistente en
  4 métodos distintos es una señal de robustez más fuerte que cualquiera
  de ellos por separado.
- El caso de Cuenca (§6.3) muestra explícitamente el valor de combinar
  Gi* y Local Moran's I: uno solo habría dado una lectura incompleta.
- La comparación entre las 5 capas (§6.4) es un hallazgo diagnóstico
  genuino, no anticipado en el diseño original (Fase 0 §8 no
  especificaba correr hotspots sobre los sub-índices) — surgió de la
  decisión de Jerson de incluir los 4 sub-índices, no solo el HCI.

## 11. Posibles mejoras futuras

- Repetir Gi*/Local Moran's I por `hazard_type` individual (no solo la
  vista `"TODOS"`), si se requiere un diagnóstico más fino por tipo de
  peligro.
- Probar sensibilidad del KDE a distintos métodos de bandwidth (Scott,
  fijo en km) y de la agregación hexagonal a otras resoluciones H3
  (4 o 6).
- Analizar Galápagos con un enfoque espacial separado (p. ej. contra
  un límite regional insular, no continental) dado que la matriz de
  pesos actual los trata como un subgrafo aislado.
- Cruzar los hexágonos de mayor densidad (§6.6) con capas futuras
  (CHIRPS, DEM, uso de suelo — Fase 0 §3, capas opcionales) para
  explorar causas físicas del patrón observado, no solo describirlo.

## 12. Referencias

- Fase 0 — Diseño Conceptual HCI Ecuador, §8 (análisis espacial).
- `docs/methodology/08_hci_composite.md` §7 (ranking HCI usado como
  referencia de sentido común en §5 de este documento).
- Getis, A. & Ord, J.K. (1992). "The Analysis of Spatial Association by
  Use of Distance Statistics." *Geographical Analysis*.
- Anselin, L. (1995). "Local Indicators of Spatial Association—LISA."
  *Geographical Analysis*.
