# 09 — ¿Dónde se agrupa la cronicidad? (resumen ejecutivo)

**Fase 9 de 10 del proyecto EFCI Ecuador — completada el 6 de agosto de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

El EFCI de la Fase 8 responde "¿qué tan crónico es cada cantón?", uno
por uno. Pero para decidir dónde concentrar recursos de Acción
Anticipatoria, importa también otra pregunta: ¿esos cantones crónicos
están dispersos por todo el país al azar, o forman zonas geográficas
conectadas donde conviene planificar una respuesta conjunta, no
cantón por cantón? Esta fase responde eso con cuatro herramientas
estadísticas espaciales, no solo con un mapa de colores.

## ¿Qué se hizo?

1. **Se identificaron "zonas calientes" y "zonas frías"** de cronicidad
   (Getis-Ord Gi*): no solo qué cantón tiene el número más alto, sino
   qué cantón *y su entorno* son consistentemente altos o bajos.
2. **Se identificaron clusters y casos atípicos** (Local Moran's I):
   grupos de cantones vecinos que comparten un mismo nivel de
   cronicidad, y casos donde un cantón no se parece a sus vecinos.
3. **Se construyó un mapa de densidad continuo** (no limitado a
   fronteras de cantón), ponderado por qué tan grave fue cada evento,
   no solo cuántos hubo.
4. **Se agregó todo en hexágonos de ~10 km**, para comparar zonas del
   mismo tamaño — los cantones de Ecuador varían mucho en área, lo que
   puede distorsionar la lectura visual de un mapa por cantón.

## ¿Qué encontramos?

- **Hay una zona claramente más caliente que las demás, y no es solo
  Quito: es todo su entorno.** Un grupo de 11 cantones alrededor de
  Quito (Cayambe, Mejía, Rumiñahui, San Miguel de los Bancos y otros,
  más una conexión hacia Esmeraldas por un lado y hacia la Amazonía
  norte por otro) resultó ser la zona más consistentemente crónica del
  país con el nivel de confianza más alto (99%). El propio Quito
  también es zona caliente, aunque con un nivel de confianza apenas
  menor — su entorno, en conjunto, es un núcleo todavía más fuerte que
  la ciudad sola.

- **También hay dos zonas frías claras**: casi toda la provincia de
  Sucumbíos (norte de la Amazonía) y un grupo de cantones en Azuay,
  ambas consistentemente bajas en cronicidad — resultado esperado, esas
  zonas no reciben la misma influencia costera de El Niño que el resto
  del país.

- **Un hallazgo con matiz interesante**: Cuenca tiene un puntaje EFCI
  relativamente alto por sí sola, pero está rodeada de cantones de
  puntaje bajo. Esto la hace aparecer como "zona fría" en un análisis
  (porque se mide junto con su entorno) y como un caso atípico en otro
  (porque ella misma no es baja) — las dos lecturas no se contradicen,
  se complementan: Cuenca es relativamente crónica dentro de una región
  que, en conjunto, no lo es tanto.

- **El hallazgo más útil para entender el EFCI**: las zonas calientes de
  cronicidad están impulsadas sobre todo por qué tan seguido ocurren
  eventos y por cuánto tiempo se sostienen (Recurrencia y Persistencia),
  no tanto por qué tan graves son individualmente (Severidad) ni por la
  fuerza de El Niño (Magnitud ENSO). El 82% de las zonas calientes de
  EFCI también son zonas calientes de Recurrencia, pero solo el 25%
  también lo son de Magnitud ENSO. Es decir: los "clusters" geográficos
  del país reflejan sobre todo procesos sostenidos en el tiempo, no
  eventos puntuales extremos — información valiosa porque sugiere qué
  tipo de intervención tiene más sentido en cada zona (prevención
  continua vs. respuesta a eventos aislados).

- **El mapa de densidad y la agregación en hexágonos confirman lo
  mismo**: el punto de mayor concentración de impacto ponderado por
  severidad está en Quito y su entorno inmediato (Rumiñahui, Mejía).
  Al mirar los hexágonos con más eventos, de nuevo aparecen Quito,
  Ambato y alrededores — pero al mirar los hexágonos con mayor
  severidad acumulada, Chone y Babahoyo (con menos eventos, pero más
  graves) toman la delantera. El mismo patrón que ya se había visto en
  la Fase 8: unos cantones son crónicos por frecuencia, otros por
  gravedad.

## ¿Cómo contribuye esto al objetivo final?

Esta fase transforma un ranking cantón por cantón en un mapa de
patrones geográficos reales — con esto, el proyecto ya puede responder
no solo "¿qué provincias han sido repetidamente afectadas?" sino
"¿existen corredores o regiones conectadas que conviene tratar como
una sola zona de intervención?", una de las preguntas centrales de la
visión del proyecto.

## ¿Qué falta?

- Fase 10: mapas finales, perfiles por cantón/provincia, y el tablero
  interactivo — esta fase produjo los insumos de datos (grillas, capas
  de hotspots, hexágonos), pero todavía no las visualizaciones finales
  para decisión.
- Validación contra fuentes externas (reportes internacionales de
  desastres) antes de un uso operativo pleno.
