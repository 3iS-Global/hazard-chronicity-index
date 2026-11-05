# 13 — Poniendo a prueba los pesos del índice, a fondo (resumen ejecutivo)

**Fase 13 del proyecto EFCI Ecuador — completada el 4 de septiembre de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

La fórmula del EFCI le da distinta importancia a cada ingrediente: 35%
Recurrencia, 30% Severidad, 20% Persistencia, 15% Magnitud de El Niño —
y dentro de Severidad, otros 5 pesos más (30% Población, 25% Vivienda,
20% Agricultura, 15% Ganadería, 10% Infraestructura). Todos esos números
vienen del diseño original del proyecto: son un criterio experto
razonado, no un resultado de laboratorio ni un número tomado de un
estudio publicado con ese fin.

Eso no los invalida — es una práctica normal al construir un índice
nuevo — pero si el proyecto se va a usar para decidir dónde invertir
recursos de preparación ante desastres, hace falta demostrar, con
pruebas, qué tan sólidos son esos pesos: si cambiara alguno un poco,
¿cambiaría mucho la lista de cantones prioritarios?

## ¿Qué se hizo ya, en la Fase 8, y qué falta?

La Fase 8 ya probó 3 alternativas puntuales de los 4 pesos grandes
(repartir el peso en partes iguales, dar más peso a Severidad, dar más
peso a Recurrencia) y encontró algo importante: aunque el orden general
de los cantones casi no cambia, la **categoría final** (Muy Baja a Muy
Alta) sí puede cambiar bastante — hasta 29% de los cantones cambian de
categoría según el escenario. También probó qué tan sensible es
Severidad a sus 2 valores más extremos (hasta 59% de los cantones
cambiarían de categoría).

Lo que falta, y es lo que aborda esta fase:

1. Probar **miles** de combinaciones de pesos, no solo 3 — para saber si
   la conclusión depende de qué 3 combinaciones se hayan elegido a mano.
2. Probar, por primera vez, los 5 pesos **internos** de Severidad
   (Población/Vivienda/Agricultura/Ganadería/Infraestructura) — nunca se
   habían puesto a prueba, solo los 4 pesos grandes.
3. Formalizar el criterio experto detrás de esos 5 pesos con un método
   estructurado (llamado AHP) que obliga a comparar la importancia de
   cada par de categorías una por una y revisa que las respuestas sean
   internamente consistentes — en vez de solo "parecer razonable".
4. Calcular, para cada cantón, no solo un número de cronicidad sino un
   rango ("entre tanto y tanto") — para saber si el número final es
   estable o depende mucho de qué eventos específicos ocurrieron.

## Un hallazgo importante, encontrado al preparar esta fase

Al revisar los resultados de la Fase 8 antes de construir sobre ellos, se
encontró que el resumen de esa fase tenía una cifra desactualizada: decía
que dar más peso a Severidad era el escenario que más cambiaba la
categoría final de los cantones (68%). Con los datos vigentes (tras la
actualización del criterio de El Niño de agosto), es al revés: ese
escenario es ahora el **más estable** (14%), y el que **más** cambia es
repartir el peso en partes iguales (29%). Ya se corrigió en el resumen de
la Fase 8 y en la presentación ejecutiva. No cambia ninguna conclusión
operativa del proyecto (el ranking de cantones/provincias más crónicos no
se altera), pero es un buen ejemplo de por qué esta fase es necesaria: una
prueba hecha con solo 3 escenarios puede dar una conclusión que cambia con
cada actualización de los datos, mientras que una prueba que cubre miles
de combinaciones es más difícil de "voltear" por accidente.

## ¿Qué se encontró, con miles de pruebas en vez de 3?

- **El peso que más importa no es el que se pensaba.** Con solo 3
  escenarios (Fase 8), todo apuntaba a que el peso de Severidad era el
  más delicado. Al probar miles de combinaciones, resultó ser el
  **menos** influyente de los 4 — el que más mueve la clasificación final
  es el de **Magnitud de El Niño**, el más pequeño de los 4 (15%).
  Probablemente porque esa variable se mueve en categorías (débil,
  moderado, fuerte...) en vez de en una escala continua, así que un
  cambio de peso pequeño puede empujar a más cantones de golpe al lado
  equivocado de un corte de categoría.

- **Los 5 pesos internos de Severidad sí tienen respaldo formal.** Se
  sometieron por primera vez a un método estructurado (AHP) que revisa
  que las comparaciones sean consistentes entre sí — pasó la prueba con
  holgura. Los pesos actuales (población primero, luego vivienda,
  agricultura, ganadería, infraestructura) no son solo "una jerarquía que
  parece razonable": formalizada, es matemáticamente coherente.

- **Solo un método puramente estadístico (sin ningún criterio humano)
  discrepa bastante** — le daría casi la mitad de la importancia total a
  Infraestructura (escuelas y centros de salud) y casi nada a Población.
  Eso no significa que los pesos actuales estén mal: ese método mide
  cuánto varían los datos históricos, no qué tan grave es cada tipo de
  impacto — son preguntas distintas.

- **La sensibilidad a valores extremos, confirmada con un segundo
  método independiente.** La Fase 8 ya había encontrado que casi 6 de
  cada 10 cantones cambiarían de categoría según cómo se traten los
  eventos con cifras muy grandes. Se probó un segundo método,
  construido de forma completamente distinta, y llegó a un número muy
  parecido (52%). Que dos caminos distintos lleguen al mismo lugar es
  una señal fuerte de que esto es real, no un efecto de un método en
  particular.

- **Un hallazgo curioso sobre qué tan "confiable" es el número de cada
  cantón.** Se esperaría que los cantones con más eventos históricos
  fueran los más confiables. Resultó ser casi lo contrario: cantones
  pequeños con pocos eventos suelen tener un número muy estable (porque
  están muy lejos del techo nacional que define la escala), mientras que
  cantones como Chone, que sí compiten por ese techo, tienen más
  variación real. Es un matiz importante para no leer el número de un
  cantón pequeño como "más sólido" solo porque tiene menos eventos
  detrás.

## ¿Cómo contribuye esto al objetivo final?

Un índice que va a apoyar decisiones reales de Acción Anticipatoria —
priorizar dónde llega ayuda antes de que ocurra el desastre — necesita
poder responder con evidencia a la pregunta "¿por qué estos pesos y no
otros?". Esta fase es exactamente eso: no cambia el EFCI que ya se
calculó, pone a prueba qué tan sólido es, con el mismo rigor que
exigiría un revisor técnico externo antes de aprobar su uso operativo.

## ¿Qué falta?

- Decidir si el hallazgo sobre el peso de Magnitud de El Niño amerita
  ajustarlo en una futura versión del EFCI — por ahora solo se documenta
  la evidencia, no se cambia nada.
- Seguir pendiente, como en fases anteriores: comparar el EFCI contra
  reportes internacionales de desastres (EM-DAT, DesInventar, UNOSAT).
