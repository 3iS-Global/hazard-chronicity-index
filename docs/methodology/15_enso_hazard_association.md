# 15 — Asociación estadística El Niño–amenaza: ajuste por estacionalidad, dosis-respuesta, región y tipo de peligro

**Fase:** 15 (nueva — surge del feedback de revisión externa del 2026-10-06,
D. Arteaga, oficial de enlace: los eventos de Chone y Quito "no todos se
asocian con ENOS", son de origen estacional o de influencia amazónica; el
análisis supone que la precipitación andina podría aumentar, algo que
INAMHI indica que no ocurriría)
**Módulo:** `src/analisis/asociacion_enso.py` · **Tests:** `tests/test_asociacion_enso.py` (9, todos pasan)
**Config:** `config/config.yaml`, sección `enso_association`
**Salidas:** `data/processed/enso_asociacion_{irr,dosis,rezagos,diag,loeo,bootstrap,heterogeneidad}.{parquet,csv}`,
`outputs/tables/fase15_irr_resumen.csv`, `outputs/figures/fase15_forest_irr.png`
**Estado:** implementado y ejecutado — 2026-10-06
**Audiencia:** científicos, desarrolladores, especialistas en observación de la Tierra y DRM/FAO AA
**Documento ejecutivo:** `docs/executive/15_enso_hazard_association.md`

## 1. Objetivo de la fase

Poner a prueba, con un modelo estadístico adecuado, la premisa que justifica
todo el diseño del HCI (Fase 0, H1): *los eventos ocurren con mayor
frecuencia durante episodios El Niño.* Hasta esta fase la evidencia era
(i) una razón cruda nacional de 1.96x (Fase 5 §4.4), (ii) conteos por
categoría ENSO sin normalizar por el número de meses de cada categoría
(Fase 3 §4.4) y (iii) un índice de magnitud ENSO construido por
construcción, no contrastado contra los eventos (Fase 7).

Preguntas que esta fase responde:

1. ¿Persiste la asociación El Niño–eventos al descontar estacionalidad y la
   tendencia de reporte, o la razón cruda de 1.96x es en buena parte un
   artefacto del calendario?
2. ¿Hay **gradiente por magnitud** (Débil < Moderado < Fuerte)? Es lo que
   justifica dar peso a la componente Magnitud ENSO (15 %).
3. ¿La asociación es homogénea entre **regiones** (Costa, Sierra, Oriente)?
4. ¿Es homogénea entre **amenazas** (inundación, deslizamiento,
   socavamiento, aluvión)?
5. ¿Qué tan robusto es el resultado a la definición de ENSO (ICEN vs ONI), a
   la forma de modelar la estacionalidad, a rezagos y a la exclusión de
   episodios individuales?

## 2. Fundamento científico

**Física del problema.** El Niño modifica la precipitación sobre Ecuador de
forma espacialmente heterogénea: la señal más robusta en la literatura se
asocia a la franja costera, donde el calentamiento anómalo del Pacífico
oriental (región Niño 1+2, base del ICEN) intensifica la convección y las
lluvias de la estación húmeda; en los Andes la relación es más débil y
depende de la interacción con el Atlántico tropical y la circulación
amazónica; en el Oriente la señal es ambigua (Vuille et al. 2000; Rossel &
Cadier 2009). Un análisis nacional agregado mezcla regímenes físicos
distintos y debe, por tanto, estratificarse.

**Confusión por estacionalidad.** La temporada de lluvias (aprox.
enero–mayo) concentra la mayoría de los eventos y, a la vez, es cuando
suelen culminar los episodios El Niño. Comparar tasas de eventos entre meses
El Niño y no El Niño sin descontar el mes calendario infla la asociación si
los episodios caen en temporada húmeda y la deflacta si caen fuera de ella.
Es exactamente el problema que subyace a la razón cruda de 1.96x.

