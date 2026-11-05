# 12 — Componente Predictivo del HCI

**Fase:** 12 (extensión, corresponde a Fase 0 §10 "Future Predictive Component")
**Notebook asociado:** `notebooks/Step12_Ecuador_Predictive_Component.ipynb` (ejecutado íntegramente en este entorno, sin dependencias externas)
**Módulo reutilizable:** `src/analisis/prediccion.py`
**Estado:** **completo** — panel construido, validación leave-one-episode-out ejecutada, modelos finales entrenados y exportados
**Audiencia:** científicos, desarrolladores, especialistas DRM/FAO AA

## 1. Objetivo de la fase

Estimar el impacto esperado (población afectada, pérdidas agrícolas, pérdidas de
vivienda) y la probabilidad de severidad alta por cantón **ante un nuevo episodio El
Niño**, entrenando sobre los 6 episodios ENSO documentados en el histórico
2015-2025 — el componente predictivo previsto en el diseño original del proyecto
(Fase 0 §10), no desarrollado hasta ahora.

## 2. Decisiones de diseño confirmadas por Jerson (AskUserQuestion, 2026-08-06)

Antes de escribir código se presentaron tres decisiones abiertas, cada una con
alternativas justificadas, siguiendo la disciplina de diseño-antes-que-código del
proyecto:

1. **Unidad de predicción: cantón × episodio ENSO**, no cantón × mes. Con
   cantón×mes el tamaño muestral nominal sube a ~29,000 filas, pero la mayoría son
   meses sin ningún impacto y, más importante, la estructura de dependencia real no
   cambia — sigue habiendo solo un puñado de eventos climáticos independientes
   agrupados en esos meses. Cantón×episodio es honesto sobre el verdadero tamaño de
   muestra y responde directamente la pregunta operativa: "si viene un Niño fuerte,
   ¿qué esperar en el cantón X?".
2. **Salida dual: regresión de impacto + clasificación de severidad**, no solo una.
   La regresión responde "cuánto" (personas, hectáreas, viviendas); la clasificación
   responde "qué tan probable es que sea severo" — más útil operativamente para
   activar un protocolo de Acción Anticipatoria que un número aislado.
3. **Manejo del tamaño muestral pequeño: modelo simple (Random Forest) + baseline
   explícito**, no un algoritmo más sofisticado (se descartó Bayesian Networks por
   mayor costo de diseño sin garantía de mejor desempeño con tan poco N) ni
   posponer el modelado a futuro. El modelo se reporta siempre junto a un baseline
   ingenuo — la media histórica del propio cantón — para que cualquier ganancia
   reportada sea relativa a "lo que ya sabíamos sin ningún modelo", no a cero.

## 3. Redefinición de episodios ENSO (desviación deliberada de la Fase 11)

La Fase 11 (extracción SAR) usó una lista de "5 episodios" (2015, 2016, 2017, 2023,
2024) para elegir fechas puntuales de Sentinel-1 — una conveniencia de muestreo por
año calendario, no una definición climatológica rigurosa. Para el componente
predictivo, donde el número de episodios independientes determina directamente el
número de folds de validación, esa imprecisión importa: **2015-04 a 2016-06 es un
solo evento El Niño continuo** ("El Niño 2015-16" en la literatura), no dos años
separados. Tratarlo como dos episodios introduciría autocorrelación falsa entre
folds (el "episodio 2016" compartiría la cola del mismo evento climático que el
"episodio 2015").

Se redefinieron los episodios como bloques de meses **contiguos** de categoría ICEN
"El Niño" (`El Niño - Débil/Moderado/Fuerte/Extraordinario`), verificado
programáticamente contra los 38 meses reales del índice ENSO extendido de la Fase 5
(`enso_index_monthly_extended.parquet`, columna `es_evento_enso`) — no una lista
copiada de memoria:

