# 15 — ¿Realmente hay más eventos cuando llega El Niño? (resumen ejecutivo)

**Fase 15 del proyecto HCI Ecuador — completada el 6 de octubre de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO y contrapartes institucionales
**Documento técnico:** `docs/methodology/15_enso_hazard_association.md`

## ¿Qué problema resuelve esta etapa?

Un revisor externo señaló, con razón, que no todos los eventos del índice
tienen su origen en El Niño: algunos son estacionales (las lluvias normales
de cada año) y, en Quito, el origen puede ser amazónico. Además, el
INAMHI ha indicado que no se espera un aumento de lluvias en la región
andina.

Hasta ahora el proyecto mostraba que hay casi el doble de eventos por mes
cuando hay El Niño (1.96 veces), pero esa cifra no descontaba que las lluvias
y los episodios de El Niño suelen coincidir en el calendario. Esta etapa
responde la pregunta de forma rigurosa: **¿cuántos eventos adicionales
aparecen realmente por El Niño, una vez descontado lo que ocurre
normalmente cada mes del año?** y la responde por región y por tipo de
amenaza.

## ¿Qué se hizo?

Se comparó, mes a mes entre 2015 y 2025, el número de eventos reportados
durante los meses de El Niño con los demás meses, **comparando siempre
el mismo mes del año** (para no confundir temporada de lluvias con El Niño)
y descontando que el sistema de reporte crece con el tiempo. Se hizo para
todo el país, para cada región (Costa, Sierra, Oriente) y para cada tipo de
amenaza, y se verificó que el resultado no dependa de una decisión técnica
particular ni de un solo episodio.

## ¿Qué se encontró?

| Pregunta | Respuesta |
|---|---|
| ¿Hay más eventos durante El Niño en el país? | **Sí, pero menos de lo que parecía:** 41 % más (no 96 %) una vez descontada la estacionalidad |
| ¿Es igual en todo el país? | **No.** En la **Costa**, los eventos se multiplican por 3.5. En la **Sierra** el aumento es pequeño (15 %) y **no se puede distinguir del azar**. En el **Oriente** no se detecta aumento |
| ¿Y según el tipo de amenaza? | **Inundación:** se duplica (×2.0), y en la Costa se multiplica por 5. **Socavamiento:** ×1.6. **Deslizamiento:** aumento leve y no concluyente (×1.2). **Aluvión:** ocurren **menos** eventos durante El Niño (×0.46) |
| ¿A mayor intensidad de El Niño, más eventos? | **Solo en la Costa.** En el resto del país un episodio "fuerte" no produce más eventos que uno "débil" |
| ¿Depende de un solo episodio? | No: la conclusión se mantiene al quitar cada episodio uno por uno |

## ¿Qué significa para el feedback recibido?

El revisor tiene razón en lo esencial, y los datos lo confirman:

* **Chone (Costa, Manabí):** zona donde El Niño sí produce muchos más
  eventos, sobre todo inundaciones. Su alta cronicidad de inundación es
  coherente con la señal de El Niño.
* **Quito y la Sierra:** los eventos son frecuentes y persistentes, pero
  **no se puede afirmar que sean consecuencia de El Niño**. Su posición alta
  en el índice describe un problema crónico real, de origen estacional y
  local, no un efecto específico de El Niño.
* **Aluviones:** no aumentan con El Niño; sus causas son otras (por ejemplo,
  actividad volcánica y lluvias locales).

Es importante decir con claridad lo que el índice **sí** y **no** es: mide
qué territorios han sufrido eventos de forma repetida y grave entre 2015 y
2025, y cuánto se solapan esos eventos con meses de El Niño. **No predice la
lluvia futura ni afirma que El Niño causó cada evento.**

## ¿Qué cambia y qué decisiones quedan abiertas?

Esta etapa no modifica la fórmula del índice. Deja tres decisiones para el
equipo:

1. **Etiquetar cada cantón** con la fuerza de la señal de El Niño de su
   región (fuerte, débil, no detectable), para que quien use el índice sepa
   cuándo es razonable activar acciones anticipatorias ante un nuevo
   episodio.
2. **Presentar el índice de aluvión como cronicidad del peligro**, no como
   cronicidad asociada a El Niño.
3. **Revisar el peso del componente "Magnitud de El Niño" (15 %)**: los datos
   no muestran que mayor intensidad implique más eventos fuera de la Costa.

## ¿Qué límites tiene este análisis?

* Solo hay **5 episodios de El Niño** en 2015–2025. Es poca información para
  asegurar cómo se comportará el próximo.
* Muestra **asociación, no causa**: no separa lluvia de exposición ni de
  cambios en el reporte.
* Trabaja con **reportes de eventos**, no con lluvia medida. Incorporar datos
  de lluvia (INAMHI, satélite) es el siguiente paso recomendado.

## Texto del aviso para el dashboard

> **Alcance, supuestos y limitaciones de este análisis.** Este índice mide la
> cronicidad histórica (2015–2025) de eventos de inundación, deslizamiento,
> socavamiento y aluvión en los cantones de Ecuador, y su coincidencia con
> meses de El Niño. **No atribuye cada evento a El Niño:** una parte
> importante responde a la estacionalidad y a factores locales. El análisis
> estadístico muestra que El Niño se asocia claramente con más eventos en la
> Costa (en especial inundaciones), pero esa asociación es débil o no
> detectable en la Sierra y el Oriente, y los aluviones no aumentan durante
> El Niño. **El índice no es un pronóstico de lluvia ni de impactos futuros:**
> supone que los patrones históricos pueden repetirse, algo menos sólido donde
> la señal de El Niño es débil. Se basa en reportes SNGRE/ECU911, sujetos a
> variaciones de cobertura entre regiones y años. Úsese como apoyo a la
> priorización junto con información climática vigente (p. ej. INAMHI) y
> análisis local, no como sustituto.

## Ya implementado

* Aviso metodológico visible en el atlas y el dashboard.
* Etiqueta de señal de El Niño para cada cantón (fuerte, moderada, débil, no detectable, inversa). Nota: se basa en la región de la provincia, por lo que algunos cantones de transición pueden quedar mal clasificados.
* Infografía que explica el método en lenguaje sencillo: `outputs/figures/HCI_Infografia_Metodologia.png`.
