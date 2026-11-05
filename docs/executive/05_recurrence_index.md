# 05 — Región Niño 1+2 e Índice de Recurrencia (resumen ejecutivo)

**Fase 5 de 10 del proyecto HCI Ecuador — completada el 5 de agosto de 2026**
**Actualizado el 17 de agosto de 2026 — ver "Un cambio importante hecho después" al final**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

Jerson pidió explícitamente tener en cuenta las regiones del Pacífico
conocidas como "Niño 1+2" — las más cercanas a la costa de Ecuador y Perú
— y su relación con los índices que ya veníamos usando (ICEN y ONI). Esta
fase responde esa pregunta con datos, y de paso resuelve algo que llevaba
abierto desde el diseño original del proyecto: ¿cuál de los dos índices
(ICEN u ONI) debe ser la referencia oficial de "El Niño" para el proyecto?
Y construye el Índice de Recurrencia: qué tan seguido, dentro de los meses
de El Niño documentados, cada cantón sufrió al menos un evento.

## ¿Qué se hizo?

1. **Se incorporó la temperatura del mar cruda de la región Niño 1+2**
   (descargada de NOAA por Jerson, igual que se hizo antes con los mapas de
   límites administrativos), y se comparó estadísticamente contra ICEN y
   ONI.

2. **Se confirmó, con datos propios del proyecto, que ICEN es el índice
   correcto para Ecuador**: la correlación entre ICEN y la temperatura
   cruda de Niño 1+2 es prácticamente perfecta (99.7%), porque ICEN está
   oficialmente calculado a partir de esa misma región del océano. ONI, en
   cambio, mide una región distinta del Pacífico (más al centro) y se
   relaciona solo moderadamente con ambos (~79%).

3. **Se puso a prueba la idea central de todo el proyecto**: ¿de verdad
   ocurren más inundaciones/deslizamientos durante los meses de El Niño?
   Respuesta: sí, casi el doble (los meses de El Niño tuvieron en promedio
   253 eventos, frente a 129 en los demás meses) — una confirmación
   importante, no asumida de antemano.

4. **Se calculó el Índice de Recurrencia**: para cada cantón y provincia,
   qué fracción de los 38 meses de El Niño documentados (2015-2025)
   tuvieron al menos un evento registrado.

## ¿Qué encontramos?

- **Ambato** es el cantón con mayor recurrencia (evento en 34 de los 38
  meses de El Niño, 89%), seguido de Morona, Santo Domingo y Quito.
- A nivel provincia, **Tungurahua y Morona Santiago** tuvieron al menos un
  evento en los 38 de 38 meses de El Niño — el máximo posible.
- Contar los meses de El Niño con nuestra propia definición dio
  exactamente 38 — el mismo número que ya usaba, sin que se lo pidiéramos,
  el modelo de escenarios que el equipo de FAO/COE ya tenía construido en
  el archivo Excel original. Es una confirmación cruzada valiosa: dos
  metodologías independientes llegaron al mismo período.

## Un ajuste que se hizo en el camino

Al revisar la primera versión de la tabla, se encontró que un cantón
(San Fernando, en Azuay, con un solo evento histórico) no aparecía en
absoluto en el resultado, en vez de aparecer con recurrencia igual a cero.
La razón: su único evento no cayó en ningún mes de El Niño, así que no
generaba ninguna fila. Se corrigió antes de entregar el resultado, para que
los 221 cantones y las 24 provincias aparezcan siempre, incluso cuando el
valor correcto es cero — es exactamente el tipo de vacío que el proyecto
está diseñado para detectar y corregir, no para dejar pasar.

## ¿Cómo contribuye esto al objetivo final?

Con este paso, el proyecto ya tiene dos de los cuatro ingredientes del HCI
final: Severidad (Fase 4) y ahora Recurrencia. Y de regalo, se resolvió una
pregunta metodológica que llevaba abierta desde el diseño original
(¿ICEN u ONI?) con evidencia concreta, no con una elección arbitraria — y
se confirmó, con datos, que la premisa completa del proyecto (más eventos
durante El Niño) es cierta para Ecuador 2015-2025.

## ¿Qué falta?

- Fase 6: Índice de Persistencia (cuánto duran, en meses consecutivos, los
  episodios de afectación).
- Fase 7: Índice de Magnitud de El Niño — ya con ICEN confirmado como
  referencia oficial.
- Fase 8: combinar Severidad, Recurrencia, Persistencia y Magnitud en el
  HCI final, con el análisis de sensibilidad que el diseño original exige.

## Un cambio importante hecho después (17 de agosto de 2026)

Jerson pidió ampliar el criterio de "mes de El Niño": ya no usar solo ICEN
(la región más cercana a la costa de Ecuador y Perú), sino también
considerar los meses en que ONI (el índice estándar internacional, que
mira una franja más amplia del Pacífico) marcó El Niño, aunque ICEN no lo
hiciera. La razón, comprobada con datos y no solo por intuición: en los
meses donde ICEN y ONI no coincidían, igual había muchos más eventos que en
un mes normal — es decir, esos meses "extra" sí importaban y se estaban
quedando fuera.

Con este cambio, el número de "meses de El Niño" pasó de 38 a **54** (de
132 meses totales en 2015-2025). Se guardó también de qué índice viene cada
mes (solo ICEN, solo ONI, o ambos de acuerdo) para no perder esa
trazabilidad. Al recalcular con el nuevo total de 54 meses, el ranking de
cantones más recurrentes cambia un poco: **Ambato sigue en primer lugar**
(ahora con evento en 50 de los 54 meses, 93%), pero **Quito sube claramente
al top 5** — antes no aparecía, ahora es el segundo cantón con más
recurrencia, porque varios de sus eventos caían justamente en esos meses
"solo ONI" que antes no contaban. El resto del ranking (Morona, Baños de
Agua Santa, Loja) se mantiene estable. Las Fases 7 (Magnitud) y 8 (HCI
compuesto) se recalcularon con este mismo ajuste, en cascada.


## Nota de actualización (6 oct 2026)

Una revisión posterior (Fase 15) mostró que el aumento de eventos durante El Niño es de 41 % a nivel nacional (no 96 %) una vez descontadas las lluvias normales de cada mes, y que es claro en la Costa (×3.5) pero no detectable en la Sierra ni el Oriente. Ver `15_enso_hazard_association.md`.