| Episodio | Meses | N meses | N eventos de peligro (4 tipos) | Cantones afectados |
|---|---|---|---|---|
| 2015-2016 | 2015-04 a 2016-06 | 15 | 2,075 | 187 |
| 2017 | 2017-01 a 2017-04 | 4 | 1,557 | 197 |
| 2018-2019 | 2018-11 a 2019-02 | 4 | 528 | 143 |
| 2023 | 2023-03 a 2023-12 | 10 | 2,394 | 201 |
| 2024 | 2024-01 a 2024-03 | 3 | 1,290 | 171 |
| 2025 | 2025-03 a 2025-04 | 2 | 1,763 | 191 |

**Hallazgo importante, verificado antes de continuar:** esto da **6 episodios**, no
5 — incluye dos episodios (2018-2019 y 2025) que la Fase 11 no usó para el muestreo
SAR pero que sí son episodios El Niño reales, con entre 528 y 2,394 eventos de
peligro cada uno (ninguno residual o vacío). Se documenta explícitamente esta
diferencia con la Fase 11 para que no se lea como una inconsistencia entre fases —
son dos definiciones de "episodio" adecuadas a sus propios fines (muestreo SAR
puntual vs. folds de validación independientes).

## 4. Construcción del panel cantón × episodio

Para cada uno de los 6 episodios y cada uno de los 221 cantones (universo completo,
igual convención que Fases 5-9: cantones sin eventos quedan en 0, nunca ausentes):

- `n_eventos`: conteo de eventos de peligro (los 4 tipos del alcance del proyecto)
  en ese cantón durante ese episodio.
- `poblacion_afectada` = `affected_direct + affected_indirect` sumado sobre el
  episodio.
- `agricultura_perdida_ha` = `crops_affected_ha + crops_destroyed_ha` sumado.
- `vivienda_afectada` = `houses_affected + houses_destroyed` sumado.
- `magnitud_enso_media` / `magnitud_enso_max`: promedio y máximo de la magnitud
  ENSO ordinal (escala de la Fase 7: Débil=0.25, Moderado=0.50, Fuerte=0.75,
  Extraordinario=1.00) de los meses del episodio — variable climática, no
  espacial, igual para todos los cantones de un mismo episodio.

**Nota metodológica sobre los targets:** a diferencia del HCI (índice 0-1
normalizado), aquí se predicen **magnitudes crudas** (personas, hectáreas,
viviendas), no un índice relativo — porque un plan de Acción Anticipatoria necesita
"cuántas personas esperar", no "qué tan crónico en una escala relativa". Panel final:
221 × 6 = 1,326 filas, verificado por assert antes de continuar.

## 5. Etiqueta binaria de severidad

Score compuesto = suma de los 3 targets normalizados 0-1 por min-max **global**
(mismo criterio de normalización que Fases 4 y 8, por consistencia metodológica
dentro del proyecto). El percentil 80 entre las filas con score>0 define la clase
"severo" — 166 de 1,326 filas (12.5%), documentado como elección de diseño
explícita, no un valor mágico oculto.

## 6. Features y prevención de fuga de información (leakage)

El paso metodológicamente más delicado de la fase: para cada fold de validación
(donde un episodio se deja fuera como conjunto de prueba), **ninguna feature puede
derivarse de datos de ese mismo episodio**. Se implementó
`construir_features_sin_fuga()`, que recalcula, usando solo los episodios de
entrenamiento (nunca toda la serie):

- `hist_n_episodios_con_evento` / `hist_frac_episodios_con_evento`: en cuántos de
  los episodios de entrenamiento el cantón tuvo al menos un evento.
- `hist_poblacion_media`, `hist_agricultura_media`, `hist_vivienda_media`,
  `hist_n_eventos_medio`: promedio histórico de cada target, excluyendo siempre el
  episodio evaluado.

