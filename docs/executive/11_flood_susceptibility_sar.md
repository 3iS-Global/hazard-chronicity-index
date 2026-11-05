# 11 — Frecuencia de Inundación Detectada por Satélite (resumen ejecutivo)

**Fase 11 (extensión) del proyecto HCI Ecuador — completa el 6 de agosto de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

Todo el proyecto hasta ahora midió cronicidad a partir de **reportes
humanos** de desastre (SNGRE/ECU911). Esta fase añade una fuente
completamente distinta: imágenes de radar satelital (Sentinel-1), que
pueden "ver" el agua en el terreno directamente, de día o de noche, con
nubes o sin ellas. El resultado es un mapa de qué zonas se inundaron
repetidamente según lo que el satélite observó — no según lo que alguien
reportó — clasificado en 5 categorías igual que hicimos con el HCI.

## ¿Qué se hizo?

1. Se escribió el análisis en Google Earth Engine y Jerson lo corrió en
   su propia cuenta (este entorno no tiene acceso directo a Google Earth
   Engine, la misma limitación que ya tuvimos con los límites
   administrativos y los datos de temperatura del mar).
2. En el camino aparecieron tres problemas técnicos reales durante los
   primeros intentos de ejecución — los tres se diagnosticaron y
   corrigieron (detalle abajo).
3. Con el resultado ya en mano (un archivo de imagen georreferenciada
   cubriendo todo el país), se clasificó en 5 categorías, se convirtió a
   un mapa y se comparó contra los 7,281 reportes históricos de
   inundación para ver si tenía sentido.

## Resultado final

El satélite pudo analizar **9 de las 15 fechas** originalmente
planeadas (las otras 6, sobre todo de 2015 y parte de 2016, no tenían
suficiente cobertura satelital disponible en esos años — explicado más
abajo). Con esas 9 fechas:

- Se detectaron **6,740 km²** del país con alguna señal de inundación
  al menos una vez.
- Clasificado en 5 categorías, el patrón que imaginaste al pedir esto
  se confirmó exactamente: la categoría **Muy Baja** (inundada una sola
  vez) cubre la mayor área (4,584 km²), y la categoría **Muy Alta**
  (inundada muy repetidamente) cubre la menor área (314 km²) — cuanto
  más se repite, más pequeña y específica es la zona.
- Al comparar con los 7,281 reportes históricos de inundación: el
  88% de esos reportes cayó en zonas donde el satélite no detectó nada
  ese día en particular — lo cual tiene una explicación simple, no es un
  fallo: el satélite solo miró 9 días puntuales de los ~4,000 días que
  cubre el proyecto (apenas un 2.9% del calendario). De los reportes que
  sí caen dentro de esas 9 fechas puntuales, el satélite coincidió con
  ellos **4.2 veces más de lo que el azar explicaría** — una señal real
  de que el radar y los reportes humanos, siendo dos fuentes totalmente
  independientes, sí se validan mutuamente cuando se les compara en el
  mismo momento.
- Curiosamente, las zonas que el satélite marca como más críticas
  (Alta/Muy Alta) coinciden visualmente con la misma zona alrededor de
  Quito que ya habíamos identificado como núcleo de cronicidad en la
  Fase 9 (análisis de hotspots) — dos fuentes de evidencia
  independientes señalando el mismo lugar.

## Los tres problemas técnicos que aparecieron y se corrigieron

**1. Un error de programación (`__file__`)** — el notebook no encontraba
un archivo de configuración al correr en modo Colab. Se corrigió y se
convirtió el entregable de script suelto a notebook completo.

**2. Fechas sin cobertura satelital** — al correr por primera vez, una
de las fechas falló porque el satélite Sentinel-1 no tenía ninguna
imagen disponible sobre esa parte del país en ese momento: más probable
en 2015 y parte de 2016, cuando el satélite llevaba menos de dos años en
órbita y aún operaba solo (su gemelo, Sentinel-1B, se lanzó en 2016).
Se agregó una revisión automática que verifica disponibilidad antes de
procesar cada fecha, y excluye — avisando explícitamente — las que no
tienen datos completos, en vez de fallar a mitad de camino. También se
agregó, a tu pedido, que el notebook muestre el estado de la exportación
cada 30 segundos mientras corre en Google, igual que en los scripts de
otros países.

**3. Un formato numérico no compatible con la exportación** — al sumar
las 9 capas de inundación en una sola, Google guardaba internamente el
resultado en un formato que la exportación final no acepta. Se corrigió
indicándole a Earth Engine que use un formato más simple, sin perder
ninguna información real.