**Tendencia de reporte.** Las bases SNGRE/ECU911 reflejan también cambios de
cobertura y de sistema de reporte en 2015–2025; sin un término de tendencia,
episodios tardíos (2023–25) quedan sobrerrepresentados.

## 3. Fundamento estadístico

**Unidad y respuesta.** Conteo mensual de eventos por estrato (132 meses,
2015-01 a 2025-12). Los meses sin eventos se conservan como ceros (principio
de Fase 1: nada se descarta silenciosamente).

**Modelo.** Regresión Binomial Negativa de tipo NB2 con enlace log:

`log E[n_t] = β0 + β_ENSO · ENSO_t + Σ_m γ_m · 1(mes=m) + δ · t + log(exposición = 1)`

* Poisson se descarta: la dispersión estimada es α = 0.15–0.55 según estrato
  (varianza ≫ media). NB2 modela `Var = μ + αμ²`.
* `γ_m` (efectos fijos de mes calendario, 11 términos) absorben la
  estacionalidad sin imponer forma funcional; `δ` (tendencia lineal sobre
  tiempo estandarizado) absorbe el crecimiento del reporte.
* El coeficiente de interés se reporta como **razón de tasas (IRR)**
  `exp(β_ENSO)`: factor multiplicativo de la tasa mensual de eventos durante
  El Niño, a mes calendario y tendencia fijos.

**Definición de ENSO.** Mes El Niño = categoría ICEN "El Niño" de cualquier
magnitud (38 meses; Fase 5 §4.3). ONI se usa solo como sensibilidad: ICEN es
un índice costero, coherente con la geografía del problema.

**Inferencia.** Errores estándar HAC de Newey-West (3 rezagos) porque los
residuos presentan autocorrelación (Ljung-Box lag 12, p < 0.05 en 10 de 18
estratos). Como verificación independiente: bootstrap por bloques móviles
(bloque = 6 meses, B = 1000, semilla fija). Pruebas múltiples: corrección
Benjamini-Hochberg (FDR 5 %) sobre la familia de los 18 estratos del modelo
primario.

**Gradiente por magnitud.** Dos especificaciones: (a) categórica (La Niña,
Débil, Moderado, Fuerte vs. Neutro) y (b) ordinal (indicador El Niño +
pendiente lineal por categoría Débil=0, Moderado=1, Fuerte=2). La pendiente
ordinal es la prueba más potente de un gradiente monótono.

**Heterogeneidad regional.** Prueba de razón de verosimilitud entre un modelo
con un efecto ENSO común y otro con efecto por región (estacionalidad y
tendencia propias de cada región en ambos).

**Robustez.** (S1) ONI en lugar de ICEN; (S2) estacionalidad armónica
(2 armónicos) en lugar de efectos fijos de mes; (S3) efectos fijos de año en
lugar de tendencia lineal; (S4) ICEN continuo; rezagos 0–3 meses;
leave-one-episode-out (LOEO).

## 4. Decisiones metodológicas (el *por qué*)

| Decisión | Alternativa descartada | Razón |
|---|---|---|
| NB2 mensual | Poisson; OLS sobre log-tasas | Sobredispersión fuerte; OLS no maneja ceros |
| Efectos fijos de mes | Armónicos (se dejan como sensibilidad) | Sin supuesto de forma; solo 11 parámetros sobre 132 meses |
| Tendencia lineal | Efectos fijos de año como primario | Los efectos de año absorben parte de la variación *entre episodios* (que es la señal de interés); se dejan como sensibilidad conservadora |
| ICEN como ENSO primario | ONI | ICEN es el índice costero y ya define el "evento ENSO" desde la Fase 5 |
| Rezago 0 como primario | Elegir el rezago por AIC | El AIC entre rezagos **no es comparable**: cada rezago elimina meses distintos y cambia *n*; se reporta el IRR de cada rezago pero no se selecciona por AIC |
| HAC + bootstrap por bloques | Solo errores clásicos | Autocorrelación residual documentada |
| Galápagos excluido de los estratos regionales | Incluirlo | Solo 26 eventos; sin poder estadístico (sí cuenta en el estrato Nacional) |
| Estratos región × amenaza con ≥ 200 eventos | Todos | Con menos eventos el modelo no es estable (Costa y Oriente × aluvión omitidos: 86 y 148) |

