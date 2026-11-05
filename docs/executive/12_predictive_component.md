# 12 — El componente predictivo (resumen ejecutivo)

**Fase 12 (extensión) del proyecto HCI Ecuador — completada el 6 de agosto de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

Todo el proyecto hasta ahora describe el **pasado**: qué tan crónico ha sido cada
cantón históricamente. Esta fase da el primer paso hacia el **futuro**: ante un
nuevo episodio El Niño que se está desarrollando, ¿cuántas personas, hectáreas de
cultivo y viviendas se puede esperar que resulten afectadas en cada cantón — y qué
tan probable es que sea un episodio severo? Es exactamente el componente que el
diseño original del proyecto (2026-08-04) dejó planteado como trabajo futuro y que
ahora se construyó y se puso a prueba con datos reales.

## ¿Qué se hizo?

1. Se organizó el historial en 6 "episodios" El Niño completos (no meses sueltos) —
   2015-2016, 2017, 2018-2019, 2023, 2024 y 2025 — y se calculó, para cada uno de
   los 221 cantones y cada episodio, cuánta gente, cuántos cultivos y cuántas
   viviendas resultaron afectadas.
2. Se entrenó un modelo (Random Forest, un algoritmo de aprendizaje automático
   robusto y ampliamente usado) para aprender el patrón: dado el historial de un
   cantón y qué tan fuerte es el episodio que se avecina, ¿qué impacto y qué
   probabilidad de severidad hay que esperar?
3. **Se comparó siempre el modelo contra un punto de referencia simple** — "asumir
   que este episodio se va a parecer al promedio histórico del cantón, sin usar
   ningún modelo" — para saber si el modelo realmente aporta algo, no solo para
   presentar un número aislado.
4. Se validó de la forma más exigente posible dado lo poco que se tiene: se
   entrenó dejando cada uno de los 6 episodios fuera por turno, y se probó
   prediciendo justo ese episodio nunca visto — la forma más honesta de simular
   "qué tan bien habría predicho el modelo un episodio antes de que ocurriera".

## ¿Qué encontramos?

- **El modelo sí aporta valor sobre la referencia simple, de forma consistente,
  aunque modesta** — algo esperable con solo 6 episodios históricos disponibles, no
  un límite del método sino del tamaño real de la muestra.
- Para estimar magnitudes (personas, hectáreas, viviendas afectadas): el modelo se
  equivocó, en promedio, **25% menos** que simplemente asumir el promedio
  histórico del cantón, y le ganó a esa referencia simple en 15 de 18
  combinaciones posibles (6 episodios × 3 tipos de impacto).
- Para estimar si un cantón tendrá un impacto **severo** (sí/no): el modelo
  distinguió claramente mejor que la referencia simple — acertó qué tan probable
  era la severidad con una confiabilidad de 79% en promedio (medida con el
  indicador estándar AUC, donde 50% sería "adivinar al azar" y 100% sería perfecto),
  contra 65% de la referencia simple — y le ganó en 5 de los 6 episodios.
- El factor más importante para el modelo, con diferencia, es **el historial propio
  del cantón** — cuánto ha sido afectado antes — más que la fuerza del episodio El
  Niño en sí. Esto confirma, con un método totalmente distinto, el mismo hallazgo ya
  documentado en la Fase 9: la cronicidad de un cantón se explica sobre todo por
  procesos sostenidos en el tiempo (con qué frecuencia y por cuánto tiempo se
  repiten los eventos), no tanto por qué tan fuerte sea un episodio puntual de El
  Niño.

## Una limitación que hay que tener presente, sin maquillarla

Con solo 6 episodios El Niño documentados en 11 años de datos, ningún modelo —
por sofisticado que sea — puede ser altamente preciso. No es una debilidad de
este modelo en particular, es una limitación real de cuántos eventos climáticos
independientes existen para aprender de ellos. Por eso el diseño de esta fase
insistió en comparar siempre contra una referencia simple: la conclusión correcta
no es "el modelo predice con precisión", sino "el modelo aporta una mejora real y
consistente sobre no usar ningún modelo — y esa mejora crecerá naturalmente a
medida que ocurran más episodios El Niño en el futuro y se pueda reentrenar con
más datos".

## ¿Cómo contribuye esto al objetivo final?

Esta fase cierra el círculo que el proyecto se propuso desde el diseño original:
pasar de describir el pasado a anticipar el futuro. El resultado — un modelo
entrenado, guardado y listo para usar (`models/step12_modelos_finales.joblib`) —
puede generar, ante el próximo episodio El Niño real, una primera estimación de
qué cantones esperar que resulten más afectados y con qué magnitud, apoyando
directamente decisiones de priorización de Acción Anticipatoria antes de que el
episodio se desarrolle por completo.

## ¿Qué falta?

- Actualizar y reentrenar el modelo cuando ocurra un nuevo episodio El Niño real
  (la validación más honesta posible es esperar y comprobar contra un evento
  genuinamente futuro, no solo los 6 históricos).
- Incorporar información física adicional (lluvia satelital, elevación del
  terreno) si se decide ampliar el proyecto — podría mejorar la precisión.
- Evaluar métodos alternativos (como redes bayesianas) si en el futuro hay más
  episodios documentados que justifiquen el esfuerzo adicional de diseño.
