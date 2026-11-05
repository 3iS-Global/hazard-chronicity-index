# 02 — Ubicación de los eventos en el mapa de Ecuador (resumen ejecutivo)

**Fase 2 de 10 del proyecto EFCI Ecuador — completada el 5 de agosto de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

La Fase 1 nos dio una lista limpia de 21,743 eventos, cada uno con la
provincia y el cantón donde ocurrió. Pero para hacer mapas y comparar
cantones entre sí, no basta con el nombre — se necesita el "dibujo" real
del territorio de cada provincia y cada cantón de Ecuador, y hay que
verificar que la ubicación de cada evento realmente caiga dentro del
territorio que se le atribuye.

## ¿Qué se hizo?

1. **Se incorporó el mapa oficial de Ecuador.** Se usó la división
   político-administrativa oficial (fuente: INEC, distribuida por la
   plataforma humanitaria HDX), con el contorno de las 24 provincias, los
   221 cantones y las 1,042 parroquias del país.

2. **Se verificó que cada evento tenga un territorio real donde ubicarse.**
   Los 21,743 eventos coinciden al 100% con una provincia y un cantón
   oficial — ninguno quedó "huérfano" sin territorio reconocido.

3. **Se hizo un control de calidad independiente.** Además de confiar en lo
   que reportó SNGRE, se verificó si el punto exacto (coordenadas) de cada
   evento realmente cae dentro del territorio del cantón que se reportó.
   Resultado: 98% coincide perfectamente. El 2% restante se marcó —no se
   descartó— para que quede claro cuáles registros tienen menor certeza de
   ubicación exacta (típicamente en zonas costeras, donde la coordenada
   puede caer justo en el límite con el mar).

4. **Se agregó una segunda verificación, a pedido de Jerson.** Cada evento
   trae también el nombre/código de la parroquia (una subdivisión más
   pequeña que el cantón) reportado por SNGRE. Se usó ese dato como "segundo
   testigo" para confirmar el cantón en los casos donde la coordenada no
   había podido verificarse directamente.

5. **Se generaron los archivos de mapa** listos para usarse en análisis
   geográfico y en el futuro tablero interactivo.

## ¿Qué encontramos?

- El 100% de los eventos tiene una provincia y un cantón oficial válido —
  la base de datos de SNGRE y el mapa oficial de Ecuador son totalmente
  compatibles.
- El 98% de los eventos tiene su ubicación exacta verificada dentro del
  cantón correcto por coordenada.
- Con la segunda verificación (parroquia), el nivel de confianza total subió
  a **99.78%** de los eventos con al menos una confirmación (coordenada o
  parroquia) de que el cantón reportado es correcto. Solo quedan 43 eventos
  (0.2%) sin ninguna confirmación clara, y 5 eventos (0.02%) sin ningún dato
  adicional disponible para verificar — de 21,743 en total.
- Importante: la parroquia por sí sola **no** habría servido como base
  completa del análisis — solo 8 de cada 10 eventos tienen una parroquia que
  coincide con el mapa oficial actual (probablemente porque los límites de
  parroquia cambian con más frecuencia que los de cantón). Por eso se usó
  como apoyo puntual para los casos dudosos, no como reemplazo del cantón.
- Se detectó que en 9 de las 24 provincias, el nombre venía escrito de más
  de una forma en los reportes originales (tildes, mayúsculas) — ya se
  armonizó usando el nombre oficial.

## ¿Cómo contribuye esto al objetivo final?

Con esta base, cada evento de inundación, deslizamiento, aluvión o
socavamiento ya se puede dibujar en un mapa real de Ecuador y agregarse por
provincia o por cantón con confianza. Este es el paso que hace posible,
literalmente, "ver" dónde se concentra la cronicidad — sin él, el índice
EFCI sería solo una tabla de números sin territorio.

## Pendientes cerrados (2026-08-05, misma tarde)

**¿Qué era "Base2"?** Ya se sabe con certeza: es la misma base de eventos,
pero recortada a los 38 meses en que hubo un episodio de El Niño/La Niña
documentado, y sin las provincias de la Amazonía (que no se ven afectadas
por El Niño costero) ni Galápagos. Es exactamente el insumo que el equipo
ya había usado para construir su modelo de escenarios de respuesta.

**¿Cómo se compara nuestro trabajo con el modelo de escenarios que ya
existía?** En 7 de cada 10 cantones, coincide: el evento más grave
históricamente sí es una inundación, deslizamiento, aluvión o socavamiento
— lo mismo que estamos midiendo nosotros. En 3 de cada 10, el evento más
grave que quedó registrado en esos mismos meses fue en realidad un
terremoto, una erupción volcánica u otro fenómeno sin relación con El
Niño, que solo coincidió en el calendario. Esto es un hallazgo útil: el
modelo anterior, al no separar por tipo de desastre, puede estar
sobrestimando el riesgo de El Niño en algunos cantones. Nuestro enfoque, al
filtrar desde el inicio solo los eventos hidrometeorológicos, evita ese
problema.

**¿Y los 43 casos dudosos?** Se revisaron uno por uno contra la
descripción original del reporte, cuando existía. No apareció ningún
patrón de error — son en su mayoría cantones vecinos donde la coordenada
cayó justo del otro lado del límite. Se mantiene el cantón que reportó
SNGRE como el válido en los 43 casos.

Los tres hallazgos, con el detalle completo, quedan en el archivo Excel
`outputs/tables/cierre_pendientes_fase2.xlsx`.

## ¿Qué falta?

- Avanzar a la Fase 3: el primer análisis histórico por provincia y cantón.