## 5. Resultados

### 5.1 La razón cruda de 1.96x se reduce a 1.41x al ajustar, y esconde un contraste regional fuerte

Modelo primario (ICEN binario, IC 95 % HAC; BH = significativo tras corrección):

| Estrato | Eventos | IRR crudo | **IRR ajustado** | IC 95 % | BH |
|---|---|---|---|---|---|
| Nacional | 21,743 | 1.96 | **1.41** | 1.17–1.70 | sí |
| Costa | 7,281 | 3.38 | **3.45** | 2.51–4.73 | sí |
| Sierra | 10,363 | 1.62 | **1.15** | 0.91–1.46 | no |
| Oriente | 4,073 | 1.14 | **1.09** | 0.87–1.36 | no |
| Inundación | 7,281 | 2.81 | **2.02** | 1.57–2.61 | sí |
| Deslizamiento | 12,625 | 1.65 | **1.21** | 0.99–1.47 | no (p=0.067) |
| Socavamiento | 1,152 | 1.99 | **1.63** | 1.34–1.97 | sí |
| Aluvión | 685 | 0.79 | **0.46** | 0.31–0.70 | sí (**efecto inverso**) |

Los intervalos del bootstrap por bloques coinciden con los HAC (Nacional
1.16–1.77; Costa 2.08–4.94; Sierra 0.91–1.53; Oriente 0.85–1.48; Aluvión
0.24–0.71), de modo que las conclusiones no dependen del estimador de la
varianza.

La prueba LR de heterogeneidad regional rechaza fuertemente un efecto común
(χ² = 62.4, g.l. = 2, p ≈ 3·10⁻¹⁴): **la asociación con El Niño es
estadísticamente distinta entre Costa, Sierra y Oriente.**

Estratos región × amenaza (solo se listan los de mayor interés):

| Estrato | IRR | IC 95 % | BH |
|---|---|---|---|
| Costa × inundación | 5.34 | 3.55–8.03 | sí |
| Costa × socavamiento | 2.88 | 2.06–4.01 | sí |
| Costa × deslizamiento | 1.91 | 1.42–2.58 | sí |
| Sierra × aluvión | 0.47 | 0.30–0.73 | sí (inverso) |
| Sierra × inundación | 1.33 | 0.96–1.85 | no |
| Sierra × deslizamiento | 1.15 | 0.91–1.46 | no |
| Oriente × inundación | 1.00 | 0.73–1.37 | no |
| Oriente × deslizamiento | 1.11 | 0.88–1.39 | no |

### 5.2 No hay gradiente monótono por magnitud a escala nacional

IRR por categoría ICEN (referencia: Neutro):

| Estrato | Débil | Moderado | Fuerte | Pendiente por categoría (IRR, p) |
|---|---|---|---|---|
| Nacional | 1.39 | 1.40 | 1.24 | 0.95 (p = 0.53) |
| Costa | 1.79 | 3.22 | 5.12 | **1.67 (p < 0.001)** |
| Sierra | 1.19 | 1.21 | 1.05 | 0.95 (p = 0.62) |
| Oriente | 1.28 | 0.82 | 0.76 | 0.75 (p = 0.005, decreciente) |
| Inundación | 1.51 | 2.28 | 1.83 | 1.12 (p = 0.34) |

Solo la Costa muestra un gradiente claro (Fuerte = 5.12, IC 3.51–7.46).
Nacionalmente, "Fuerte" no supera a "Débil" ni a "Moderado". Con ONI el
IRR nacional cae a 1.07 (S1), lo que indica que el efecto depende de la
definición costera del evento.

### 5.3 Robustez

