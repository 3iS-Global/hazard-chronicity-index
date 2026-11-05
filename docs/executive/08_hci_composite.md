# 08 — El índice HCI completo (resumen ejecutivo)

**Fase 8 de 10 del proyecto HCI Ecuador — completada el 5 de agosto de 2026, actualizada el 6 y el 17 de agosto de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

Esta es la fase donde los cuatro ingredientes construidos hasta ahora
(Severidad, Recurrencia, Persistencia, Magnitud de El Niño) se combinan por
primera vez en un solo número: el HCI, el índice de cronicidad de
inundaciones por El Niño para cada cantón y provincia de Ecuador. También
es la fase donde se pone a prueba qué tan confiable es ese número —no basta
con calcularlo una vez, hay que comprobar si cambia mucho según pequeñas
decisiones metodológicas.

## ¿Qué se hizo?

1. **Se combinaron los cuatro índices** con la fórmula que se definió desde
   el diseño original del proyecto: 35% Recurrencia, 30% Severidad, 20%
   Persistencia, 15% Magnitud de El Niño.

2. **Se clasificó cada cantón y provincia** en 5 categorías (de Muy Baja a
   Muy Alta cronicidad), usando el método de "quiebres naturales" que
   confirmaste — agrupa según cómo se distribuyen realmente los datos, no
   forzando grupos del mismo tamaño.

3. **Se pusieron a prueba cuatro decisiones pendientes** que quedaron
   abiertas en fases anteriores, cada una con una comparación real, no
   solo teórica: qué versión de Magnitud de El Niño usar, qué tan
   sensibles son los resultados a cambiar los pesos de la fórmula, y qué
   tanto importan los dos valores atípicos que se encontraron en la Fase 4
   (el evento de Quito con 750,000 afectados indirectos y el de Baños de
   Agua Santa con 500,000 muertes de ganado).

## ¿Qué encontramos?

- El cantón con mayor cronicidad de todo el país es el **Distrito
  Metropolitano de Quito**, seguido de **Ambato** y **Chone**. A nivel
  provincia, **Tungurahua** lidera, seguida de **Manabí** y **Pichincha**.

- Un hallazgo valioso: cantones con el mismo puntaje final pueden llegar
  ahí por caminos completamente distintos. Quito llega arriba por la
  persistencia (prácticamente nunca deja de tener algún evento) y la
  frecuencia, no porque sus eventos individuales sean los más graves.
  Ambato tiene una severidad casi nula por evento, pero una frecuencia y
  persistencia altísimas. Chone es lo contrario: pocos eventos, pero muy
  graves. Esto es justamente lo útil de combinar cuatro medidas distintas
  en vez de una sola: permite distinguir *qué tipo* de problema tiene cada
  cantón, no solo cuánto.

- **Los dos valores atípicos de la Fase 4 ya se verificaron y uno se
  corrigió** (ver más abajo). Con el dato corregido, Baños de Agua Santa
  pasó del 4º al 8º lugar del ranking nacional — sigue en la categoría más
  alta de cronicidad, pero ahora por su frecuencia y persistencia real, no
  por un dato de ganado que resultó ser un error de captura.

- Aun con esa corrección hecha, **la prueba de sensibilidad a valores
  extremos de Severidad sigue siendo la más consecuente de todas**: casi
  6 de cada 10 cantones (59%) cambiarían de categoría de cronicidad según
  qué tanto peso se le dé a los eventos con cifras muy grandes (como el de
  Quito, que sí se confirmó como legítimo). Esto ya no es un problema de
  un dato mal capturado — es una característica propia del método de
  cálculo que conviene tener presente si el índice se usa para decisiones
  binarias (¿entra o no en la lista de prioridad?).

