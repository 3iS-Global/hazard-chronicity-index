# 04 — Índice de Severidad (resumen ejecutivo)

**Fase 4 de 10 del proyecto EFCI Ecuador — completada el 5 de agosto de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

La Fase 3 dejó cifras separadas por cada tipo de impacto (personas
afectadas, viviendas, cultivos, ganado, escuelas, centros de salud). Pero
para poder comparar la gravedad histórica entre cantones y priorizar dónde
actuar primero, se necesita un solo número que combine todo eso de forma
razonada. Esta fase construye ese número: el Índice de Severidad, en una
escala de 0 a 1 para cada cantón y cada provincia.

## ¿Qué se hizo?

1. **Se combinaron los distintos tipos de daño en cinco categorías**:
   población, vivienda, agricultura, ganadería e infraestructura (escuelas
   y salud) — dentro de cada categoría, una pérdida total (p. ej. una
   vivienda destruida) pesa más que una pérdida parcial (una vivienda solo
   dañada).

2. **Se tomó el peor caso histórico de cada cantón en cada categoría**, no
   el promedio — decisión confirmada contigo antes de programar, porque el
   propósito de este índice es anticipar el peor escenario esperable, no
   describir un día típico.

3. **Se llevó cada categoría a una escala común de 0 a 1**, comparando cada
   cantón contra el peor caso registrado en todo el país.

4. **Se combinaron las cinco categorías en un solo índice**, con los pesos
   ya definidos en el diseño del proyecto: población 30%, vivienda 25%,
   agricultura 20%, ganadería 15%, infraestructura 10%.

## ¿Qué encontramos?

- El cantón con mayor Índice de Severidad histórica es **Chone** (Manabí),
  seguido del **Distrito Metropolitano de Quito**. Pero llegan ahí por
  razones muy distintas: Chone alcanza el peor caso nacional en vivienda Y
  en agricultura al mismo tiempo; Quito depende casi por completo de un
  único evento con un número muy alto de personas afectadas
  indirectamente, y es prácticamente irrelevante en las otras cuatro
  categorías.
- A nivel provincia, Manabí encabeza el ranking, seguida de Pichincha y
  Guayas.

## Un hallazgo importante — y cómo se resolvió (actualizado 2026-08-06)

Al revisar de dónde salían los valores más extremos, se encontraron dos
casos puntuales: un evento en Quito (junio de 2022) con 750,000 personas
reportadas como afectadas indirectamente, y un evento en Baños de Agua
Santa (septiembre de 2021) con 500,000 animales reportados como muertos.

Ya se verificaron ambos contra el reporte original de SNGRE (y, en el caso
de Baños, también contra prensa independiente):

- **Quito: el valor se sostiene.** La descripción del evento explica que un
  deslizamiento cortó el agua potable a gran parte de la ciudad durante
  varios días — 750,000 personas afectadas indirectamente es una cifra
  alta pero coherente con esa magnitud de corte de servicio en una ciudad
  de casi 3 millones de habitantes. Se mantiene sin cambios.
- **Baños de Agua Santa: era un error de captura.** El reporte SNGRE del
  evento es extenso y no menciona en ningún momento una cifra de animales
  muertos; además, la misma fila del Excel decía "0 animales afectados" y
  "500,000 animales muertos" al mismo tiempo, algo imposible. Tres medios
  de prensa distintos documentaron el evento (3 personas fallecidas,
  pérdidas estimadas en 600,000 dólares) sin mencionar pérdida de ganado.
  Se corrigió el valor a 0 y se volvió a calcular todo el índice — el
  puntaje de Severidad de ese cantón bajó de 0.16 a 0.03, un resultado
  mucho más acorde con lo que realmente ocurrió ahí.

Este es exactamente el tipo de cosa que el proyecto está diseñado para
sacar a la luz: no se corrigió nada por sospecha, se verificó primero, y
solo se cambió lo que la evidencia respaldaba.

## ¿Cómo contribuye esto al objetivo final?

El Índice de Severidad es uno de los cuatro ingredientes del EFCI final
(los otros son Recurrencia, Persistencia y Magnitud de El Niño, que vienen
en las próximas fases). Con esta pieza lista, el proyecto ya tiene una
respuesta cuantitativa y comparable a "¿qué tan grave ha sido el impacto
histórico en cada cantón?" — la primera de las preguntas centrales del
proyecto (ver visión del proyecto).

## ¿Qué falta?

- Fase 5: Índice de Recurrencia (con qué frecuencia, relativo a los
  episodios de El Niño documentados).
- Fase 6: Índice de Persistencia (cuánto duran los episodios de afectación).
- Fase 7: Índice de Magnitud de El Niño.
- Antes de dar por definitivos los pesos usados aquí: un análisis de
  sensibilidad (ya previsto en el diseño original) que pruebe si el
  ranking cambia mucho al ajustar los pesos o el método de normalización —
  particularmente relevante después del hallazgo de la sección anterior.