* **LOEO (5 bloques contiguos ICEN; ver §7.3):** IRR nacional 1.37–1.49,
  siempre significativo; Costa 2.59–3.68 (el mínimo al excluir 2023-03 a
  2024-03); Aluvión 0.38–0.57. Sierra 1.10–1.27, no significativo en
  ninguna exclusión. Matiz: Oriente (IRR 1.33, p = 0.01) y deslizamiento
  (1.37, p < 0.01) pasan a ser significativos **solo** al excluir el
  episodio 2023-03 a 2024-03, que por tanto atenúa la señal en esos
  estratos (el episodio 2023-24 se asoció con menos eventos adicionales de
  lo que predicen los demás). Ningún episodio individual domina las
  conclusiones principales (Nacional, Costa, inundación, aluvión).
* **Estacionalidad armónica (S2):** prácticamente idéntica al primario
  (Nacional 1.42; Costa 3.31).
* **Efectos fijos de año (S3):** atenúa el efecto (Costa 2.20) porque
  absorbe variación entre episodios; es una cota conservadora, no un modelo
  mejor.
* **Rezagos 0–3:** el IRR decrece con el rezago en Costa (3.45 → 2.45) y
  en inundación (2.02 → 1.47); no hay evidencia de un máximo rezagado.
* **Diagnósticos:** todos los ajustes convergieron; α entre 0.15 y 0.55;
  autocorrelación residual remanente (Ljung-Box p < 0.05) en 10 de 18
  estratos, entre ellos Nacional, Sierra, Oriente, deslizamiento,
  inundación y aluvión → justifica HAC y bootstrap por bloques.

## 6. Implicaciones para el HCI y decisiones abiertas

Esta fase **no modifica** el HCI; documenta evidencia que obliga a decisiones
explícitas del equipo (flujo de trabajo del proyecto: discutir antes de
cambiar la fórmula):

1. **Interpretación del índice fuera de la Costa.** En Sierra y Oriente el
   HCI mide cronicidad de eventos hidrometeorológicos, pero la evidencia
   no respalda atribuirla a El Niño. El uso para activación anticipatoria
   ante un episodio El Niño es defendible en la Costa y para inundación y
   socavamiento; no lo es, con estos datos, para la Sierra ni el Oriente.
   Acción mínima: una **etiqueta de "señal ENSO regional"** (fuerte / débil /
   no detectable) por cantón en el dashboard y los perfiles.
2. **Aluvión (HCI).** La asociación es inversa (IRR 0.46): hay menos
   aluviones por mes durante El Niño. El HCI debe presentarse como
   cronicidad del peligro, no como cronicidad *asociada a ENSO*.
3. **Componente Magnitud ENSO (15 %).** Sin gradiente por magnitud a escala
   nacional y con ese componente ya identificado como el más influyente en
   la inestabilidad de la clasificación (Fase 13, Sobol), conviene evaluar
   (a) mantenerlo, (b) un peso regional (solo Costa) o (c) reducirlo. No se
   decide aquí.
4. **Denominador de Recurrencia (Fase 5).** "Meses con evento / meses El
   Niño" mide intensidad de reporte en meses El Niño, no atribuibilidad;
   debe leerse con el IRR regional.

## 7. Limitaciones y supuestos

1. **Pocos episodios independientes.** Solo 5 bloques contiguos (6 según
   Fase 12). Los IC reflejan variación mensual dentro del período, no la
   incertidumbre de generalizar a episodios futuros. Es la limitación
   dominante y ningún método la elimina.
2. **Asociación, no causalidad.** El modelo estima asociación condicional a
   mes calendario y tendencia. No separa lluvia de exposición, vulnerabilidad
   ni cambios de reporte.
3. **Inconsistencia a reconciliar con la Fase 12.** `prediccion.py` define 6
   episodios separando "2023" (2023-03 a 2023-12) y "2024" (2024-01 a
   2024-03); estos meses son contiguos en el índice ICEN, por lo que bajo
   contigüidad estricta forman **un solo** episodio (5 en total). Esta fase
   usa contigüidad estricta. Se recomienda revisar si la Fase 12 debe
   unificarlos (afecta N de la validación LOEO de esa fase).