También se preparó, sin necesidad de usarla al final, una versión
alternativa más liviana (`Step11b`) por si la corrida original volvía a
fallar o tardaba demasiado — quedó como respaldo, documentada, sin
tocar el archivo principal mientras este corría.

## Cómo se construyó el mapa final

Con el archivo de imagen ya en mano, se intentó primero dibujar los
contornos exactos de las zonas inundadas, pero esto resultó
computacionalmente inviable en este entorno (la zona más dispersa por sí
sola generaba más de 180,000 formas individuales que no se podían unir
en un tiempo razonable). Se probó simplificar la imagen a cuadros más
grandes antes de dibujar los contornos, pero esto exageraba
artificialmente el área "inundada" hasta 13 veces más de lo real — no
aceptable para una herramienta que debe informar decisiones reales.

La solución: se reutilizó la misma cuadrícula hexagonal (~85 km² por
hexágono) que ya se había construido y validado en la Fase 9, y se
calculó el promedio de inundación dentro de cada hexágono — un método
que no exagera el área, a diferencia de la alternativa descartada. El
mapa final usa esa cuadrícula. Para quien necesite el detalle exacto
píxel por píxel (30 metros), ese archivo también queda guardado y
disponible.

## Un chequeo adicional: ¿el umbral de -3 dB es el correcto?

Preguntaste si el umbral fijo que usamos para decidir "esto es agua nueva"
(-3 dB de caída en la señal de radar) es realmente el adecuado para tus
datos, o si deberíamos calcularlo de otra forma. Agregué una nueva sección
al notebook de Google Earth Engine que, sin cambiar el umbral que ya usa el
análisis, lo compara contra un cálculo automático (el "método de Otsu",
una técnica estándar que encuentra el punto que mejor separa dos grupos en
una distribución de datos — en este caso, "cambió" vs. "no cambió").

Cuando corras esta parte, vas a ver, fecha por fecha, cuánto se aleja el
umbral automático del -3 dB fijo. Si en promedio están cerca, confirma que
el -3 dB es una buena elección para tu zona de estudio; si se alejan
consistentemente, sería la señal de ajustarlo.

**Ya corriste esta parte, y el resultado fue mixto:** en las 3 fechas de
2024 el cálculo automático coincidió bien con el -3 dB que usamos. Pero
en las 6 fechas de 2017 y 2023, el cálculo automático sugirió un umbral
mucho más débil (apenas -0.5 a +0.25 dB, en vez de -3 dB).

Mi interpretación, no tomada al pie de la letra: esto probablemente no
significa que el -3 dB esté mal — significa que el método automático
(Otsu) tiene problemas cuando la zona realmente inundada es muy pequeña
comparada con el resto del país (que es exactamente nuestro caso: apenas
0.57% del área analizada muestra alguna inundación). En vez de encontrar
el punto real que separa "agua nueva" de "sin cambio", el método termina
partiendo por la mitad el grupo mayoritario (el terreno normal), lo cual
no tiene sentido físico. Que 2024 sí haya coincidido bien apoya esta
lectura: probablemente hubo más área realmente inundada ese año dentro
de la zona analizada, dándole al método automático algo más sólido con
qué trabajar.

Para comprobar esto con evidencia concreta (no solo con una intuición),
agregué una tercera celda que calcula cuánta área quedaría marcada como
"inundada" si usáramos el umbral automático en vez del -3 dB.

**Resultado: confirma la sospecha con un margen muy amplio.** En 2017 y
2023, usar el umbral automático habría marcado entre **13 y 51 veces
más área** como "inundada" que el -3 dB que usamos. En 2024 (donde el
umbral automático ya había coincidido bien), la diferencia es mínima. Un
salto de hasta 51 veces más área no es una corrección razonable — es la
señal clara de que el método automático, en las fechas con poca
inundación real, terminó marcando variación normal del radar (humedad
del suelo, vegetación, ruido de la señal) como si fuera agua nueva.

**Conclusión: se mantiene el -3 dB sin cambios.** Quedó puesto a prueba
con dos chequeos independientes, no solo tomado de la literatura por
default — y ambos apuntan en la misma dirección: es la elección correcta
para este análisis.

## Nota importante

Este mapa mide algo distinto al HCI, no lo reemplaza: el HCI dice "aquí
la gente reportó inundaciones repetidas"; este nuevo mapa dice "aquí el
satélite observó agua repetidas veces, en los momentos puntuales que se
pudo mirar". Comparar ambos y ver dónde coinciden (como la zona de
Quito) y dónde no, es en sí mismo un hallazgo útil para priorizar dónde
confiar más en cada fuente.