La magnitud ENSO del episodio objetivo (`magnitud_enso_media`/`max`) SÍ se usa
como feature — no es fuga, porque es una variable climática conocida
independientemente del impacto que se quiere predecir (se sabe que un episodio es
"Fuerte" sin necesidad de observar sus consecuencias).

## 7. Validación: leave-one-episode-out (LOEO)

Por cada uno de los 6 episodios: se recalculan las features (Sección 6) usando solo
los otros 5, se entrena un Random Forest (300 árboles, `min_samples_leaf=3`) —
regresión con transformación `log1p` para los 3 targets de impacto (distribución muy
sesgada con exceso de ceros) y clasificación balanceada (`class_weight="balanced"`,
dado el desbalance ~12.5% positivos) para severidad — y se predice el episodio
dejado fuera. Se compara siempre contra el baseline ingenuo (media histórica del
propio cantón, del mismo paso sin fuga).

### 7.1 Resultados reales — regresión (MAE, métrica principal)

Se prefiere MAE (Error Absoluto Medio) sobre R² como métrica principal: con targets
tan sesgados y con exceso de ceros, R² penaliza fuertemente a cualquier predictor
que no capture los pocos valores extremos, incluso si predice razonablemente bien
la mayoría de los casos — ver §7.3 para el detalle de R².

| Resultado | Valor |
|---|---|
| Combinaciones episodio × target donde el modelo supera al baseline (MAE) | 15 de 18 |
| Reducción media de error (MAE) del modelo vs. baseline | **25.4%** |

El modelo bate al baseline ingenuo en la gran mayoría de combinaciones — reduce el
error absoluto promedio en una cuarta parte respecto de simplemente asumir "este
episodio se parecerá al promedio histórico del cantón". No es una mejora enorme (N=6
folds no da para más certeza), pero es consistente y va en la dirección correcta.

### 7.2 Resultados reales — clasificación de severidad (AUC, F1)

| Métrica | Modelo (promedio) | Baseline (promedio) | Modelo mejor en |
|---|---|---|---|
| AUC | **0.792** | 0.654 | 5 de 6 episodios |
| F1 | **0.344** | 0.237 | 5 de 6 episodios |

Resultado más claro que el de regresión: el modelo de clasificación distingue
sistemáticamente mejor los cantones que tendrán impacto severo que el baseline de
frecuencia histórica, con el mayor margen en los episodios 2024 (AUC 0.88 vs. 0.65)
y 2018-2019 (AUC 0.80 vs. 0.62) — precisamente los episodios más recientes/atípicos,
donde un baseline puramente histórico tiene menos margen para acertar por inercia.

### 7.3 R² — reportado por transparencia, no como métrica principal

| Métrica | Modelo (promedio) | Baseline (promedio) |
|---|---|---|
| R² | -4.19 | -22.91 |

Ambos (modelo y baseline) dan R² negativo en promedio — esperable con targets tan
sesgados y con exceso de ceros, donde ni un buen predictor "explica varianza" en el
sentido clásico de R² cuando la mayoría de los valores reales son cercanos a cero y
unos pocos son extremos. El punto relevante no es que el modelo sea "bueno" en
términos absolutos de R², sino que es **sistemáticamente menos malo que el
baseline** (R² promedio 5.5 veces menos negativo) — coherente con el resultado de
MAE de §7.1, no contradictorio.

## 8. Importancia de features (modelo final)

El modelo final se reentrena con los 6 episodios completos (no está validado fuera
de muestra — para eso está el LOEO de la Sección 7; es el modelo que quedaría listo
para producir una estimación real ante el próximo episodio El Niño). La importancia
de features confirma la intuición del diseño: el historial propio del cantón
(`hist_vivienda_media`, `hist_poblacion_media`, etc.) pesa considerablemente más que
la magnitud ENSO del episodio — coherente con el hallazgo de la Fase 9 de que la
cronicidad está dominada por Recurrencia/Persistencia (procesos sostenidos con firma
geográfica real), no por Magnitud ENSO (variable nacional con poca variación
espacial). Detalle completo en `data/processed/prediccion_importancia_features.csv`.

