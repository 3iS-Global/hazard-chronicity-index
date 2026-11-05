# 04 — Índice de Severidad

**Fase:** 4 de 10 (ver Fase 0, §9)
**Notebook asociado:** `notebooks/Step4_Ecuador_Severity_Index.ipynb`
**Estado:** implementado y ejecutado — 2026-08-05
**Audiencia:** científicos, desarrolladores, especialistas GIS/DRM

## 1. Objetivo de la fase

Construir el primero de los cuatro índices compuestos del diseño (Fase 0
§9): el Índice de Severidad, que combina el impacto histórico en población,
vivienda, agricultura, ganadería e infraestructura en un solo valor 0-1 por
cantón y por provincia, ponderado según la fórmula original:

```
Severidad = 0.30·Población + 0.25·Vivienda + 0.20·Agricultura
          + 0.15·Ganadería + 0.10·Infraestructura
```

Esta fase **no** calcula el HCI compuesto (eso es Fase 8, cuando se combine
con Recurrencia, Persistencia y Magnitud ENSO).

## 2. Decisiones metodológicas confirmadas antes de programar

Dos decisiones de diseño quedaban abiertas en la Fase 0 (§19.4). Se
presentaron a Jerson con alternativas y trade-offs explícitos, y se
confirmaron (AskUserQuestion, 2026-08-05) antes de escribir código:

### 2.1 Estadístico base: **máximo histórico** (no media ni percentil 90)

**Alternativas consideradas:**
- Media histórica — más estable, pero subestima cantones con eventos raros
  y catastróficos (el mismo patrón que ya se documentó en el cruce con el
  modelo COE de Fase 2 §4.8, donde un solo sismo o erupción domina el
  máximo en 31% de los cantones).
- Percentil 90 — compromiso, pero inestable en cantones con pocos eventos
  por tipo de peligro (Fase 3 §7: 58-73% de los cantones tienen
  `datos_insuficientes` en la tendencia de `scour`/`debris_flow` por bajo
  conteo de eventos — el mismo problema de tamaño de muestra afectaría un
  percentil).
- **Máximo histórico (elegido):** coherente con el propósito del índice —
  Acción Anticipatoria se activa antes del peor escenario esperable, no del
  promedio — y es el mismo estadístico que ya usa el modelo COE existente
  en el workbook (`MAX(PERSONAS AFECTADAS DIRECTAMENTE)`, Fase 2 §4.8),
  facilitando comparabilidad futura.

### 2.2 Normalización: **min-max** (no z-score ni percentil/rango)

**Elegida** por interpretabilidad directa (0 = mínimo nacional observado,
1 = máximo nacional observado) y por ser coherente con los umbrales
50/100/150% del modelo COE existente, que también se basan en el máximo
histórico como referencia 100%. **Riesgo aceptado explícitamente:** min-max
es sensible a valores atípicos extremos — ver §6 "Riesgos metodológicos",
donde se documentan dos casos reales encontrados en los datos que
materializan este riesgo, no solo en teoría.

## 3. Fundamento científico

El uso de máximo + min-max replica la lógica de los "worst-case scenario
indices" ya usados en los proyectos de Acción Anticipatoria de referencia
(Fase 0 §19.3) y es metodológicamente consistente con el propio modelo COE
del workbook — no se introduce un criterio nuevo sin precedente en el
contexto del proyecto.

## 4. Decisiones metodológicas adicionales y su justificación

### 4.1 Puntajes compuestos por pilar, calculados a nivel de evento antes de agregar

Cada pilar no es una sola variable de `hazard_event_geo`, sino una
combinación ponderada, calculada evento por evento:

| Pilar | Fórmula (por evento) | Peso "destruido"/"muerto" y por qué |
|---|---|---|
| Población | `affected_direct + affected_indirect + evacuated + sheltered + 10·(deaths + missing_persons) + 5·injured` | Muertos/desaparecidos pesan 10x y heridos 5x frente a "afectado directo" — no estaba en la fórmula original de Fase 0 (que solo nombraba los 5 pilares agregados), pero excluir la mortalidad trataría una muerte igual que una persona "afectada", lo cual no es defendible para un índice de severidad. **Decisión explícita, no implícita en el diseño original — señalada aquí para que Jerson pueda ajustarla.** |
| Vivienda | `houses_affected + 2·houses_destroyed` | Pérdida total pesa el doble que pérdida parcial. |
| Agricultura | `crops_affected_ha + 2·crops_destroyed_ha` | Ídem. |
| Ganadería | `livestock_affected + 2·livestock_deaths` | La muerte del animal es el equivalente de "destruido" en este pilar. |
| Infraestructura | `(schools_affected + 2·schools_destroyed) + (health_facilities_affected + 2·health_facilities_destroyed)` | Escuelas y salud se combinan en un puntaje crudo único antes de normalizar — más simple que normalizar cada una por separado y promediar, y el resultado final igual queda en escala 0-1. |

