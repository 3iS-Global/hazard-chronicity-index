# 03 — Primer análisis histórico por provincia y cantón (resumen ejecutivo)

**Fase 3 de 10 del proyecto EFCI Ecuador — completada el 5 de agosto de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

Las fases anteriores dejaron 21,743 eventos limpios y correctamente
ubicados en el mapa de Ecuador. Esta fase da el primer paso hacia
responder las preguntas que realmente le importan a quien toma decisiones:
¿qué provincias y cantones han sido afectados con más frecuencia?, ¿desde
cuándo?, ¿la situación está empeorando, mejorando o se mantiene estable?,
¿qué tan grave ha sido el impacto en cada lugar?

Todavía no es el índice final de cronicidad (eso llega en las Fases 4 a 8),
pero es el primer momento del proyecto en que aparecen cifras concretas,
comparables entre provincias y cantones.

## ¿Qué se hizo?

1. **Se contó cuántas veces, y en qué años y meses, ha sido afectado cada
   cantón y cada provincia** — separado por tipo de peligro (inundación,
   deslizamiento, aluvión, socavamiento) y también combinado.

2. **Se calculó qué tan grave ha sido el impacto en promedio y en el peor
   caso** — personas afectadas, viviendas, escuelas, salud, cultivos,
   ganado — siempre indicando también sobre cuántos eventos se calculó ese
   promedio, para no confundir un promedio robusto con uno basado en 2 o 3
   casos.

3. **Se contó cuántos eventos coincidieron con cada categoría de El Niño /
   La Niña**, usando dos fuentes independientes (el índice costero ICEN y
   el índice oceánico ONI de NOAA), para poder comparar ambas antes de
   decidir cuál usar como referencia principal más adelante.

4. **Se calculó si la frecuencia de eventos está subiendo, bajando o se
   mantiene estable** en cada cantón y provincia a lo largo de 2015-2025,
   usando una prueba estadística estándar (Mann-Kendall) diseñada para no
   inventar una tendencia donde no la hay.

## ¿Qué encontramos?

- Las provincias con más eventos registrados en el período 2015-2025 son
  Pichincha (2,718), Guayas (1,738), Loja (1,575), Manabí (1,506) y El Oro
  (1,492). Esto no significa automáticamente que sean las más "crónicas"
  frente a El Niño — son también las más pobladas y con más territorio, y
  ese ajuste se hace en las fases siguientes.
- A nivel provincia, 9 de las 24 provincias muestran una tendencia
  creciente estadísticamente significativa en el número de eventos
  reportados por año; 1 muestra tendencia decreciente; las 14 restantes se
  mantienen estables.
- A nivel cantón, los que muestran el crecimiento más marcado son Quito,
  Cuenca y Guayaquil — nuevamente, coherente con ser los cantones más
  grandes y con más capacidad de reporte, no necesariamente los más
  vulnerables proporcionalmente.
- Las dos fuentes de El Niño/La Niña (ICEN y ONI) no siempre coinciden en
  cómo categorizan el mismo período — es una diferencia real y esperada
  entre ambos índices, y queda documentada con cifras concretas para
  decidir, en una fase próxima, cuál usar como referencia oficial del
  proyecto (o si se combinan ambas).

## Un ajuste importante que se hizo en el camino

Al construir esta fase se detectó, gracias a una validación automática que
el propio proceso ejecuta antes de guardar cualquier resultado, que 35
eventos se estaban perdiendo silenciosamente de las tablas agregadas por un
detalle técnico: el nombre oficial de la provincia de esos 35 eventos venía
vacío (son los mismos 35 eventos "sin ubicación exacta" ya documentados en
la Fase 2), y el proceso de agrupación los descartaba sin avisar. Se
corrigió tomando el nombre oficial de cantón/provincia por el código
administrativo (que sí tiene el 100% de los eventos cubierto) en vez del
nombre derivado del mapa. La validación automática confirmó, después de la
corrección, que los 21,743 eventos completos están contados — ninguno se
perdió. Este es exactamente el tipo de control que el proyecto exige: que
ningún error quede oculto, y que las cifras finales sean verificables.

## ¿Cómo contribuye esto al objetivo final?

Estas tablas son los ladrillos con los que se construirán los cuatro
índices compuestos de las próximas fases (Severidad, Recurrencia,
Persistencia, Magnitud ENSO) y, finalmente, el Índice de Cronicidad de
Inundaciones por El Niño (EFCI). Sin este paso, esos índices no tendrían
ninguna cifra real sobre la cual normalizar y ponderar.

## ¿Qué falta?

- Avanzar hacia la Fase 4: el Índice de Severidad, que combina los
  impactos en población, vivienda, agricultura, ganadería e infraestructura
  en una sola medida comparable entre cantones.
- Decidir si el índice de referencia de El Niño/La Niña del proyecto será
  ICEN, ONI, o una combinación de ambos — con las diferencias entre ambos ya
  cuantificadas en esta fase.
