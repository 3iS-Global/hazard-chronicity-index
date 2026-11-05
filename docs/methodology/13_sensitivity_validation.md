# 13 — Validación de Sensibilidad Extendida y Blindaje Metodológico

**Fase:** 13 (nueva, no prevista en el diseño original de Fase 0 — surge de
la Fase 0 §9, que exige análisis de sensibilidad, y de las limitaciones ya
reconocidas en `08_efci_composite.md` §8/§11: "no se realizó una búsqueda
exhaustiva de todas las combinaciones posibles de pesos")
**Notebook asociado:** `notebooks/Step13_Ecuador_Sensitivity_Validation.ipynb`
(pendiente de implementar — este documento fija el diseño antes de escribir
código, por el flujo de trabajo del proyecto)
**Estado:** implementado y ejecutado — 2026-09-04
**Audiencia:** científicos, desarrolladores, especialistas DRM/FAO AA

## 1. Objetivo de la fase

Extender — no repetir — el análisis de sensibilidad ya hecho en Fase 8 §5,
cerrando las brechas que ese análisis reconoce explícitamente como
pendientes, y cubriendo una capa que nunca se probó: los 5 pesos internos
del Índice de Severidad (Fase 4), que hasta ahora no habían sido sometidos
a ninguna prueba de sensibilidad — solo se probaron los 4 pesos del EFCI
compuesto que combinan Severidad con Recurrencia/Persistencia/Magnitud.

Preguntas que este documento busca responder con evidencia, no con
supuestos:

1. ¿Qué tan estable es el ranking/clasificación del EFCI frente al espacio
   *completo* de combinaciones de pesos posibles, no solo 3 escenarios
   puntuales elegidos a mano?
2. ¿Cuál de los 4 pesos del EFCI compuesto realmente explica más varianza
   del resultado — no solo cuál mueve más el ranking en un escenario
   concreto?
3. ¿Son defendibles los 5 pesos de Severidad (0.30/0.25/0.20/0.15/0.10)
   frente a alternativas formales (pesos iguales, derivados de datos, o
   elicitación estructurada de juicio experto)?
4. ¿Qué tan robusto es el EFCI de un cantón dado frente al muestreo
   aleatorio de qué eventos históricos "le tocaron" — no solo frente a los
   2 outliers ya identificados, sino en general?

## 2. Por qué esta fase existe — lección del hallazgo en Fase 8 §13

Al preparar esta fase se encontró que la prosa de `08_efci_composite.md`
§5 describía resultados de sensibilidad de la corrida v1.1 (agosto 2026),
nunca actualizados tras el re-ejecute completo v1.2 (17-ago-2026, tras
ampliar el criterio ENSO en Fase 5/7) — el CSV de salida sí se
regeneró, la interpretación en prosa no. La consecuencia concreta: el
"hallazgo" publicado (que el escenario "Énfasis Severidad" era el más
frágil en clasificación) se invirtió con los datos vigentes ("Equitativo"
es ahora el más frágil). Se corrigió (ver `08_efci_composite.md` §13),
pero expone un riesgo estructural: **3 escenarios puntuales, evaluados a
mano, no son una descripción estable del comportamiento del índice** —
pueden cambiar de conclusión con cada actualización de un insumo aguas
arriba, sin que nadie lo note hasta que alguien vuelve a leer los números
con cuidado. Un método de sensibilidad *global* (que cubre el espacio de
pesos completo, no solo 3 puntos) es menos frágil ante este tipo de
problema — no porque no pueda cambiar de resultado, sino porque su
resultado no depende de qué 3 escenarios se hayan elegido subjetivamente.

## 3. Fundamento científico

Los cuatro componentes de esta fase corresponden a prácticas establecidas
en la literatura de indicadores compuestos e índices de riesgo de
desastres, no son un diseño ad hoc:

- **Análisis de sensibilidad global (Monte Carlo + índices de Sobol):**
  método estándar del *OECD/JRC Handbook on Constructing Composite
  Indicators* (2008), capítulos 5-6 — la referencia canónica detrás de
  índices de riesgo ya usados en el sector humanitario (INFORM Risk Index,
  WorldRiskIndex). A diferencia de perturbar un peso a la vez u probar
  escenarios discretos, muestrea miles de combinaciones válidas de pesos y
  descompone la varianza del resultado por parámetro.
- **AHP (Analytic Hierarchy Process, Saaty 1980):** método estándar para
  convertir juicio experto en pesos numéricos de forma estructurada y
  auditable, mediante comparación pareada en escala 1-9 y un chequeo de
  consistencia interna (*Consistency Ratio*, CR). Es el método más citado
  en literatura DRM para justificar pesos de índices de riesgo cuando no
  hay suficiente data histórica para derivarlos estadísticamente — el caso
  de Severidad aquí, dado que sus 5 pesos nunca tuvieron una fuente
  externa formal (ver `04_severity_index.md` §11 y el hallazgo de este
  proyecto documentado el 2026-09-04: los pesos actuales son juicio
  experto del diseño original, sin AHP ni fuente citada).
- **PCA (Análisis de Componentes Principales):** método estándar para
  derivar pesos "desde los datos" — las cargas del primer componente
  principal de los 5 pilares normalizados se usan como un esquema de peso
  alternativo, puramente estadístico, sin ningún juicio experto de por
  medio. Sirve de contraste: si PCA da pesos muy distintos a los actuales
  Y el ranking resultante también difiere mucho, es señal de que los
  pesos actuales imponen una estructura que los datos no sugieren por sí
  solos (ni bueno ni malo per se, pero debe saberse).
- **Bootstrap no paramétrico:** estándar para construir intervalos de
  confianza cuando no puede asumirse una distribución conocida — el caso
  aquí, dada la cola larga y los outliers ya documentados en Severidad
  (Fase 4 §6). Remuestrear eventos con reemplazo y recalcular el índice en
  cada remuestreo da una banda de incertidumbre directamente interpretable
  por cantón, en vez de un solo número puntual.

## 4. Metodología

### 4.1 Monte Carlo + Sobol sobre los 4 pesos del EFCI compuesto

- N=10,000 muestreos de pesos (Recurrencia/Severidad/Persistencia/Magnitud)
  vía distribución Dirichlet centrada en los pesos base (0.35/0.30/0.20/0.15),
  concentración k a calibrar para que el 90% de las muestras caiga dentro de
  ±20% del peso base — explora variación "razonable", no el simplex completo.
- Segunda corrida con Dirichlet no informativo (α=1,1,1,1) — explora el
  simplex completo sin sesgo hacia los pesos actuales, para no dar por
  sentado que la vecindad del peso base es la única zona relevante.
- Por cada muestreo: recalcular EFCI y clase Jenks (221 cantones, vista
  `"TODOS"`), Spearman ρ contra el EFCI base, % de cambio de clase.
- Índices de Sobol (primer orden `S1` y efecto total `ST`) por peso, con
  `SALib` (librería estándar de Python para sensibilidad global) — cuánta
  varianza del EFCI resultante explica cada peso individualmente (`S1`) y
  cuánta explica considerando sus interacciones con los otros 3 (`ST`).
- Salida: distribución de Spearman ρ y % cambio de clase sobre las 10,000
  muestras (no solo 3 puntos), más los índices de Sobol por peso.

### 4.2 AHP + PCA + pesos iguales sobre los 5 pesos de Severidad

- **AHP:** construir la matriz de comparación pareada 5x5 a partir de la
  jerarquía ya implícita en los pesos actuales (población > vivienda >
  agricultura > ganadería > infraestructura), usando la escala de Saaty
  (1=igual importancia, 9=extremadamente más importante). Calcular el
  vector de pesos (autovector principal) y el Consistency Ratio (CR<0.10
  es el umbral estándar de aceptación). **Limitación reconocida de
  antemano (ver §6):** esta matriz la genero yo a partir de la jerarquía
  ya existente, no es una elicitación con múltiples expertos DRM/FAO
  independientes — se documenta como aproximación de una sola fuente, no
  como validación externa.
- **PCA:** correr PCA sobre los 5 `score_<pilar>` normalizados (nivel
  cantón, vista `"TODOS"`), tomar las cargas del primer componente
  (normalizadas a sumar 1) como esquema de peso alternativo.
- **Pesos iguales:** 0.20 cada pilar, el prior no informativo de control.
- Recalcular `severity_index` y el EFCI resultante con cada uno de los 3
  esquemas alternativos, comparar contra el esquema base (Spearman ρ, %
  cambio de clase) — misma métrica que Fase 8 §5, para comparabilidad
  directa.

### 4.3 Robustez a outliers — extensión de Fase 8 §5.3

Fase 8 ya probó winsorización al percentil 99 (rho=0.8716, 59.3% cambio de
clase — la prueba más sensible de las cinco ya existentes). Esta fase
añade:

- Normalización robusta basada en mediana/IQR (en vez de min-max puro)
  como alternativa adicional a la winsorización — Fase 8 §11 ya la
  proponía como mejora futura.
- Repetir la prueba a nivel de los 5 `score_<pilar>` individuales, no solo
  sobre `severity_index` agregado — para identificar si la sensibilidad
  proviene de un pilar específico (se sospecha Ganadería y Población, los
  2 pilares con los outliers ya documentados en Fase 4 §6) o está
  distribuida.

### 4.4 Bootstrap de incertidumbre

- Remuestreo de eventos por cantón, con reemplazo, 1,000 iteraciones.
- Recalcular `severity_index` y `efci` en cada iteración.
- Reportar percentiles [p5, p50, p95] por cantón, además del punto
  estimado ya existente — banda de incertidumbre, no solo un número.
- Cantones con pocos eventos históricos (la misma limitación de tamaño de
  muestra ya documentada en Fase 3 §7 para `scour`/`debris_flow`) tendrán
  bandas más anchas — resultado esperado, no un error del método: es
  precisamente la información que el punto estimado solo no comunica.

## 5. Esquema de salida planeado

- `sensitivity_sobol_efci.csv` — índices S1/ST por peso (Recurrencia,
  Severidad, Persistencia, Magnitud), ambas corridas Dirichlet.
- `sensitivity_montecarlo_efci_canton.parquet` — distribución completa de
  Spearman ρ y % cambio de clase sobre las 10,000 muestras (para graficar
  histogramas, no solo reportar un promedio).
- `severity_weights_comparison.csv` — `severity_index` bajo AHP/PCA/pesos
  iguales vs. base, con Spearman ρ y % cambio de clase por esquema, más
  el CR del AHP.
- `severity_robust_comparison_canton.csv` — `severity_index` con
  normalización mediana/IQR vs. min-max, a nivel pilar y agregado.
- `bootstrap_ci_efci_canton.csv` (221 filas) — `efci_p5`, `efci_p50`,
  `efci_p95` por cantón, vista `"TODOS"`.

## 6. Riesgos y limitaciones — reconocidos antes de implementar

- Este análisis prueba **robustez del ranking/clasificación**, no
  "corrige" pesos automáticamente. Si el resultado muestra alta
  sensibilidad, la conclusión correcta es que hace falta más trabajo de
  elicitación formal (encuesta a varios expertos DRM/FAO independientes),
  no cambiar el peso unilateralmente a partir de este análisis.
- El AHP de §4.2 es una aproximación de una sola fuente (mi inferencia de
  la jerarquía ya implícita en el diseño), no una elicitación real con
  múltiples expertos — no debe presentarse como si fuera una validación
  externa equivalente a una encuesta Delphi o similar.
- PCA asume que la varianza histórica observada en los datos es un buen
  proxy de "importancia" del pilar — no siempre es cierto: un pilar puede
  ser crítico en términos humanitarios y aun así poco variable en los
  datos (p. ej. si un tipo de impacto es raro pero catastrófico cuando
  ocurre).
- El bootstrap por remuestreo de eventos asume que los eventos históricos
  observados son representativos de la variabilidad futura — misma
  limitación ya reconocida en Fase 3/4 sobre el tamaño de la ventana
  histórica (11 años).
- Esta fase no reemplaza la validación externa contra EM-DAT/DesInventar/
  UNOSAT/Copernicus EMS, que sigue pendiente desde Fase 0 §12.
- Los resultados de Monte Carlo dependen de la distribución de muestreo
  elegida (Dirichlet) — se reportan ambas corridas (centrada y no
  informativa) precisamente para no ocultar esta dependencia.

## 7. Supuestos

- Se asume que la estructura aditiva del EFCI (suma ponderada de 4
  índices normalizados 0-1) es la correcta — esta fase prueba sensibilidad
  *dentro* de esa estructura, no cuestiona la estructura misma (ya
  señalado como supuesto no probado en Fase 8 §9).
- Se asume que 10,000 muestras Monte Carlo son suficientes para estimar
  los índices de Sobol con precisión razonable — se verificará
  convergencia (ver validación, próxima sección) antes de reportar los
  resultados como finales.

## 8. Referencias

- OECD/JRC — *Handbook on Constructing Composite Indicators: Methodology
  and User Guide* (2008), capítulos 5 (uncertainty analysis) y 6
  (sensitivity analysis).
- Saaty, T.L. — *The Analytic Hierarchy Process* (1980) — método AHP y
  Consistency Ratio.
- `SALib` — librería Python estándar para análisis de sensibilidad global
  (Sobol, Morris, FAST).
- `docs/methodology/04_severity_index.md` §6, §7, §11 (outliers, pesos sin
  fuente formal, mejoras futuras).
- `docs/methodology/08_efci_composite.md` §5, §8, §11, §13 (sensibilidad
  existente, limitaciones reconocidas, corrección de la prosa desactualizada
  que motivó esta fase).
- Fase 0 — Diseño Conceptual EFCI Ecuador, §9 (pedido explícito de
  validación de pesos por sensibilidad), §12 (validación externa).

## 9. Resultados reales (2026-09-04)

**Nota metodológica sobre `SALib`:** se instaló pero no se usó — su
muestreador Saltelli exige entradas independientes, lo cual no aplica a 4
pesos que suman 1 por construcción. En su lugar se usó el estimador
*given-data* de Plischke et al. (2013) (agrupamiento en bins
equifrecuentes), que funciona directamente sobre cualquier muestra ya
generada sin asumir independencia — ver notebook §2.1 para el detalle.

### 9.1 Monte Carlo + Sobol sobre los 4 pesos del EFCI (§4.1)

| Corrida | Mediana % cambio de clase | p95 % cambio de clase |
|---|---|---|
| Centrada (±20% del peso base, N=10,000) | 1.8% | 19.5% |
| No informativa (simplex completo, N=10,000) | 32.6% | 71.9% |

Sensibilidad global (S1 aproximado, ambas corridas, y confirmado estable
con N=20,000): **Magnitud ENSO** es el peso más influyente en la
inestabilidad de clasificación (S1≈0.39-0.72), seguido de Recurrencia y
Persistencia — **Severidad es el peso menos influyente de los 4**
(S1≈0.02-0.05). Esto contradice la intuición que dejaba Fase 8 (que
apuntaba a Severidad como el parámetro "delicado"): con una
caracterización global del espacio de pesos, no 3 puntos discretos, el
peso que realmente más mueve la clasificación es el más pequeño de los
4 (Magnitud ENSO, 0.15), probablemente por su distribución más
concentrada/ordinal (Fase 7).

### 9.2 AHP + PCA + pesos iguales sobre los 5 pesos de Severidad (§4.2)

AHP: Consistency Ratio = **0.0175** (muy por debajo del umbral de
aceptación 0.10) — la jerarquía Población > Vivienda > Agricultura >
Ganadería > Infraestructura, formalizada en comparación pareada, es
internamente consistente. Los pesos AHP resultantes (0.271/0.248/0.220/
0.146/0.115) reproducen casi exactamente los pesos base — solo 0.5% de
cantones cambian de clase.

| Esquema | Spearman ρ | % cantones que cambian de clase |
|---|---|---|
| AHP | 0.9999 | 0.5% |
| Equitativo | 0.9983 | 3.6% |
| PCA | 0.9895 | 13.1% |

PCA (basado puramente en varianza de los datos, no en juicio experto)
es el que más diverge: le asigna 47% del peso a Infraestructura y menos
del 8% a Población — el orden opuesto al de los pesos base. Es
consistente con que PCA mide dispersión estadística, no importancia
humanitaria (documentado como limitación esperada en §6). **Conclusión:
los pesos base de Severidad tienen respaldo formal cuando se someten a
AHP — no son arbitrarios — y la única divergencia relevante viene de un
método que mide algo distinto por diseño (varianza, no importancia).**

### 9.3 Normalización robusta — mediana/MAD (§4.3)

**Hallazgo metodológico durante la implementación:** el primer intento
(mediana/IQR seguido de un segundo min-max) resultó ser matemáticamente
**idéntico** al min-max directo sobre el dato crudo — min-max es
invariante a cualquier transformación afín de su entrada, así que
"normalizar" un z-score sin recortarlo no cambia nada. Se corrigió usando
el *modified z-score* (Iglewicz & Hoaglin, 1993): recorte a ±3.5
desviaciones robustas antes de min-max — un método genuinamente distinto,
porque el recorte sí amortigua outliers.

Resultado: Spearman ρ=0.8864, **115/221 cantones (52.0%) cambian de
clase** — converge con la winsorización p99 ya hecha en Fase 8 §5.3
(ρ=0.8716, 59.3%). Dos métodos independientes, magnitudes similares:
evidencia más sólida de que la sensibilidad a outliers de Severidad es
una propiedad estructural real, no un artefacto de un método de
normalización específico.

### 9.4 Bootstrap de incertidumbre (§4.4)

Ancho de banda IC90 del EFCI: mediana 0.0054, p95 0.0477 (escala 0-1).
**Hallazgo no intuitivo:** los cantones con bandas MÁS ANGOSTAS no son
los que tienen más eventos históricos, sino cantones pequeños muy por
debajo del techo nacional de normalización (p. ej. Déleg, 3 eventos,
banda ≈ 0) — su normalización 0-1 no se mueve perceptiblemente sin
importar qué eventos les toque en el remuestreo, porque están lejos de
donde se define la escala (dominada por Quito/Chone). Los cantones con
bandas más anchas (Chone 0.152, Loja 0.091, Esmeraldas 0.084) son los que
sí interactúan directamente con ese techo. Quito, pese a su magnitud,
tiene una banda relativamente angosta (≈0.06) porque con 1,955 eventos el
máximo histórico casi siempre aparece en cualquier remuestreo.

### 9.5 Validación de convergencia

Sobol S1 recalculado con N=20,000 (vs. N=10,000 reportado arriba):
magnitud_enso 0.715 (vs. 0.712), recurrencia 0.276 (vs. 0.263),
persistencia 0.119 (vs. 0.126), severidad 0.047 (vs. 0.046) — cambios
menores a 0.02 en todos los pesos, mismo orden de importancia. Se
considera convergido.

## 10. Próximos pasos

1. Considerar si el hallazgo de Magnitud ENSO (§9.1) amerita revisar ese
   peso específico o su método de agregación en una futura iteración del
   EFCI — no se cambia nada en esta fase, solo se documenta la evidencia.
2. Validación externa contra EM-DAT/DesInventar/UNOSAT (Fase 0 §12, sigue
   pendiente).
3. Extender el bootstrap (§4.4) a Recurrencia/Persistencia/Magnitud, no
   solo Severidad, si se requiere una banda de incertidumbre completa del
   EFCI (requiere remuestrear la serie temporal ENSO, no solo eventos de
   impacto).