El multiplicador `2.0` ("destruido" vs. "afectado") y `10.0`/`5.0`
(muerto-desaparecido / herido vs. "afectado directo") están en
`config.yaml` (`severity_index.destroyed_weight_multiplier`,
`death_weight_multiplier`, `injured_weight_multiplier`), no hardcodeados en
el notebook — quedan disponibles para el análisis de sensibilidad que la
Fase 0 (§9) ya pedía antes de fijar el HCI compuesto.

### 4.2 Normalización independiente por vista (`hazard_type` y nivel administrativo)

El min-max de cada pilar se calcula por separado dentro de cada valor de
`hazard_type` (incluida la fila combinada `"TODOS"`) y por separado para
cantón y provincia — nunca se mezcla el rango de una vista desglosada por
peligro con el de la vista combinada, ni el rango cantonal con el
provincial. Comparar, por ejemplo, el `norm_poblacion` de un cantón en la
vista `flood` contra el máximo nacional de *esa* vista, no contra el máximo
combinado de los 4 peligros.

**Caso borde documentado:** si todos los cantones de una vista tienen el
mismo valor en un pilar (rango = 0), el puntaje normalizado se define como
0 para todos — sin variación, no hay información de severidad relativa que
aportar.

### 4.3 Clasificación por cuantiles: provisional, no es la clasificación final del HCI

Se incluye una clasificación de 5 categorías (Muy Baja a Muy Alta) por
cuantiles sobre `severity_index`, solo dentro de la vista `"TODOS"`, para
interpretación inmediata. **No debe leerse como el resultado final del
proyecto** — la clasificación oficial del HCI compuesto (Fase 0 §7:
cuantiles, quiebres naturales o percentiles, a decidir con análisis de
sensibilidad) se define en la Fase 8, sobre el índice compuesto final, no
sobre un componente individual.

## 5. Esquema de salida

Dos tablas, en `data/processed/` (Parquet + CSV):

- `severity_index_canton` (927 filas: 221 cantones × hasta 5 vistas de
  `hazard_type` cada uno, incluida `"TODOS"`).
- `severity_index_provincia` (116 filas, mismo patrón, 24 provincias).

Columnas: `province_code`, `province_name_official`, `canton_code`,
`canton_name_official` (solo en la tabla de cantón), `hazard_type`,
`n_eventos`, `score_<pilar>` (puntaje crudo, máximo histórico),
`norm_<pilar>` (normalizado 0-1), `severity_index` (0-1),
`clase_severidad` (solo en filas `hazard_type == "TODOS"`).

## 6. Riesgos metodológicos — sensibilidad de min-max a valores atípicos (hallazgo real, no hipotético)

La Fase 0 (§15) pedía identificar riesgos metodológicos explícitamente.
Este análisis encontró dos casos concretos donde un solo evento domina el
máximo nacional de un pilar, lo cual **materializa** el riesgo teórico de
usar min-max:

- **Población:** el máximo nacional de `score_poblacion` (750,000) proviene
  de un único evento de deslizamiento en Quito (2022-06-07), con
  `affected_indirect = 750,000` y `affected_direct = 0`. **Verificado
  2026-08-06** contra la descripción completa SNGRE del evento: el
  deslizamiento tapó el canal de ingreso de agua cruda a la planta de
  tratamiento de Puengasí, que abastece los sectores Centro y Sur del DMQ
  (área metropolitana de ~2.8 millones de habitantes) — 750,000 personas
  con servicio de agua suspendido durante varios días es una cifra alta
  pero **plausible y consistente** con la descripción del evento. Se
  mantiene el valor sin modificar.
- **Ganadería — CORREGIDO 2026-08-06:** el máximo nacional de
  `score_ganaderia` provenía de `livestock_deaths = 500,000` en un evento
  de flujo de escombros en Baños de Agua Santa (2021-09-05). Verificado
  contra la descripción SNGRE (extensa, no menciona ninguna cifra de
  animales muertos) y contra prensa independiente (El Comercio, El
  Universo, La Hora — documentan el evento sin mencionar pérdida de
  ganado) — confirmado como **error de captura**, no un dato real (la
  misma fila traía `ANIMALES AFECTADOS = 0`, inconsistente con 500,000
  muertos). Corregido a 0 en el origen (Fase 1 §4.6) y toda la cadena
  Step1→Step8 re-ejecutada. Ver `docs/methodology/01_data_ingestion.md`
  §4.6 y `08_hci_composite.md` §5.3 para el detalle completo de la
  verificación y la corrección.

