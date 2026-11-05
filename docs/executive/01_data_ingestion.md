# 01 — Construcción de la base histórica de eventos (resumen ejecutivo)

**Fase 1 de 10 del proyecto HCI Ecuador — completada el 5 de agosto de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

Ecuador ya cuenta con más de 10 años de reportes de emergencias (SNGRE,
ECU911), pero están mezclados con miles de eventos que no son de nuestro
interés (incendios, explosiones, sismos, etc.) y en un formato de Excel
difícil de analizar de forma sistemática. Sin un primer paso que separe,
limpie y ordene esta información, no es posible calcular nada confiable
sobre "qué tan crónicas" son las inundaciones en cada provincia o cantón.

Esta primera fase responde a una pregunta simple pero fundamental: **¿de qué
eventos exactos vamos a hablar, y qué tan buena es esa información?**

## ¿Qué se hizo?

1. **Se separaron los eventos relevantes.** De 69,718 reportes de emergencia
   registrados entre 2015 y 2025, se identificaron 21,743 relacionados con
   el problema que nos interesa: inundaciones, deslizamientos, aluviones y
   socavamientos — todos ligados a lluvias intensas.

2. **Se revisó la calidad de la información.** Se verificó que las fechas y
   coordenadas de estos 21,743 eventos sean utilizables: el resultado fue
   positivo — cero errores de fecha y cero coordenadas fuera del territorio
   ecuatoriano.

3. **Se protegieron los datos personales.** Los reportes originales incluían
   nombres y teléfonos de operadores de emergencia. Esa información se
   eliminó de la base de trabajo — no es necesaria para el análisis y no
   corresponde compartirla en un producto institucional.

4. **Se construyó una serie completa del fenómeno El Niño mes a mes.** Ya
   existía información sobre El Niño/La Niña en el archivo de Ecuador, pero
   estaba incompleta (solo cubría los meses en que alguien ya había
   documentado un impacto). Se reconstruyó la serie completa —132 meses,
   sin huecos— para poder cruzar *cualquier* evento de inundación con la
   condición de El Niño de ese mismo mes, no solo los ya conocidos.

5. **Se unieron ambas piezas.** Cada uno de los 21,743 eventos quedó
   vinculado al estado de El Niño del mes en que ocurrió, con un 100% de
   éxito en el cruce.

## ¿Qué encontramos?

- De los eventos relevantes: 12,625 son deslizamientos, 7,281 son
  inundaciones, 1,152 son socavamientos y 685 son aluviones.
- Estos eventos ocurrieron en las 24 provincias y en 221 de los 221+
  cantones del país — el problema no está concentrado en un solo lugar.
- El archivo de Ecuador ya contenía trabajo previo valioso (un modelo de
  escenarios de respuesta ante El Niño por cantón) que se usará más adelante
  para comparar y validar nuestros propios resultados, en vez de descartarlo.

## ¿Cómo contribuye esto al objetivo final?

Esta base limpia y verificada es el cimiento de todo lo que sigue: sin ella
no se puede calcular con confianza qué tan seguido se inunda cada cantón, qué
tan grave ha sido el impacto, ni construir el índice de cronicidad (HCI)
que finalmente ayudará a decidir dónde actuar antes de que ocurra el próximo
evento de El Niño. Es, en términos simples, pasar de "una carpeta de reportes
sueltos" a "una base de datos que se puede analizar con rigor científico".

## ¿Qué falta?

- Confirmar con el equipo el criterio usado para preparar una versión
  reducida de la base (llamada `Base2`) que ya existía en el archivo, por si
  aporta información adicional útil.
- Vincular esta base con la división político-administrativa oficial del
  país (siguiente fase).
- Comparar nuestros resultados contra el modelo de escenarios de respuesta
  que el equipo ya había construido, como control de calidad.