4. **Series de eventos = reportes.** El conteo depende de la capacidad de
   reporte, que varía por región; la tendencia lineal es una aproximación.
5. **Sin variable climática directa.** No se usa lluvia observada (CHIRPS,
   estaciones INAMHI). Es la mejora más importante (§9).
6. **Autocorrelación residual** persiste pese a HAC; los IC son aproximados.
7. **Referencias a verificar** antes de uso en publicación: Vuille, Bradley &
   Keimig (2000, *J. Climate*); Rossel & Cadier (2009, *Hydrol. Process.*);
   Cameron & Trivedi (2013, *Regression Analysis of Count Data*); Newey &
   West (1987, *Econometrica*); Benjamini & Hochberg (1995, *JRSS-B*);
   Künsch (1989, *Ann. Stat.*).

## 8. Ventajas del enfoque

* Separa explícitamente estacionalidad, tendencia y señal ENSO; la razón
  cruda se transforma en un efecto interpretable.
* Cubre dosis-respuesta, región, amenaza, definición de ENSO, rezagos y
  exclusión de episodios; reporta todos los resultados, incluidos los
  desfavorables a la hipótesis original.
* Totalmente reproducible: parámetros en YAML, semilla fija, 9 pruebas
  unitarias con datos sintéticos de efecto conocido (recuperación de IRR = 2,
  falsos positivos con IRR = 1, control de estacionalidad).

## 9. Mejoras futuras

1. Sustituir o complementar el índice ENSO por **precipitación observada**
   (CHIRPS/estaciones INAMHI) como mediador: ENSO → lluvia → eventos.
2. Modelos jerárquicos bayesianos por cantón con contracción hacia la región.
3. Incorporar SST Niño 3.4 y la covariable de Atlántico tropical para la Sierra.
4. Análisis de episodios individuales con control sintético o comparación de
   episodios de magnitud similar.
5. Reconciliar la definición de episodios (Fases 5, 11, 12 y 15).
6. Incorporar el aviso de metodología al dashboard (texto en el documento
   ejecutivo, §"Texto del aviso").

## 10. Reproducción

```
python -m pytest tests/test_asociacion_enso.py
python -c "import yaml,pandas as pd; from src.analisis import asociacion_enso as ae; \
cfg=yaml.safe_load(open('config/config.yaml',encoding='utf-8'))['enso_association']; \
r=ae.run_analysis(pd.read_parquet('data/processed/hazard_event.parquet'), \
pd.read_parquet('data/processed/enso_index_monthly_extended.parquet'), cfg); \
ae.export_tables(r, cfg['salida_dir'])"
```

Tiempo de ejecución ≈ 1 minuto. Dependencias nuevas: `statsmodels>=0.14`,
`pytest>=8` (añadidas a `requirements.txt`).


## Addendum: implementación de las decisiones de comunicación (6 oct 2026)

- **Limitación adicional (asignación regional):** la región (Costa/Sierra/Oriente) se asigna a nivel de provincia. Cantones de transición climática (p. ej. Puerto Quito, Pedro Vicente Maldonado, La Maná, La Troncal, Zapotillo) pueden quedar mal clasificados; la etiqueta de señal por cantón hereda este error.
- **Etiquetas por cantón:** `data/processed/enso_senal_canton.{parquet,csv}` (función `classify_signal`, umbrales en `config.yaml`: ≥2.0 Fuerte, ≥1.2 Moderada, <1 Inversa, no significativo = No detectable).
- **Aviso en el dashboard:** `src/exportacion/aviso_metodologico.py` inyecta de forma idempotente un aviso colapsable, con cifras leídas de los resultados, en los 4 HTML (atlas y dashboard).
- **Infografía:** `outputs/figures/HCI_Infografia_Metodologia.png`.