**Consecuencia visible en el ranking (post-corrección):** Chone (Manabí)
sigue encabezando el `severity_index` nacional (0.530) por alcanzar el
máximo nacional en Vivienda y Agricultura (pesos combinados 0.45) — sin
cambios, porque Chone no dependía del valor corregido. Quito (segundo
lugar, 0.365) sigue dependiendo del pilar Población — ese valor se
verificó y se mantiene. El cambio real es en **Baños de Agua Santa**: su
`severity_index` baja de 0.160 a 0.026 (salió del top 10 nacional) al
perder el `norm_ganaderia = 1.0` que dependía del dato erróneo — un
resultado mucho más consistente con la magnitud real del evento (grave en
términos humanos, 3 fallecidos, pero geográficamente acotado a un sector
rural).

**Por qué Población (Quito) no se corrigió y Ganadería (Baños) sí:** la
diferencia no es el tamaño del número, es la evidencia. El valor de Quito
tiene una explicación causal específica y verificable en la propia
descripción del evento (corte de agua potable a escala de ciudad); el de
Baños no tiene ninguna mención equivalente y es además internamente
inconsistente con otra columna de la misma fila. "Corregir solo cuando hay
evidencia, no por sospecha de magnitud" es el criterio aplicado en ambos
casos, con resultados distintos.

## 7. Limitaciones

- El índice de esta fase **no está validado por sensibilidad** — los pesos
  de pilar (0.30/0.25/0.20/0.15/0.10) y los multiplicadores internos
  (`destroyed`, `death`, `injured`) son los propuestos en el diseño
  original más las extensiones documentadas en §4.1, pendientes de la
  validación de sensibilidad que la Fase 0 (§9) ya exige antes de fijar el
  HCI compuesto.
- Sensibilidad a valores atípicos por min-max — ver §6, con dos casos reales
  ya identificados.
- El puntaje de Infraestructura combina escuelas y salud en una sola cifra
  cruda antes de normalizar, no pondera cada subsector por separado — un
  cantón con muchas escuelas afectadas pero ningún centro de salud afectado
  puntúa igual que uno con la combinación inversa de magnitud equivalente.
- La clasificación por cuantiles (§4.3) fuerza grupos de tamaño similar
  (~44 cantones cada uno) incluso si la distribución real de severidad no
  es uniforme — es una limitación conocida de la clasificación por
  cuantiles frente a quiebres naturales (Fase 0 §7), a resolver en Fase 8.

## 8. Supuestos

- Se asume que los valores extremos identificados en §6 son datos válidos
  de SNGRE (no errores de captura) hasta que se verifique lo contrario — no
  se descartaron ni se limitó su magnitud.
- Se asume que combinar escuelas y salud en un solo puntaje de
  Infraestructura (§7) es una aproximación aceptable para esta fase; Fase 0
  no especifica si deben tratarse por separado.

## 9. Ventajas del enfoque

- Todos los pesos y multiplicadores viven en `config.yaml`
  (`severity_index`), no hardcodeados — listos para el análisis de
  sensibilidad de Fase 8 sin tocar el notebook.
- El notebook expone el puntaje crudo (`score_<pilar>`) junto al normalizado
  (`norm_<pilar>`) — permite auditar cualquier resultado extremo hasta el
  evento de origen, como se hizo en §6.
- Validación explícita antes de exportar: cobertura completa de 221
  cantones y 24 provincias, `severity_index` siempre en [0,1], sin nulos.

## 10. Posibles mejoras futuras

- Verificar contra el reporte SNGRE original los dos valores atípicos de §6
  (evento Quito 2022-06-07, evento Baños de Agua Santa 2021-09-05).
- Evaluar winsorización u otra normalización robusta a outliers como
  alternativa al min-max puro, dentro del análisis de sensibilidad previo a
  Fase 8.
- Ponderar escuelas y salud por separado dentro de Infraestructura si Fase
  0 o Jerson lo consideran necesario.

## 11. Referencias

- Fase 0 — Diseño Conceptual HCI Ecuador, §9 (fórmula de Severidad), §15
  (riesgos metodológicos).
- `docs/methodology/02_spatial_integration.md` §4.8 (metodología del modelo
  COE, precedente del uso de máximo histórico).
- `docs/methodology/03_historical_analysis.md` (insumo de recuento de
  eventos por cantón/provincia).