- Otro hallazgo con matiz importante, **corregido el 4 de septiembre de
  2026** (ver nota abajo): dar el mismo peso a las cuatro dimensiones
  ("equitativo") es, de los tres escenarios de pesos probados, el que más
  cambia a qué categoría queda asignado cada cantón — 29% de ellos. Dar
  más peso a la Severidad, en cambio, es ahora el escenario **más
  estable** de los tres (14% de cambios de categoría). Es un recordatorio
  de que "el ranking casi no cambia" no siempre significa "la
  clasificación final tampoco cambia" — pero también de que esta prueba
  hay que repetirla cada vez que se actualiza un ingrediente del índice,
  porque el escenario más frágil puede cambiar.

## Dos ajustes que se hicieron en el camino

**Un ajuste técnico**, al probar la sensibilidad a los valores atípicos: la
primera prueba usó un método (recortar el 5% más extremo de los datos) que
resultó demasiado agresivo para algunas variables donde más del 95% de los
eventos tienen valor cero — terminó aplastando casi toda la información
real en vez de solo los extremos. Se detectó, se explicó la causa exacta,
y se corrigió usando un recorte más conservador (el 1% más extremo) antes
de reportar el resultado final.

**Una corrección de dato**, siguiendo el pedido explícito de Jerson tras
la Fase 8: se investigó el evento de Baños de Agua Santa (500,000 animales
reportados como muertos) buscando en prensa independiente si había alguna
relación real con el evento. No se encontró ninguna mención de pérdida de
ganado en ningún medio, pese a cobertura extensa del mismo evento con
otros detalles (personas fallecidas, pérdidas económicas). Siguiendo la
instrucción de fijar en cero lo que no tiene evidencia que lo respalde, se
corrigió el valor a 0 en el origen de los datos y se recalculó todo el
pipeline (Fases 1 a 8) con el dato corregido. El evento de Quito (750,000
personas afectadas indirectamente), en cambio, sí quedó respaldado por la
descripción del reporte original y se mantuvo sin cambios. Ver el detalle
completo en el resumen ejecutivo de la Fase 4.

## ¿Cómo contribuye esto al objetivo final?

Este es, en esencia, el primer HCI completo del proyecto — la
herramienta central que el diseño original proponía para apoyar decisiones
de Acción Anticipatoria en Ecuador. Las pruebas de sensibilidad no son un
paso opcional: son lo que separa un número calculado una sola vez de un
índice en el que se puede confiar para decisiones reales.

## ¿Qué falta?

- Fase 9: análisis espacial (identificar agrupamientos geográficos de
  cronicidad, no solo cantón por cantón).
- Fase 10: mapas, perfiles por cantón/provincia, y el tablero interactivo.
- Validación contra fuentes externas (reportes internacionales de
  desastres) antes de un uso operativo pleno.

## Un cambio hecho después (17 de agosto de 2026)

Tras ampliar el criterio de "mes de El Niño" (ver la actualización de la
Fase 5), se recalculó el índice completo. El **top 3 se mantiene
igual — Quito, Ambato y Chone, en ese orden** — así que la conclusión
principal del proyecto no cambia. Lo que sí cambió, de forma medible, es
uno de los ingredientes: Quito ahora también destaca en Recurrencia por sí
sola (antes lideraba el HCI sobre todo por Persistencia y Severidad, no
por Recurrencia) — un ajuste que refina el "por qué" detrás del número,
sin cambiar el "quién" está en los primeros lugares.

## Otro cambio hecho después (4 de septiembre de 2026)

Al recalcular el índice el 17 de agosto (arriba), las pruebas de
sensibilidad a los pesos de la fórmula también cambiaron de resultado,
pero eso no se había actualizado en este resumen hasta ahora. El texto
decía que dar más peso a la Severidad era el escenario que más cambiaba
la categoría final de los cantones — con los datos vigentes, es al revés:
ese escenario es ahora el más estable, y el más inestable es dar el mismo
peso a las cuatro dimensiones. Se corrigió arriba. El número de la
sensibilidad a valores extremos también se actualizó, de 49% a 59% de los
cantones. No cambia ninguna conclusión operativa del proyecto (el top 3
de cantones/provincias no se altera), pero si se citó la cifra anterior
en alguna comunicación externa, conviene actualizarla.