## 9. Limitaciones (honestas, no minimizadas)

- **N=6 episodios independientes es una base pequeña para cualquier ML
  supervisado.** Las métricas LOEO tienen bandas de incertidumbre amplias — 5/6 o
  15/18 son proporciones informativas pero no estadísticamente concluyentes con tan
  pocos folds. El valor del ejercicio es que el modelo bate consistentemente a un
  baseline razonable, no que sea "preciso" en un sentido absoluto.
- **El episodio 2015-2016, al ser el primero cronológicamente, no tiene ningún
  episodio previo real anterior a 2015 en los datos del proyecto** — sus features
  históricas de fold se calculan igual (usando los otros 5 episodios, que
  cronológicamente son posteriores) porque el diseño LOEO no exige orden temporal
  estricto, pero operativamente, para un episodio verdaderamente nuevo y futuro, sí
  habría historial completo de los 6 episodios disponibles como entrenamiento —
  el modelo final de la Sección 8 sí lo aprovecha todo.
- **R² negativo en ambos (modelo y baseline)** — ver §7.3, es una propiedad de la
  distribución del target, no un fallo del modelo, pero se documenta sin
  maquillarlo.
- **No incluye capas físicas** (lluvia CHIRPS, elevación, uso de suelo) que
  probablemente mejorarían la predicción — quedan como capas opcionales futuras
  (Fase 0 §3), consistente con lo ya señalado como pendiente en el reporte
  ejecutivo de la Fase 10.
- **La capa SAR (Fase 11) no se usó como feature** deliberadamente: se construyó
  usando datos de los propios episodios 2017/2023/2024, así que incluirla causaría
  fuga de información exactamente en esos 3 folds — se documenta la exclusión para
  que no se lea como un descuido.

## 10. Exportación

- `data/processed/prediccion_panel_canton_episodio.{csv,parquet}` — panel completo
  (1,326 filas).
- `data/processed/prediccion_metricas_loeo.csv` — métricas fold por fold (48 filas:
  6 episodios × [3 targets × 2 métricas + severo × 2 métricas]).
- `data/processed/prediccion_predicciones_loeo.csv` — predicciones individuales
  (3,978 filas), para auditar cualquier caso puntual.
- `data/processed/prediccion_importancia_features.csv` — importancia de features
  del modelo final.
- `models/step12_modelos_finales.joblib` — 3 regresores + 1 clasificador,
  entrenados con los 6 episodios completos, listos para producir una estimación
  real ante un nuevo episodio El Niño (no validados individualmente — la validación
  honesta es el LOEO de la Sección 7).

## 11. Próximos pasos posibles

- Reentrenar/actualizar el modelo final cuando se documente un nuevo episodio El
  Niño (séptimo punto de validación real, no solo LOEO retrospectivo).
- Incorporar capas físicas (CHIRPS, DEM) si se decide ampliar el conjunto de
  features.
- Considerar Bayesian Networks o modelos jerárquicos bayesianos si el N de
  episodios crece lo suficiente para justificar el costo de diseño adicional.
- Extender el mismo patrón (panel unidad×episodio + LOEO + baseline explícito) a
  la validación externa (Fase 0 §12) cuando se disponga de fuentes como EM-DAT o
  DesInventar.

## 12. Referencias

- `docs/methodology/05_recurrence_index.md` §4.3 — definición original de
  episodios El Niño (reutilizada y refinada aquí, ver Sección 3).
- `docs/methodology/09_spatial_analysis.md` §hallazgo Recurrencia/Persistencia vs.
  Magnitud ENSO — contexto para la importancia de features observada (Sección 8).
- Breiman, L. (2001). "Random Forests." *Machine Learning*, 45(1), 5-32.
- Scikit-learn `RandomForestRegressor`/`RandomForestClassifier` (v1.7).
